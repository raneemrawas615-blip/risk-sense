import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import base64

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Risk Sense | ريسك سينس",
    page_icon="🩺",
    layout="centered",
)

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "lang" not in st.session_state:
    st.session_state.lang = "en"
if "page" not in st.session_state:
    st.session_state.page = "home"

# ─────────────────────────────────────────────
# ─────────────────────────────────────────────
# BACKGROUND IMAGE HELPER
# ─────────────────────────────────────────────
BG_URL = "https://raw.githubusercontent.com/raneemrawas615-blip/risk-sense/main/bg.png"
bg_b64 = BG_URL
# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────
bg_css = f"""
background-image: url("{bg_b64}");
background-size: cover;
background-position: center;
""" if bg_b64 else "background: linear-gradient(135deg,#1a0533,#0f0f1a);"

st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&family=Inter:wght@400;600;700&display=swap');

  html, body, [class*="css"] {{
    background-color: #0f0f1a !important;
    color: #e0e0f0 !important;
    font-family: 'Inter', 'Cairo', sans-serif;
  }}
  .stApp {{ background-color: #0f0f1a; }}

  /* ── HOME PAGE ── */
  .home-wrapper {{
    position: relative;
    min-height: 85vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 40px 20px;
    border-radius: 20px;
    overflow: hidden;
  }}
  .home-bg {{
    position: absolute; inset: 0;
    {bg_css}
    border-radius: 20px;
    filter: blur(6px) brightness(0.45);
    transform: scale(1.05);
    z-index: 0;
  }}
  .home-content {{ position: relative; z-index: 1; }}
  .home-title {{
    font-size: 3rem; font-weight: 800;
    background: linear-gradient(135deg, #c084fc, #38bdf8);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 12px;
  }}
  .home-sub {{
    color: #d1d5db; font-size: 1rem; margin-bottom: 8px;
  }}
  .home-disclaimer {{
    background: rgba(124,58,237,0.15);
    border: 1px solid rgba(124,58,237,0.4);
    border-radius: 12px;
    padding: 12px 20px;
    font-size: 0.85rem;
    color: #c4b5fd;
    max-width: 600px;
    margin: 20px auto 32px;
  }}

  /* ── CARDS ── */
  .card {{
    background: #1a1a2e; border: 1px solid #2a2a4a;
    border-radius: 16px; padding: 24px; margin-bottom: 20px;
  }}
  .card-title {{
    font-size: 1.05rem; font-weight: 700; color: #a78bfa;
    margin-bottom: 14px; padding-bottom: 8px;
    border-bottom: 1px solid #2a2a4a;
  }}

  /* ── HEADER ── */
  .app-header {{ text-align: center; padding: 24px 16px 8px; }}
  .app-title {{
    font-size: 1.8rem; font-weight: 800;
    background: linear-gradient(135deg, #a78bfa, #38bdf8);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 4px;
  }}
  .app-subtitle {{ color: #6b7280; font-size: 0.85rem; }}

  /* ── DISCLAIMER ── */
  .disclaimer {{
    background: #1e1a2e; border-left: 4px solid #7c3aed;
    border-radius: 8px; padding: 12px 16px;
    font-size: 0.85rem; color: #9ca3af; margin: 12px 0;
  }}
  .disclaimer-info {{
    background: rgba(56,189,248,0.08); border-left: 4px solid #38bdf8;
    border-radius: 8px; padding: 12px 16px;
    font-size: 0.85rem; color: #bae6fd; margin: 12px 0;
  }}

  /* ── RISK BADGES ── */
  .risk-low  {{ background:#064e3b; color:#6ee7b7; border:1px solid #10b981; border-radius:12px; padding:6px 18px; font-weight:700; }}
  .risk-mod  {{ background:#78350f; color:#fcd34d; border:1px solid #f59e0b; border-radius:12px; padding:6px 18px; font-weight:700; }}
  .risk-high {{ background:#7f1d1d; color:#fca5a5; border:1px solid #ef4444; border-radius:12px; padding:6px 18px; font-weight:700; }}

  /* ── PROB BAR ── */
  .prob-bar-container {{ background:#2a2a4a; border-radius:12px; overflow:hidden; height:22px; margin:10px 0; }}
  .prob-bar-low  {{ background:linear-gradient(90deg,#10b981,#34d399); height:100%; border-radius:12px; }}
  .prob-bar-mod  {{ background:linear-gradient(90deg,#f59e0b,#fbbf24); height:100%; border-radius:12px; }}
  .prob-bar-high {{ background:linear-gradient(90deg,#ef4444,#f87171); height:100%; border-radius:12px; }}

  /* ── RECOMMENDATIONS ── */
  .rec-item {{ display:flex; gap:10px; padding:10px 0; border-bottom:1px solid #2a2a4a; font-size:0.95rem; }}
  .rec-item:last-child {{ border-bottom:none; }}

  /* ── NAV TABS ── */
  .nav-tab {{
    display: inline-flex; gap: 8px; background: #1a1a2e;
    border-radius: 12px; padding: 6px; margin-bottom: 20px;
  }}
  .nav-btn {{
    padding: 8px 20px; border-radius: 8px; border: none;
    font-size: 0.9rem; font-weight: 600; cursor: pointer;
    transition: all 0.2s;
  }}
  .nav-btn-active {{ background: linear-gradient(135deg,#7c3aed,#2563eb); color: white; }}
  .nav-btn-inactive {{ background: transparent; color: #9ca3af; }}

  /* ── COMPARISON TABLE ── */
  .compare-table {{ width:100%; border-collapse: collapse; font-size: 0.9rem; }}
  .compare-table th {{
    background: linear-gradient(135deg,#7c3aed,#2563eb);
    color: white; padding: 10px 14px; text-align: right;
  }}
  .compare-table td {{ padding: 10px 14px; border-bottom: 1px solid #2a2a4a; color: #d1d5db; }}
  .compare-table tr:hover td {{ background: #1e1e35; }}
  .compare-table .feature {{ color: #a78bfa; font-weight: 600; }}

  /* ── LAB CARD ── */
  .lab-card {{
    background: #1a1a2e; border: 1px solid #2a2a4a;
    border-radius: 12px; padding: 16px; margin-bottom: 12px;
  }}
  .lab-name {{ color: #c084fc; font-weight: 700; font-size: 1rem; margin-bottom: 4px; }}
  .lab-desc {{ color: #9ca3af; font-size: 0.85rem; margin-bottom: 10px; }}
  .lab-bar-bg {{ background: #2a2a4a; border-radius: 8px; overflow: hidden; height: 16px; margin: 4px 0; }}
  .lab-bar-f  {{ background: linear-gradient(90deg,#a855f7,#c084fc); height:100%; border-radius:8px; }}
  .lab-bar-m  {{ background: linear-gradient(90deg,#2dd4bf,#38bdf8); height:100%; border-radius:8px; }}

  /* ── STREAMLIT OVERRIDES ── */
  .stRadio > label {{ color:#c4b5fd !important; font-weight:600; }}
  .stSlider > label {{ color:#c4b5fd !important; font-weight:600; }}
  .stSelectbox > label {{ color:#c4b5fd !important; font-weight:600; }}
  .stNumberInput > label {{ color:#c4b5fd !important; font-weight:600; }}
  div[data-baseweb="select"] {{ background:#1a1a2e !important; border-color:#3a3a5a !important; }}
  .stButton > button {{
    background: linear-gradient(135deg, #7c3aed, #2dd4bf) !important;
    color: white !important; border: none !important;
    border-radius: 12px !important; padding: 10px 32px !important;
    font-size: 1rem !important; font-weight: 700 !important;
    width: 100%; margin-top: 6px;
  }}
  .stButton > button:hover {{ opacity: 0.9; }}
  [data-testid="stRadio"] div {{ color: #d1d5db !important; }}
  .stExpander {{ background: #1a1a2e !important; border: 1px solid #2a2a4a !important; border-radius: 12px !important; }}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TRANSLATIONS
# ─────────────────────────────────────────────
T = {
"en": {
  "lang_btn": "🌐 عربي",
  "nav_assess": "🤖 Smart Assessment",
  "nav_guide": "📚 Diabetes Guide",
  "back_home": "← Home",

  # Home
  "home_title": "Risk Sense",
  "home_sub": "Diabetes Type 2 Risk Predictor",
  "home_disclaimer": "💡 This tool does not provide a medical diagnosis. It helps you understand how your daily habits and health status may influence your risk of developing Type 2 Diabetes.",
  "home_btn_assess": "🤖 Smart Assessment",
  "home_btn_guide": "📚 Diabetes Guide",
  "home_source": "Based on CDC BRFSS 2015 Health Indicators Dataset",

  # Assessment
  "assess_title": "Smart Assessment",
  "assess_sub": "Type 2 Diabetes Risk Predictor — Based on CDC BRFSS 2015",
  "disclaimer_main": "💡 This tool does not replace a medical diagnosis. Results reflect lifestyle and health indicators that may influence Type 2 Diabetes risk.",
  "sec_demo": "👤 Demographics",
  "sec_body": "📏 Body & General Health",
  "sec_bmi_method": "How would you like to enter your BMI?",
  "bmi_calc": "Calculate for me (Height & Weight)",
  "bmi_enter": "Enter BMI directly",
  "bmi_cat": "Select my category",
  "bmi_height": "Height (cm)",
  "bmi_weight": "Weight (kg)",
  "bmi_label": "Body Mass Index (BMI)",
  "bmi_hint": "BMI = weight(kg) / height(m)²",
  "bmi_result": "Your BMI",
  "bmi_cats": ["Underweight (< 18.5)", "Normal (18.5 – 24.9)", "Overweight (25 – 29.9)", "Class I Obesity (30 – 34.9)", "Class II Obesity (35 – 39.9)", "Class III Obesity (≥ 40)"],
  "bmi_cat_vals": [17.0, 22.0, 27.0, 32.0, 37.0, 45.0],
  "q_gh": "How would you rate your general health?",
  "gh_opts": ["Excellent", "Very Good", "Good", "Fair", "Poor"],
  "sec_conditions": "❤️ Medical Conditions",
  "q_bp": "Do you suffer from high blood pressure (diagnosed by a doctor)?",
  "q_chol": "Do you suffer from high cholesterol (diagnosed by a doctor)?",
  "q_stroke": "Have you ever had a stroke?",
  "q_heart": "Do you have coronary heart disease or a history of heart attack?",
  "q_walk": "Do you have serious difficulty walking or climbing stairs?",
  "sec_lifestyle": "🏃 Lifestyle",
  "q_smoke": "Have you smoked at least 100 cigarettes in your lifetime?",
  "q_phys": "Did you engage in any physical activity in the past 30 days?",
  "sec_days": "📅 Health Days (Past 30 Days)",
  "q_ment": "Days your mental health was NOT good (0–30)",
  "q_phys2": "Days your physical health was NOT good (0–30)",
  "sec_demo2": "👤 Personal Info",
  "q_age": "Age Group",
  "q_edu": "Highest Education Level",
  "q_inc": "Annual Household Income",
  "age_opts": ["18–24","25–29","30–34","35–39","40–44","45–49","50–54","55–59","60–64","65–69","70–74","75–79","80+"],
  "gh_opts2": ["Excellent","Very Good","Good","Fair","Poor"],
  "edu_opts": ["Never attended / Kindergarten","Elementary","Some high school","High school graduate","Some college","College graduate"],
  "inc_opts": ["< $10,000","$10,000–$14,999","$15,000–$19,999","$20,000–$24,999","$25,000–$34,999","$35,000–$49,999","$50,000–$74,999","$75,000+"],
  "yes": "Yes", "no": "No",
  "submit": "Get My Risk Assessment",
  "result_title": "Your Risk Assessment",
  "risk_label": "Risk Level",
  "prob_label": "Predicted Probability",
  "rec_title": "Recommendations",
  "nutrition_btn": "🥗 Nutritional Recommendations",
  "low": "Low Risk", "mod": "Moderate Risk", "high": "High Risk",
  "rec_low": [
    "✅ Great news! Your risk is low — keep your healthy habits.",
    "🏃 Stay physically active — aim for 150 min/week.",
    "🩺 Schedule regular annual check-ups.",
    "💧 Stay hydrated and maintain quality sleep.",
    "🥗 Continue eating fruits and vegetables daily.",
  ],
  "rec_mod": [
    "⚠️ Moderate risk — take action now before it progresses.",
    "🏃 Increase physical activity to at least 150 minutes per week.",
    "🥗 Reduce refined carbohydrates and sugary drinks.",
    "📊 Monitor blood pressure and cholesterol regularly.",
    "🩺 Consult your doctor for a blood glucose test.",
    "😴 Prioritize sleep quality and stress management.",
  ],
  "rec_high": [
    "🚨 High risk — please consult a doctor as soon as possible.",
    "🩸 Request a fasting blood glucose test immediately.",
    "💊 Discuss treatment or prevention options with your doctor.",
    "🥗 Follow a diabetes-friendly diet: low sugar, high fiber.",
    "🏃 Even a 30-minute daily walk can significantly help.",
    "📱 Consider regularly monitoring your blood glucose.",
  ],

  # Guide
  "guide_title": "Diabetes Guide",
  "guide_sub": "Your Comprehensive Guide to Type 2 Diabetes",
  "g_about": "📖 What is Type 2 Diabetes?",
  "g_diff": "🔄 Type 1 vs Type 2 — What's the Difference?",
  "g_symptoms_same": "❓ Do They Share the Same Symptoms?",
  "g_symptoms": "🤒 Symptoms of Type 2 Diabetes",
  "g_risk": "⚠️ Risk Factors",
  "g_complications": "🫀 Complications",
  "g_prevention": "🛡️ Prevention",
  "g_stats": "🌍 Global Statistics (WHO)",
  "g_lab": "🩸 Lab Tests & Diabetes — Real Data from Jordan",
  "g_nutrition": "🥗 Nutritional Recommendations",
  "nutrition_coming": "Coming soon — data from a certified Jordanian nutrition center.",

  "about_text": """
Type 2 Diabetes is a chronic condition that affects how the body uses glucose (blood sugar). It occurs when the body either doesn't produce enough insulin, or the cells don't respond properly to it — leading to high blood sugar levels.

Insulin is a hormone produced by the pancreas that allows sugar to enter cells and be used for energy. In Type 2 Diabetes, this system breaks down gradually — often due to lifestyle factors, genetics, or both.

**Key fact:** Type 2 Diabetes is largely preventable and manageable through lifestyle changes.
  """,

  "diff_intro": "Although both types involve blood sugar problems, they differ significantly in cause, mechanism, and management:",
  "diff_headers": ["Feature", "Type 1", "Type 2"],
  "diff_rows": [
    ["Cause", "Autoimmune — immune system attacks insulin-producing cells", "Insulin resistance + insufficient insulin production"],
    ["Typical Age", "Often in childhood or young adults", "Usually 40+ (but increasingly younger)"],
    ["Insulin", "Always required", "Sometimes required; often managed with lifestyle/meds"],
    ["Onset", "Sudden, rapid", "Gradual, often unnoticed"],
    ["Prevention", "Not preventable", "Largely preventable through lifestyle changes"],
    ["Weight", "Usually normal or underweight", "Often associated with overweight or obesity"],
    ["Percentage", "~5–10% of diabetes cases", "~90–95% of diabetes cases"],
  ],

  "symptoms_same_text": """
**They share many common symptoms**, because both result in elevated blood sugar levels. However, Type 1 symptoms tend to appear suddenly and severely, while Type 2 symptoms often develop slowly and may go unnoticed for years.

**Shared symptoms include:** frequent urination, excessive thirst, fatigue, blurry vision, and slow-healing wounds.

**Key difference:** Type 1 may include rapid weight loss and fruity-smelling breath (from ketoacidosis), which is rare in Type 2.
  """,

  "symptoms_list": [
    "🚽 Frequent urination, especially at night",
    "💧 Excessive thirst",
    "😴 Unusual fatigue and low energy",
    "👁️ Blurry or changing vision",
    "🩹 Slow-healing cuts or bruises",
    "🦶 Tingling, numbness, or pain in hands/feet",
    "⚖️ Unexplained weight changes",
    "🍽️ Increased hunger even after eating",
    "🦠 Frequent infections (skin, gum, urinary)",
  ],

  "risk_list": [
    "⚖️ Overweight or obesity (especially belly fat)",
    "🛋️ Sedentary lifestyle / physical inactivity",
    "👨‍👩‍👧 Family history of Type 2 Diabetes",
    "🩸 High blood pressure or cholesterol",
    "🎂 Age over 40 (risk increases with age)",
    "🤰 History of gestational diabetes",
    "😴 Poor sleep or chronic stress",
    "🚬 Smoking",
  ],

  "complications_list": [
    ("❤️ Heart & Blood Vessels", "Diabetes doubles the risk of cardiovascular disease and stroke."),
    ("🫘 Kidneys", "Diabetic nephropathy can lead to chronic kidney disease and dialysis."),
    ("👁️ Eyes", "Diabetic retinopathy is a leading cause of blindness worldwide."),
    ("🦶 Feet", "Nerve damage and poor circulation can lead to severe foot complications."),
    ("🧠 Nervous System", "Neuropathy causes tingling, pain, and loss of sensation."),
    ("🦷 Oral Health", "Diabetes increases risk of gum disease and tooth loss."),
  ],

  "prevention_list": [
    "🏃 150+ minutes of moderate physical activity per week",
    "⚖️ Maintain a healthy weight — losing even 5–7% reduces risk significantly",
    "🥗 Eat a balanced diet rich in fiber, whole grains, and vegetables",
    "🚭 Avoid smoking and excessive alcohol",
    "💤 Get 7–8 hours of quality sleep",
    "📊 Regular health screenings (blood sugar, cholesterol, blood pressure)",
    "😌 Manage stress effectively",
  ],

  "stats_items": [
    ("830 million", "People living with diabetes worldwide in 2022 (WHO)"),
    ("200 million → 830M", "The number quadrupled from 1990 to 2022"),
    ("> 50%", "Of people with diabetes were not receiving treatment in 2022"),
    ("#1 cause", "Diabetes is a leading cause of blindness, kidney failure, and limb amputation"),
    ("90–95%", "Of all diabetes cases are Type 2"),
  ],

  "lab_intro": "This analysis is based on real patient data from Smart Lab Jordan — over 10,000 patients. It shows how abnormal lab results are significantly more common in diabetic patients across all age groups.",
  "lab_rank_title": "🏆 Strength of Association with Diabetes",
  "lab_tests": [
    {
      "name": "Triglycerides (ثلاثي الغليسريد)",
      "rank": "#1 Strongest",
      "desc_en": "Blood fats that rise when the body can't properly use insulin. Strongly linked to metabolic syndrome and Type 2 Diabetes.",
      "female_d": 47.7, "female_nd": 25.3, "male_d": 43.6, "male_nd": 34.5,
      "gap_f": "+22.4%", "gap_m": "+9.1%",
    },
    {
      "name": "CRP (C-Reactive Protein)",
      "rank": "#2",
      "desc_en": "A marker of inflammation. Elevated CRP indicates systemic inflammation, which plays a key role in insulin resistance.",
      "female_d": 49.4, "female_nd": 34.0, "male_d": 33.5, "male_nd": 25.4,
      "gap_f": "+15.3%", "gap_m": "+8.1%",
    },
    {
      "name": "GGT (Gamma-Glutamyl Transferase)",
      "rank": "#3",
      "desc_en": "A liver enzyme. Elevated GGT reflects liver stress — often linked to fatty liver, which is strongly associated with diabetes.",
      "female_d": 17.8, "female_nd": 6.5, "male_d": 14.7, "male_nd": 10.6,
      "gap_f": "+11.2%", "gap_m": "+4.1%",
    },
    {
      "name": "Creatinine (كرياتينين)",
      "rank": "#4",
      "desc_en": "A kidney function marker. Elevated creatinine in diabetic patients reflects early kidney stress — one of the most common diabetes complications.",
      "female_d": 17.5, "female_nd": 7.8, "male_d": 15.1, "male_nd": 8.0,
      "gap_f": "+9.7%", "gap_m": "+7.1%",
    },
  ],
  "lab_female": "🟣 Female", "lab_male": "🩵 Male",
  "lab_diabetic": "Diabetic", "lab_nondiabetic": "Non-Diabetic",
  "lab_note": "* Percentage of patients with abnormal results. Data: Smart Lab Jordan, 10,067 patients.",
},

"ar": {
  "lang_btn": "🌐 English",
  "nav_assess": "🤖 التقييم الذكي",
  "nav_guide": "📚 دليل السكري",
  "back_home": "← الرئيسية",

  # Home
  "home_title": "ريسك سينس",
  "home_sub": "تنبؤ بخطر الإصابة بالسكري من النوع الثاني",
  "home_disclaimer": "💡 هذه الأداة لا تُقدّم تشخيصاً طبياً. تساعدك على فهم تأثير عاداتك اليومية وحالتك الصحية على احتمالية إصابتك بالسكري من النوع الثاني.",
  "home_btn_assess": "🤖 التقييم الذكي",
  "home_btn_guide": "📚 دليل السكري",
  "home_source": "مبني على بيانات CDC BRFSS 2015",

  # Assessment
  "assess_title": "التقييم الذكي",
  "assess_sub": "تنبؤ بخطر السكري من النوع الثاني — مبني على CDC BRFSS 2015",
  "disclaimer_main": "💡 هذه الأداة لا تُغني عن التشخيص الطبي. النتائج تعكس مؤشرات نمط الحياة والصحة المرتبطة بخطر الإصابة بالسكري من النوع الثاني.",
  "sec_demo": "👤 المعلومات الشخصية",
  "sec_body": "📏 الجسم والصحة العامة",
  "sec_bmi_method": "كيف تريد إدخال مؤشر كتلة الجسم؟",
  "bmi_calc": "احسب لي (الطول والوزن)",
  "bmi_enter": "أدخل الرقم مباشرة",
  "bmi_cat": "اختر فئتي",
  "bmi_height": "الطول (سم)",
  "bmi_weight": "الوزن (كغ)",
  "bmi_label": "مؤشر كتلة الجسم (BMI)",
  "bmi_hint": "BMI = الوزن(كغ) ÷ الطول(م)²",
  "bmi_result": "مؤشر كتلة جسمك",
  "bmi_cats": ["نحيف (< 18.5)", "طبيعي (18.5 – 24.9)", "زيادة وزن (25 – 29.9)", "سمنة درجة أولى (30 – 34.9)", "سمنة درجة ثانية (35 – 39.9)", "سمنة مفرطة (≥ 40)"],
  "bmi_cat_vals": [17.0, 22.0, 27.0, 32.0, 37.0, 45.0],
  "q_gh": "كيف تقيّم صحتك العامة؟",
  "gh_opts": ["ممتاز", "جيد جداً", "جيد", "مقبول", "سيئ"],
  "sec_conditions": "❤️ الحالات الطبية",
  "q_bp": "هل تعاني من ارتفاع ضغط الدم (تم تشخيصه من قِبل طبيب)؟",
  "q_chol": "هل تعاني من ارتفاع الكوليسترول (تم تشخيصه من قِبل طبيب)؟",
  "q_stroke": "هل سبق أن أُصبت بجلطة دماغية؟",
  "q_heart": "هل تعاني من مرض قلبي أو أصبت بنوبة قلبية من قبل؟",
  "q_walk": "هل تعاني من صعوبة شديدة في المشي أو صعود السلالم؟",
  "sec_lifestyle": "🏃 نمط الحياة",
  "q_smoke": "هل دخّنت 100 سيجارة أو أكثر في حياتك؟",
  "q_phys": "هل مارست أي نشاط بدني خلال الـ 30 يوماً الماضية؟",
  "sec_days": "📅 أيام الصحة (الـ 30 يوم الماضية)",
  "q_ment": "كم يوماً لم تكن صحتك النفسية جيدة؟ (0–30)",
  "q_phys2": "كم يوماً لم تكن صحتك الجسدية جيدة؟ (0–30)",
  "sec_demo2": "👤 المعلومات الشخصية",
  "q_age": "الفئة العمرية",
  "q_edu": "أعلى مستوى تعليمي",
  "q_inc": "إجمالي دخل الأسرة السنوي",
  "age_opts": ["18–24","25–29","30–34","35–39","40–44","45–49","50–54","55–59","60–64","65–69","70–74","75–79","80+"],
  "gh_opts2": ["ممتاز","جيد جداً","جيد","مقبول","سيئ"],
  "edu_opts": ["لم أذهب للمدرسة / روضة","ابتدائية","بعض سنوات الثانوية","ثانوية عامة","بعض سنوات الجامعة","تخرجت من الجامعة"],
  "inc_opts": ["أقل من 10,000$","10,000–14,999$","15,000–19,999$","20,000–24,999$","25,000–34,999$","35,000–49,999$","50,000–74,999$","75,000$ أو أكثر"],
  "yes": "نعم", "no": "لا",
  "submit": "احصل على تقييم الخطر",
  "result_title": "نتيجة تقييمك",
  "risk_label": "مستوى الخطر",
  "prob_label": "الاحتمالية المتوقعة",
  "rec_title": "التوصيات",
  "nutrition_btn": "🥗 التوصيات الغذائية",
  "low": "خطر منخفض", "mod": "خطر متوسط", "high": "خطر مرتفع",
  "rec_low": [
    "✅ بشرى سارة! خطرك منخفض — استمر في عاداتك الصحية.",
    "🏃 حافظ على النشاط البدني — 150 دقيقة أسبوعياً على الأقل.",
    "🩺 أجرِ فحوصات صحية دورية سنوية.",
    "💧 اشرب كمية كافية من الماء واحرص على النوم الجيد.",
    "🥗 واصل تناول الفواكه والخضروات يومياً.",
  ],
  "rec_mod": [
    "⚠️ خطر متوسط — ابدأ باتخاذ إجراءات الآن قبل أن يتطور.",
    "🏃 زد نشاطك البدني إلى 150 دقيقة أسبوعياً على الأقل.",
    "🥗 قلّل من الكربوهيدرات المكررة والمشروبات السكرية.",
    "📊 راقب ضغط دمك ومستوى الكوليسترول بانتظام.",
    "🩺 استشر طبيبك لإجراء فحص سكر الدم.",
    "😴 اهتم بجودة نومك وإدارة مستوى التوتر.",
  ],
  "rec_high": [
    "🚨 خطر مرتفع — يُرجى مراجعة الطبيب في أقرب وقت ممكن.",
    "🩸 أجرِ فحص سكر الدم الصائم فوراً.",
    "💊 ناقش خيارات العلاج أو الوقاية مع طبيبك.",
    "🥗 اتبع نظاماً غذائياً مناسباً: قليل السكر وغني بالألياف.",
    "🏃 المشي 30 دقيقة يومياً يساعد بشكل ملحوظ.",
    "📱 فكّر في متابعة مستوى الغلوكوز بانتظام.",
  ],

  # Guide
  "guide_title": "دليل السكري",
  "guide_sub": "دليلك الشامل عن السكري من النوع الثاني",
  "g_about": "📖 ما هو السكري من النوع الثاني؟",
  "g_diff": "🔄 النوع الأول مقابل النوع الثاني — ما الفرق؟",
  "g_symptoms_same": "❓ هل أعراضهما واحدة؟",
  "g_symptoms": "🤒 أعراض السكري من النوع الثاني",
  "g_risk": "⚠️ عوامل الخطر",
  "g_complications": "🫀 المضاعفات",
  "g_prevention": "🛡️ الوقاية",
  "g_stats": "🌍 إحصائيات عالمية (منظمة الصحة العالمية)",
  "g_lab": "🩸 تحاليل المختبر والسكري — بيانات حقيقية من الأردن",
  "g_nutrition": "🥗 التوصيات الغذائية",
  "nutrition_coming": "قريباً — بيانات من مركز تغذوي أردني معتمد.",

  "about_text": """
السكري من النوع الثاني هو حالة مزمنة تؤثر على طريقة استخدام الجسم للجلوكوز (سكر الدم). يحدث إما لأن الجسم لا يُنتج كمية كافية من الأنسولين، أو لأن الخلايا لا تستجيب له بشكل صحيح — مما يُؤدي إلى ارتفاع مستوى السكر في الدم.

الأنسولين هرمون تُنتجه البنكرياس يسمح للسكر بدخول الخلايا وتحويله إلى طاقة. في السكري من النوع الثاني، يتعطل هذا النظام تدريجياً — غالباً بسبب عوامل نمط الحياة أو الوراثة أو كليهما.

**حقيقة مهمة:** السكري من النوع الثاني يمكن الوقاية منه إلى حدٍّ بعيد وإدارته بتغييرات في نمط الحياة.
  """,

  "diff_intro": "رغم أن كلا النوعين يتعلقان بمشاكل في سكر الدم، إلا أنهما يختلفان اختلافاً جوهرياً في الأسباب والآلية والعلاج:",
  "diff_headers": ["الخاصية", "النوع الأول", "النوع الثاني"],
  "diff_rows": [
    ["السبب", "مناعي ذاتي — الجهاز المناعي يهاجم خلايا البنكرياس", "مقاومة الأنسولين + عدم كفاية إنتاجه"],
    ["العمر الشائع", "الأطفال والشباب في الغالب", "عادةً فوق 40 سنة (لكن يتزايد في الأصغر)"],
    ["الأنسولين", "ضروري دائماً", "أحياناً — يمكن الإدارة بالأدوية ونمط الحياة"],
    ["بداية الأعراض", "مفاجئة وحادة", "تدريجية وقد لا تُلاحَظ لسنوات"],
    ["الوقاية", "لا يمكن الوقاية منه", "يمكن الوقاية منه إلى حدٍّ بعيد"],
    ["الوزن", "عادةً طبيعي أو نحيف", "غالباً مرتبط بزيادة الوزن أو السمنة"],
    ["النسبة", "٥–١٠٪ من حالات السكري", "٩٠–٩٥٪ من حالات السكري"],
  ],

  "symptoms_same_text": """
**يتشاركان كثيراً من الأعراض**، لأن كلاهما يُفضي إلى ارتفاع سكر الدم. لكن أعراض النوع الأول تظهر فجأة وبحدة، بينما أعراض النوع الثاني تتطور ببطء وقد تمر سنوات دون ملاحظتها.

**الأعراض المشتركة:** كثرة التبول، العطش الشديد، التعب، تشوش الرؤية، وبطء التئام الجروح.

**الفرق الرئيسي:** النوع الأول قد يُصاحبه فقدان وزن سريع ورائحة الفم الكيتونية، وهذا نادر في النوع الثاني.
  """,

  "symptoms_list": [
    "🚽 كثرة التبول خاصةً في الليل",
    "💧 عطش شديد ومفرط",
    "😴 تعب وإرهاق غير معتاد",
    "👁️ تشوش أو تغيّر في الرؤية",
    "🩹 بطء التئام الجروح والكدمات",
    "🦶 تنميل أو وخز أو ألم في اليدين والقدمين",
    "⚖️ تغيّرات غير مبررة في الوزن",
    "🍽️ جوع مستمر حتى بعد الأكل",
    "🦠 التهابات متكررة (جلد، لثة، مسالك بولية)",
  ],

  "risk_list": [
    "⚖️ زيادة الوزن أو السمنة (خاصةً الكرش)",
    "🛋️ قلة الحركة ونمط الحياة الخامل",
    "👨‍👩‍👧 تاريخ عائلي بالسكري من النوع الثاني",
    "🩸 ارتفاع ضغط الدم أو الكوليسترول",
    "🎂 العمر فوق 40 سنة (الخطر يزداد مع العمر)",
    "🤰 تاريخ من السكري الحملي",
    "😴 قلة النوم أو التوتر المزمن",
    "🚬 التدخين",
  ],

  "complications_list": [
    ("❤️ القلب والأوعية الدموية", "السكري يضاعف خطر الإصابة بأمراض القلب والسكتة الدماغية."),
    ("🫘 الكلى", "اعتلال الكلى السكري قد يؤدي إلى الفشل الكلوي والديلزة."),
    ("👁️ العيون", "اعتلال الشبكية السكري من أبرز أسباب العمى في العالم."),
    ("🦶 القدمان", "تلف الأعصاب وضعف الدورة الدموية قد يُفضيان لمضاعفات خطيرة."),
    ("🧠 الجهاز العصبي", "الاعتلال العصبي يُسبب وخزاً وألماً وفقدان الإحساس."),
    ("🦷 صحة الفم", "السكري يزيد خطر التهابات اللثة وفقدان الأسنان."),
  ],

  "prevention_list": [
    "🏃 150 دقيقة أسبوعياً من النشاط البدني المعتدل على الأقل",
    "⚖️ الحفاظ على وزن صحي — فقدان 5–7٪ من الوزن يُقلل الخطر بشكل ملحوظ",
    "🥗 اتباع نظام غذائي متوازن غني بالألياف والحبوب الكاملة والخضروات",
    "🚭 تجنب التدخين والكحول",
    "💤 النوم 7–8 ساعات يومياً بجودة جيدة",
    "📊 الفحوصات الدورية (سكر الدم، الكوليسترول، ضغط الدم)",
    "😌 إدارة التوتر بفعالية",
  ],

  "stats_items": [
    ("830 مليون", "شخص يعيش مع السكري في 2022 (منظمة الصحة العالمية)"),
    ("200 مليون ← 830 مليون", "الرقم تضاعف أربع مرات منذ 1990 حتى 2022"),
    ("أكثر من 50٪", "من مرضى السكري لم يكونوا يتلقون العلاج في 2022"),
    ("السبب الأول", "السكري سبب رئيسي للعمى، الفشل الكلوي، وبتر الأطراف"),
    ("90–95٪", "من جميع حالات السكري هي من النوع الثاني"),
  ],

  "lab_intro": "هذا التحليل مبني على بيانات حقيقية من Smart Lab الأردن — أكثر من 10,000 مريض. يُظهر أن النتائج المخبرية غير الطبيعية أكثر شيوعاً بشكل ملحوظ عند مرضى السكري مقارنةً بغيرهم.",
  "lab_rank_title": "🏆 قوة الارتباط بالسكري",
  "lab_tests": [
    {
      "name": "Triglycerides (ثلاثي الغليسريد)",
      "rank": "#1 الأقوى",
      "desc_en": "دهون الدم التي ترتفع عندما لا يستطيع الجسم استخدام الأنسولين بشكل صحيح. مرتبطة بقوة بالسكري من النوع الثاني.",
      "female_d": 47.7, "female_nd": 25.3, "male_d": 43.6, "male_nd": 34.5,
      "gap_f": "+22.4%", "gap_m": "+9.1%",
    },
    {
      "name": "CRP (بروتين سي التفاعلي)",
      "rank": "#2",
      "desc_en": "مؤشر الالتهاب. ارتفاعه يعني وجود التهاب منهجي يُقلل من حساسية الخلايا للأنسولين.",
      "female_d": 49.4, "female_nd": 34.0, "male_d": 33.5, "male_nd": 25.4,
      "gap_f": "+15.3%", "gap_m": "+8.1%",
    },
    {
      "name": "GGT (غاما غلوتاميل)",
      "rank": "#3",
      "desc_en": "إنزيم الكبد. ارتفاعه يعكس ضغطاً على الكبد — مرتبط بالكبد الدهني الذي يسبق السكري غالباً.",
      "female_d": 17.8, "female_nd": 6.5, "male_d": 14.7, "male_nd": 10.6,
      "gap_f": "+11.2%", "gap_m": "+4.1%",
    },
    {
      "name": "Creatinine (كرياتينين)",
      "rank": "#4",
      "desc_en": "مؤشر وظائف الكلى. ارتفاعه عند مرضى السكري يعكس بدايات تأثر الكلى — من أبرز مضاعفات المرض.",
      "female_d": 17.5, "female_nd": 7.8, "male_d": 15.1, "male_nd": 8.0,
      "gap_f": "+9.7%", "gap_m": "+7.1%",
    },
  ],
  "lab_female": "🟣 إناث", "lab_male": "🩵 ذكور",
  "lab_diabetic": "مرضى السكري", "lab_nondiabetic": "غير مرضى السكري",
  "lab_note": "* نسبة المرضى الذين أظهرت نتائجهم قيماً غير طبيعية. البيانات: Smart Lab الأردن، 10,067 مريض.",
},
}

# ─────────────────────────────────────────────
# LOAD MODEL
# ─────────────────────────────────────────────
@st.cache_resource
def load_artifacts():
    base = os.path.dirname(__file__)
    model        = joblib.load(os.path.join(base, "diabetes_model.pkl"))
    preprocessor = joblib.load(os.path.join(base, "preprocessor.pkl"))
    feat_names   = joblib.load(os.path.join(base, "feature_names.pkl"))
    threshold    = joblib.load(os.path.join(base, "threshold.pkl"))
    return model, preprocessor, feat_names, threshold

try:
    model, preprocessor, feature_names, threshold = load_artifacts()
    model_loaded = True
except Exception as e:
    model_loaded = False
    load_error = str(e)

# ─────────────────────────────────────────────
# FEATURE ENGINEERING
# ─────────────────────────────────────────────
def categorize_bmi(bmi):
    if bmi < 20.0:   return 'Underweight'
    elif bmi < 25.0: return 'Normal weight'
    elif bmi < 30.0: return 'Overweight/Preobesity'
    elif bmi < 35.0: return 'Class I Obesity'
    elif bmi < 40.0: return 'Class II Obesity'
    else:            return 'Class III Obesity'

FEATURES_TO_DROP = ['AnyHealthcare', 'NoDocbcCost', 'Sex', 'BMI_Category_Normal weight']

def build_features(inputs):
    bmi   = inputs["BMI"]
    menth = inputs["MentHlth"]
    physh = inputs["PhysHlth"]
    genh  = inputs["GenHlth"]
    row = {
        "HighBP":               inputs["HighBP"],
        "HighChol":             inputs["HighChol"],
        "CholCheck":            1,
        "Smoker":               inputs["Smoker"],
        "Stroke":               inputs["Stroke"],
        "HeartDiseaseorAttack": inputs["HeartDiseaseorAttack"],
        "PhysActivity":         inputs["PhysActivity"],
        "Fruits":               1,
        "Veggies":              1,
        "HvyAlcoholConsump":    0,
        "AnyHealthcare":        1,
        "NoDocbcCost":          0,
        "DiffWalk":             inputs["DiffWalk"],
        "Sex":                  0,
        "GenHlth":              genh,
        "Age":                  inputs["Age"],
        "Education":            inputs["Education"],
        "Income":               inputs["Income"],
        "BMI_Category":         categorize_bmi(bmi),
        "MentHlth_log":         np.log1p(menth),
        "PhysHlth_log":         np.log1p(physh),
        "health_interaction":   menth * physh,
        "health_score":         (menth + physh) / (genh + 1),
        "Metabolic_Risk":       inputs["HighBP"] + inputs["HighChol"],
        "Lifestyle_Score":      inputs["PhysActivity"] + 1 + 1 - 0,
        "Comorbidity_Score":    inputs["Stroke"] + inputs["HeartDiseaseorAttack"] + inputs["DiffWalk"],
    }
    return pd.DataFrame([row])

def predict(inputs):
    # Compatibility patch for sklearn version differences
    import sklearn.compose._column_transformer as _ct
    if not hasattr(_ct, '_RemainderColsList'):
        class _RemainderColsList(list):
            pass
        _ct._RemainderColsList = _RemainderColsList

    df_raw  = build_features(inputs)
    df_proc = preprocessor.transform(df_raw)
    numerical_cols   = ['MentHlth_log', 'PhysHlth_log', 'GenHlth', 'health_interaction', 'health_score']
    cat_cols         = preprocessor.named_transformers_['cat'].get_feature_names_out(['BMI_Category']).tolist()
    passthrough_cols = [c for c in df_raw.columns if c not in numerical_cols + ['BMI_Category']]
    all_cols         = numerical_cols + cat_cols + passthrough_cols
    df_proc = pd.DataFrame(df_proc, columns=all_cols)
    to_drop = [f for f in FEATURES_TO_DROP if f in df_proc.columns]
    df_proc = df_proc.drop(columns=to_drop)
    df_proc = df_proc[feature_names]
    return float(model.predict_proba(df_proc)[0, 1])

def yn(q, t, key):
    val = st.radio(q, [t["yes"], t["no"]], horizontal=True, key=key)
    return 1 if val == t["yes"] else 0

def classify_risk(prob):
    if prob < 0.40: return "low"
    elif prob < 0.70: return "mod"
    else: return "high"

# ─────────────────────────────────────────────
# LANGUAGE TOGGLE (always shown)
# ─────────────────────────────────────────────
t = T[st.session_state.lang]

col_back, col_space, col_lang = st.columns([2, 6, 2])
with col_lang:
    if st.button(t["lang_btn"], key="lang_toggle"):
        st.session_state.lang = "ar" if st.session_state.lang == "en" else "en"
        st.rerun()

# ─────────────────────────────────────────────
# HOME PAGE
# ─────────────────────────────────────────────
def render_home():
    t = T[st.session_state.lang]
    st.markdown(f"""
    <div class="home-wrapper">
      <div class="home-bg"></div>
      <div class="home-content">
        <div class="home-title">🩺 {t['home_title']}</div>
        <div class="home-sub">{t['home_sub']}</div>
        <div class="home-disclaimer">{t['home_disclaimer']}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button(t["home_btn_assess"], key="go_assess"):
            st.session_state.page = "assess"
            st.rerun()
    with col2:
        if st.button(t["home_btn_guide"], key="go_guide"):
            st.session_state.page = "guide"
            st.rerun()

    st.markdown(f"<div style='text-align:center;color:#4b5563;font-size:0.75rem;margin-top:16px;'>{t['home_source']}</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ASSESSMENT PAGE
# ─────────────────────────────────────────────
def render_assessment():
    t = T[st.session_state.lang]

    if st.button(t["back_home"], key="back_from_assess"):
        st.session_state.page = "home"
        st.rerun()

    st.markdown(f"""
    <div class="app-header">
      <div class="app-title">🤖 {t['assess_title']}</div>
      <div class="app-subtitle">{t['assess_sub']}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="disclaimer-info">{t["disclaimer_main"]}</div>', unsafe_allow_html=True)

    if not model_loaded:
        st.error(f"Model files not found. Please place diabetes_model.pkl, preprocessor.pkl, feature_names.pkl, threshold.pkl in the same folder as app.py")
        return

    with st.form("risk_form"):

        # Demographics
        st.markdown(f'<div class="card-title">{t["sec_demo2"]}</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            age_idx = st.selectbox(t["q_age"], t["age_opts"])
            age_val = t["age_opts"].index(age_idx) + 1
        with col2:
            edu_idx = st.selectbox(t["q_edu"], t["edu_opts"])
            edu_val = t["edu_opts"].index(edu_idx) + 1
        inc_idx = st.selectbox(t["q_inc"], t["inc_opts"])
        inc_val = t["inc_opts"].index(inc_idx) + 1

        st.divider()

        # Body & BMI
        st.markdown(f'<div class="card-title">{t["sec_body"]}</div>', unsafe_allow_html=True)

        bmi_method = st.radio(t["sec_bmi_method"],
                              [t["bmi_calc"], t["bmi_enter"], t["bmi_cat"]],
                              horizontal=True, key="bmi_method")

        bmi_val = 25.0
        if bmi_method == t["bmi_calc"]:
            col1, col2 = st.columns(2)
            with col1:
                height_cm = st.number_input(t["bmi_height"], min_value=100, max_value=250, value=170)
            with col2:
                weight_kg = st.number_input(t["bmi_weight"], min_value=30, max_value=300, value=70)
            if height_cm > 0:
                h_m = height_cm / 100
                bmi_val = round(weight_kg / (h_m ** 2), 1)
                st.markdown(f'<div style="color:#a78bfa;font-weight:700;font-size:1.1rem;">📊 {t["bmi_result"]}: {bmi_val}</div>', unsafe_allow_html=True)

        elif bmi_method == t["bmi_enter"]:
            bmi_val = st.number_input(t["bmi_label"], min_value=10.0, max_value=80.0, value=25.0, step=0.1, help=t["bmi_hint"])

        else:  # select category
            cat_idx = st.selectbox(t["bmi_label"], t["bmi_cats"])
            bmi_val = t["bmi_cat_vals"][t["bmi_cats"].index(cat_idx)]

        col1, col2 = st.columns(2)
        with col1:
            gh_idx = st.selectbox(t["q_gh"], t["gh_opts2"])
            gh_val = t["gh_opts2"].index(gh_idx) + 1

        st.divider()

        # Medical Conditions
        st.markdown(f'<div class="card-title">{t["sec_conditions"]}</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            bp_v     = yn(t["q_bp"],    t, "bp")
            chol_v   = yn(t["q_chol"],  t, "chol")
        with col2:
            stroke_v = yn(t["q_stroke"], t, "stroke")
            heart_v  = yn(t["q_heart"],  t, "heart")
            walk_v   = yn(t["q_walk"],   t, "walk")

        st.divider()

        # Lifestyle
        st.markdown(f'<div class="card-title">{t["sec_lifestyle"]}</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            smoke_v = yn(t["q_smoke"], t, "smoke")
        with col2:
            phys_v  = yn(t["q_phys"],  t, "phys")

        st.divider()

        # Health Days
        st.markdown(f'<div class="card-title">{t["sec_days"]}</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            ment_v  = st.slider(t["q_ment"],  0, 30, 0)
        with col2:
            phys2_v = st.slider(t["q_phys2"], 0, 30, 0)

        submitted = st.form_submit_button(t["submit"])

    # Results
    if submitted:
        inputs = {
            "HighBP": bp_v, "HighChol": chol_v,
            "Smoker": smoke_v, "Stroke": stroke_v,
            "HeartDiseaseorAttack": heart_v,
            "PhysActivity": phys_v, "DiffWalk": walk_v,
            "GenHlth": gh_val, "Age": age_val,
            "Education": edu_val, "Income": inc_val,
            "BMI": bmi_val, "MentHlth": ment_v, "PhysHlth": phys2_v,
        }

        with st.spinner("⏳"):
            try:
                prob = predict(inputs)
            except Exception as e:
                st.error(f"Prediction error: {e}")
                return

        risk = classify_risk(prob)
        pct  = round(prob * 100, 1)
        risk_labels = {"low": t["low"], "mod": t["mod"], "high": t["high"]}
        risk_css    = {"low": "risk-low", "mod": "risk-mod", "high": "risk-high"}
        bar_css     = {"low": "prob-bar-low", "mod": "prob-bar-mod", "high": "prob-bar-high"}
        rec_key     = {"low": "rec_low", "mod": "rec_mod", "high": "rec_high"}

        st.markdown("---")
        st.markdown(f"### 📊 {t['result_title']}")

        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:16px;margin-bottom:16px;">
          <span style="color:#9ca3af;">{t['risk_label']}:</span>
          <span class="{risk_css[risk]}">{risk_labels[risk]}</span>
        </div>
        <div style="color:#9ca3af;font-size:0.9rem;margin-bottom:6px;">
          {t['prob_label']}: <strong style="color:#e0e0f0;">{pct}%</strong>
        </div>
        <div class="prob-bar-container">
          <div class="{bar_css[risk]}" style="width:{pct}%;"></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"### 💡 {t['rec_title']}")
        recs     = t[rec_key[risk]]
        rec_html = "".join([f'<div class="rec-item">{r}</div>' for r in recs])
        st.markdown(f'<div class="card">{rec_html}</div>', unsafe_allow_html=True)

        if st.button(t["nutrition_btn"], key="go_nutrition"):
            st.session_state.page = "guide"
            st.rerun()

        st.markdown(f'<div class="disclaimer">{t["disclaimer_main"]}</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# GUIDE PAGE
# ─────────────────────────────────────────────
def render_guide():
    t = T[st.session_state.lang]

    if st.button(t["back_home"], key="back_from_guide"):
        st.session_state.page = "home"
        st.rerun()

    st.markdown(f"""
    <div class="app-header">
      <div class="app-title">📚 {t['guide_title']}</div>
      <div class="app-subtitle">{t['guide_sub']}</div>
    </div>
    """, unsafe_allow_html=True)

    # 1. About
    with st.expander(t["g_about"]):
        st.markdown(t["about_text"])

    # 2. Type 1 vs Type 2
    with st.expander(t["g_diff"]):
        st.markdown(t["diff_intro"])
        headers = t["diff_headers"]
        rows    = t["diff_rows"]
        table_html = f"""
        <table class="compare-table">
          <tr>{"".join(f"<th>{h}</th>" for h in headers)}</tr>
          {"".join(f'<tr><td class="feature">{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>' for r in rows)}
        </table>
        """
        st.markdown(table_html, unsafe_allow_html=True)

    # 3. Same symptoms?
    with st.expander(t["g_symptoms_same"]):
        st.markdown(t["symptoms_same_text"])

    # 4. Symptoms
    with st.expander(t["g_symptoms"]):
        for s in t["symptoms_list"]:
            st.markdown(f"- {s}")

    # 5. Risk Factors
    with st.expander(t["g_risk"]):
        for r in t["risk_list"]:
            st.markdown(f"- {r}")

    # 6. Complications
    with st.expander(t["g_complications"]):
        for name, desc in t["complications_list"]:
            st.markdown(f"**{name}** — {desc}")

    # 7. Prevention
    with st.expander(t["g_prevention"]):
        for p in t["prevention_list"]:
            st.markdown(f"- {p}")

    # 8. WHO Stats
    with st.expander(t["g_stats"]):
        for stat, desc in t["stats_items"]:
            st.markdown(f"""
            <div style="display:flex;gap:16px;padding:10px 0;border-bottom:1px solid #2a2a4a;align-items:center;">
              <div style="color:#c084fc;font-size:1.2rem;font-weight:800;min-width:140px;">{stat}</div>
              <div style="color:#d1d5db;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    # 9. Lab Tests — Real Jordan Data
    with st.expander(t["g_lab"]):
        st.markdown(f'<div class="disclaimer-info">{t["lab_intro"]}</div>', unsafe_allow_html=True)
        st.markdown(f"#### {t['lab_rank_title']}")

        # Chart data
        lab_tests = t["lab_tests"]
        test_names = [lt["name"].split(" (")[0] for lt in lab_tests]
        gap_f = [float(lt["gap_f"].replace("+","").replace("%","")) for lt in lab_tests]
        gap_m = [float(lt["gap_m"].replace("+","").replace("%","")) for lt in lab_tests]

        chart_data = pd.DataFrame({
            t["lab_female"]: gap_f,
            t["lab_male"]: gap_m,
        }, index=test_names)
        st.bar_chart(chart_data, color=["#a855f7", "#2dd4bf"])
        st.caption("📊 " + ("Percentage point gap: Diabetic vs Non-Diabetic abnormal rates" if st.session_state.lang == "en" else "فرق النسبة المئوية: مرضى السكري مقابل غيرهم"))

        st.markdown("---")

        # Lab cards
        for lt in lab_tests:
            f_d  = lt["female_d"]
            f_nd = lt["female_nd"]
            m_d  = lt["male_d"]
            m_nd = lt["male_nd"]

            st.markdown(f"""
            <div class="lab-card">
              <div class="lab-name">{lt['rank']} — {lt['name']}</div>
              <div class="lab-desc">{lt['desc_en']}</div>
              <div style="font-size:0.8rem;color:#9ca3af;margin-bottom:6px;">
                {t['lab_female']}: {t['lab_diabetic']} <b style="color:#c084fc">{f_d}%</b> &nbsp;|&nbsp; {t['lab_nondiabetic']} <b>{f_nd}%</b> &nbsp;&nbsp; Gap: <b style="color:#c084fc">{lt['gap_f']}</b>
              </div>
              <div class="lab-bar-bg"><div class="lab-bar-f" style="width:{f_d}%;"></div></div>
              <div class="lab-bar-bg"><div class="lab-bar-f" style="width:{f_nd}%;opacity:0.4;"></div></div>
              <div style="font-size:0.8rem;color:#9ca3af;margin:6px 0;">
                {t['lab_male']}: {t['lab_diabetic']} <b style="color:#2dd4bf">{m_d}%</b> &nbsp;|&nbsp; {t['lab_nondiabetic']} <b>{m_nd}%</b> &nbsp;&nbsp; Gap: <b style="color:#2dd4bf">{lt['gap_m']}</b>
              </div>
              <div class="lab-bar-bg"><div class="lab-bar-m" style="width:{m_d}%;"></div></div>
              <div class="lab-bar-bg"><div class="lab-bar-m" style="width:{m_nd}%;opacity:0.4;"></div></div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"<div style='color:#6b7280;font-size:0.78rem;margin-top:8px;'>{t['lab_note']}</div>", unsafe_allow_html=True)

    # 10. Nutritional Recommendations
    with st.expander(t["g_nutrition"]):
        st.markdown(f'<div class="disclaimer-info">🔜 {t["nutrition_coming"]}</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ROUTER
# ─────────────────────────────────────────────
if st.session_state.page == "home":
    render_home()
elif st.session_state.page == "assess":
    render_assessment()
elif st.session_state.page == "guide":
    render_guide()
