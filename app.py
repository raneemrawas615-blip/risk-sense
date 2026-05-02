
Copy

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import base64
 
st.set_page_config(page_title="Risk Sense | ريسك سينس", page_icon="🩺", layout="centered")
 
if "lang"  not in st.session_state: st.session_state.lang  = "en"
if "page"  not in st.session_state: st.session_state.page  = "home"
 
# ── Background ────────────────────────────────
def _b64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None
 
_bg = _b64(os.path.join(os.path.dirname(__file__), "bg.png"))
BG  = f"url('data:image/png;base64,{_bg}')" if _bg else \
      "linear-gradient(135deg,#2d0066 0%,#0f0f1a 100%)"
 
# ── CSS ──────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&family=Inter:wght@400;600;700&display=swap');
 
*, body, html {{ box-sizing: border-box; }}
html, body, [class*="css"] {{
  background-color: #0f0f1a !important;
  color: #e0e0f0 !important;
  font-family: 'Inter','Cairo',sans-serif;
}}
.stApp {{ background-color: #0f0f1a !important; }}
 
/* HOME HERO */
.hero {{
  position: relative;
  min-height: 82vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 48px 24px 32px;
  border-radius: 20px;
  overflow: hidden;
  margin-bottom: 0;
}}
.hero-bg {{
  position: absolute; inset: 0; z-index: 0;
  background: {BG};
  background-size: cover;
  background-position: center;
  filter: blur(7px) brightness(0.38);
  transform: scale(1.08);
  border-radius: 20px;
}}
.hero-content {{
  position: relative; z-index: 1;
  width: 100%; max-width: 680px; margin: 0 auto;
}}
.hero-title {{
  font-size: 3.2rem; font-weight: 800; line-height: 1.1;
  background: linear-gradient(135deg, #c084fc 30%, #38bdf8 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  margin-bottom: 14px;
}}
.hero-sub {{
  color: #ffffff; font-size: 1.05rem; margin-bottom: 24px; font-weight: 500;
}}
.hero-disc {{
  background: rgba(124,58,237,0.18);
  border: 1px solid rgba(167,139,250,0.45);
  border-radius: 14px;
  padding: 14px 22px;
  font-size: 0.9rem;
  color: #e9d5ff;
  margin-bottom: 0;
  line-height: 1.6;
}}
.hero-source {{
  color: rgba(255,255,255,0.35);
  font-size: 0.75rem;
  margin-top: 12px;
}}
 
/* BUTTONS */
.stButton > button {{
  background: linear-gradient(135deg, #7c3aed, #2dd4bf) !important;
  color: #ffffff !important; border: none !important;
  border-radius: 12px !important; padding: 11px 28px !important;
  font-size: 1rem !important; font-weight: 700 !important;
  width: 100%; margin-top: 4px; letter-spacing: 0.02em;
  transition: opacity .2s;
}}
.stButton > button:hover {{ opacity: 0.88; }}
 
/* CARDS */
.card {{
  background: #1a1a2e; border: 1px solid #2a2a4a;
  border-radius: 16px; padding: 22px; margin-bottom: 18px;
}}
.card-title {{
  font-size: 1rem; font-weight: 700; color: #a78bfa;
  margin-bottom: 14px; padding-bottom: 8px;
  border-bottom: 1px solid #2a2a4a;
}}
 
/* PAGE HEADER */
.app-header {{ text-align: center; padding: 20px 16px 6px; }}
.app-title {{
  font-size: 1.85rem; font-weight: 800;
  background: linear-gradient(135deg, #a78bfa, #38bdf8);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}}
.app-subtitle {{ color: #6b7280; font-size: 0.82rem; margin-top: 4px; }}
 
/* DISCLAIMERS */
.disc-purple {{
  background: #1e1a2e; border-left: 4px solid #7c3aed;
  border-radius: 8px; padding: 12px 16px;
  font-size: 0.85rem; color: #9ca3af; margin: 12px 0;
}}
.disc-blue {{
  background: rgba(56,189,248,.08); border-left: 4px solid #38bdf8;
  border-radius: 8px; padding: 12px 16px;
  font-size: 0.85rem; color: #bae6fd; margin: 12px 0;
}}
 
/* RISK */
.risk-low  {{ background:#064e3b;color:#6ee7b7;border:1px solid #10b981;border-radius:12px;padding:6px 18px;font-weight:700; }}
.risk-mod  {{ background:#78350f;color:#fcd34d;border:1px solid #f59e0b;border-radius:12px;padding:6px 18px;font-weight:700; }}
.risk-high {{ background:#7f1d1d;color:#fca5a5;border:1px solid #ef4444;border-radius:12px;padding:6px 18px;font-weight:700; }}
.pbar-bg   {{ background:#2a2a4a;border-radius:12px;overflow:hidden;height:22px;margin:10px 0; }}
.pbar-low  {{ background:linear-gradient(90deg,#10b981,#34d399);height:100%;border-radius:12px; }}
.pbar-mod  {{ background:linear-gradient(90deg,#f59e0b,#fbbf24);height:100%;border-radius:12px; }}
.pbar-high {{ background:linear-gradient(90deg,#ef4444,#f87171);height:100%;border-radius:12px; }}
.rec-item  {{ display:flex;gap:10px;padding:10px 0;border-bottom:1px solid #2a2a4a;font-size:.95rem; }}
.rec-item:last-child {{ border-bottom:none; }}
 
/* COMPARE TABLE */
.ctable {{ width:100%;border-collapse:collapse;font-size:.88rem; }}
.ctable th {{ background:linear-gradient(135deg,#7c3aed,#2563eb);color:#fff;padding:10px 14px;text-align:right; }}
.ctable td {{ padding:10px 14px;border-bottom:1px solid #2a2a4a;color:#d1d5db; }}
.ctable tr:hover td {{ background:#1e1e35; }}
.ctable .feat {{ color:#a78bfa;font-weight:600; }}
 
/* LAB */
.lcard {{ background:#1a1a2e;border:1px solid #2a2a4a;border-radius:12px;padding:16px;margin-bottom:12px; }}
.lname {{ color:#c084fc;font-weight:700;font-size:1rem;margin-bottom:4px; }}
.ldesc {{ color:#9ca3af;font-size:.84rem;margin-bottom:10px; }}
.lbar  {{ background:#2a2a4a;border-radius:8px;overflow:hidden;height:15px;margin:4px 0; }}
.lbar-f {{ background:linear-gradient(90deg,#a855f7,#c084fc);height:100%;border-radius:8px; }}
.lbar-m {{ background:linear-gradient(90deg,#2dd4bf,#38bdf8);height:100%;border-radius:8px; }}
 
/* OVERRIDES */
.stRadio > label, .stSlider > label,
.stSelectbox > label, .stNumberInput > label {{ color:#c4b5fd !important;font-weight:600; }}
div[data-baseweb="select"] {{ background:#1a1a2e !important;border-color:#3a3a5a !important; }}
.stExpander {{ background:#1a1a2e !important;border:1px solid #2a2a4a !important;border-radius:12px !important; }}
[data-testid="stRadio"] div {{ color:#d1d5db !important; }}
</style>
""", unsafe_allow_html=True)
 
# ── Translations ──────────────────────────────
T = {
"en": {
  "lang_btn":"🌐 عربي","back":"← Home",
  "home_title":"Risk Sense","home_sub":"Diabetes Type 2 Risk Predictor",
  "home_disc":"💡 This tool does not provide a medical diagnosis. It helps you understand how your daily habits and health status may influence your risk of developing Type 2 Diabetes.",
  "btn_assess":"🤖 Smart Assessment","btn_guide":"📚 Diabetes Guide",
  "home_src":"Based on CDC BRFSS 2015 Health Indicators Dataset",
  "assess_title":"Smart Assessment","assess_sub":"Type 2 Diabetes Risk Predictor — Based on CDC BRFSS 2015",
  "disc_main":"💡 This tool does not replace a medical diagnosis. Results reflect lifestyle and health indicators that may influence Type 2 Diabetes risk.",
  "sec_demo":"👤 Personal Info","sec_body":"📏 Body & General Health",
  "bmi_q":"How would you like to enter your BMI?",
  "bmi_c":"Calculate for me (Height & Weight)","bmi_e":"Enter BMI directly","bmi_s":"Select my category",
  "bmi_h":"Height (cm)","bmi_w":"Weight (kg)","bmi_lbl":"BMI","bmi_hint":"BMI = weight(kg)/height(m)²",
  "bmi_res":"Your BMI",
  "bmi_cats":["Underweight (< 18.5)","Normal (18.5–24.9)","Overweight (25–29.9)","Class I Obesity (30–34.9)","Class II Obesity (35–39.9)","Class III Obesity (≥ 40)"],
  "bmi_vals":[17.0,22.0,27.0,32.0,37.0,45.0],
  "q_gh":"How would you rate your general health?","gh_opts":["Excellent","Very Good","Good","Fair","Poor"],
  "sec_cond":"❤️ Medical Conditions",
  "q_bp":"Do you suffer from high blood pressure (diagnosed by a doctor)?",
  "q_chol":"Do you suffer from high cholesterol (diagnosed by a doctor)?",
  "q_stroke":"Have you ever had a stroke?",
  "q_heart":"Do you have coronary heart disease or a history of heart attack?",
  "q_walk":"Do you have serious difficulty walking or climbing stairs?",
  "sec_life":"🏃 Lifestyle",
  "q_smoke":"Have you smoked at least 100 cigarettes in your lifetime?",
  "q_phys":"Did you engage in any physical activity in the past 30 days?",
  "sec_days":"📅 Health Days (Past 30 Days)",
  "q_ment":"Days mental health was NOT good (0–30)","q_phys2":"Days physical health was NOT good (0–30)",
  "q_age":"Age Group","q_edu":"Highest Education Level","q_inc":"Annual Household Income",
  "age_opts":["18–24","25–29","30–34","35–39","40–44","45–49","50–54","55–59","60–64","65–69","70–74","75–79","80+"],
  "edu_opts":["Never attended","Elementary","Some high school","High school graduate","Some college","College graduate"],
  "inc_opts":["< $10,000","$10,000–$14,999","$15,000–$19,999","$20,000–$24,999","$25,000–$34,999","$35,000–$49,999","$50,000–$74,999","$75,000+"],
  "yes":"Yes","no":"No","submit":"Get My Risk Assessment",
  "res_title":"Your Risk Assessment","risk_lbl":"Risk Level","prob_lbl":"Predicted Probability","rec_title":"Recommendations",
  "nut_btn":"🥗 Nutritional Recommendations",
  "low":"Low Risk","mod":"Moderate Risk","high":"High Risk",
  "rec_low":["✅ Great news! Your risk is low — keep your healthy habits.","🏃 Stay physically active — aim for 150 min/week.","🩺 Schedule regular annual check-ups.","💧 Stay hydrated and get quality sleep.","🥗 Continue eating fruits and vegetables daily."],
  "rec_mod":["⚠️ Moderate risk — take action now before it progresses.","🏃 Increase physical activity to at least 150 min/week.","🥗 Reduce refined carbs and sugary drinks.","📊 Monitor blood pressure and cholesterol regularly.","🩺 Consult your doctor for a blood glucose test.","😴 Prioritize sleep and stress management."],
  "rec_high":["🚨 High risk — please consult a doctor as soon as possible.","🩸 Request a fasting blood glucose test immediately.","💊 Discuss treatment or prevention options with your doctor.","🥗 Follow a diabetes-friendly diet: low sugar, high fiber.","🏃 Even a 30-min daily walk can significantly help.","📱 Consider monitoring your blood glucose regularly."],
  "guide_title":"Diabetes Guide","guide_sub":"Your Comprehensive Guide to Type 2 Diabetes",
  "g_about":"📖 What is Type 2 Diabetes?","g_diff":"🔄 Type 1 vs Type 2 — What's the Difference?",
  "g_same":"❓ Do They Share the Same Symptoms?","g_symp":"🤒 Symptoms of Type 2 Diabetes",
  "g_risk":"⚠️ Risk Factors","g_comp":"🫀 Complications","g_prev":"🛡️ Prevention",
  "g_stats":"🌍 Global Statistics (WHO)","g_lab":"🩸 Lab Tests & Diabetes — Real Data from Jordan",
  "g_nut":"🥗 Nutritional Recommendations","nut_soon":"Coming soon — data from a certified Jordanian nutrition center.",
  "about":"""Type 2 Diabetes is a chronic condition affecting how the body uses glucose (blood sugar). It occurs when the body doesn't produce enough insulin or cells don't respond properly to it — leading to high blood sugar levels.\n\nInsulin is a hormone produced by the pancreas allowing sugar to enter cells for energy. In Type 2 Diabetes, this system breaks down gradually — often due to lifestyle, genetics, or both.\n\n**Key fact:** Type 2 Diabetes is largely preventable and manageable through lifestyle changes.""",
  "diff_intro":"Although both types involve blood sugar problems, they differ significantly in cause, mechanism, and management:",
  "diff_h":["Feature","Type 1","Type 2"],
  "diff_r":[["Cause","Autoimmune — immune system attacks insulin-producing cells","Insulin resistance + insufficient insulin production"],["Typical Age","Children and young adults","Usually 40+ (increasingly younger)"],["Insulin","Always required","Sometimes; often managed with lifestyle/meds"],["Onset","Sudden, rapid","Gradual, often unnoticed for years"],["Prevention","Not preventable","Largely preventable"],["Weight","Usually normal/underweight","Often overweight/obese"],["% of cases","~5–10%","~90–95%"]],
  "same":"""**They share many common symptoms**, because both result in elevated blood sugar. However, Type 1 symptoms appear suddenly and severely, while Type 2 develops slowly and may go unnoticed for years.\n\n**Shared:** frequent urination, excessive thirst, fatigue, blurry vision, slow-healing wounds.\n\n**Key difference:** Type 1 may include rapid weight loss and fruity breath (ketoacidosis) — rare in Type 2.""",
  "symp_list":["🚽 Frequent urination, especially at night","💧 Excessive thirst","😴 Unusual fatigue and low energy","👁️ Blurry or changing vision","🩹 Slow-healing cuts or bruises","🦶 Tingling or numbness in hands/feet","⚖️ Unexplained weight changes","🍽️ Increased hunger even after eating","🦠 Frequent infections (skin, gum, urinary)"],
  "risk_list":["⚖️ Overweight or obesity (especially belly fat)","🛋️ Sedentary lifestyle","👨‍👩‍👧 Family history of Type 2 Diabetes","🩸 High blood pressure or cholesterol","🎂 Age over 40","🤰 History of gestational diabetes","😴 Poor sleep or chronic stress","🚬 Smoking"],
  "comp_list":[("❤️ Heart & Blood Vessels","Diabetes doubles the risk of cardiovascular disease and stroke."),("🫘 Kidneys","Diabetic nephropathy can lead to kidney failure and dialysis."),("👁️ Eyes","Diabetic retinopathy is a leading cause of blindness worldwide."),("🦶 Feet","Nerve damage and poor circulation can lead to severe foot complications."),("🧠 Nervous System","Neuropathy causes tingling, pain, and loss of sensation."),("🦷 Oral Health","Diabetes increases risk of gum disease and tooth loss.")],
  "prev_list":["🏃 150+ minutes of moderate physical activity per week","⚖️ Maintain healthy weight — losing 5–7% reduces risk significantly","🥗 Balanced diet rich in fiber, whole grains, vegetables","🚭 Avoid smoking and excessive alcohol","💤 Get 7–8 hours of quality sleep","📊 Regular screenings (blood sugar, cholesterol, blood pressure)","😌 Manage stress effectively"],
  "stats":[("830 million","People living with diabetes worldwide in 2022 (WHO)"),("200M → 830M","The number quadrupled from 1990 to 2022"),("> 50%","Of people with diabetes were not receiving treatment in 2022"),("#1 cause","Diabetes leads to blindness, kidney failure & limb amputation"),("90–95%","Of all diabetes cases are Type 2")],
  "lab_intro":"This analysis is based on real patient data from Smart Lab Jordan — over 10,000 patients. It shows abnormal lab results are significantly more common in diabetic patients.",
  "lab_rank":"🏆 Strength of Association with Diabetes",
  "lab_f":"🟣 Female","lab_m":"🩵 Male","lab_d":"Diabetic","lab_nd":"Non-Diabetic",
  "lab_note":"* % of patients with abnormal results. Data: Smart Lab Jordan, 10,067 patients.",
  "lab_cap":"Percentage point gap: Diabetic vs Non-Diabetic abnormal rates",
  "lab_tests":[
    {"name":"Triglycerides","rank":"#1 Strongest","desc":"Blood fats that rise when the body can't properly use insulin. Strongly linked to metabolic syndrome and Type 2 Diabetes.","fd":47.7,"fnd":25.3,"md":43.6,"mnd":34.5,"gf":"+22.4%","gm":"+9.1%"},
    {"name":"CRP","rank":"#2","desc":"A marker of inflammation. Elevated CRP indicates systemic inflammation, which plays a key role in insulin resistance.","fd":49.4,"fnd":34.0,"md":33.5,"mnd":25.4,"gf":"+15.3%","gm":"+8.1%"},
    {"name":"GGT","rank":"#3","desc":"A liver enzyme. Elevated GGT reflects liver stress — linked to fatty liver, which strongly precedes diabetes.","fd":17.8,"fnd":6.5,"md":14.7,"mnd":10.6,"gf":"+11.2%","gm":"+4.1%"},
    {"name":"Creatinine","rank":"#4","desc":"A kidney function marker. Elevated creatinine in diabetic patients reflects early kidney stress — a common complication.","fd":17.5,"fnd":7.8,"md":15.1,"mnd":8.0,"gf":"+9.7%","gm":"+7.1%"},
  ],
},
"ar": {
  "lang_btn":"🌐 English","back":"← الرئيسية",
  "home_title":"ريسك سينس","home_sub":"تنبؤ بخطر الإصابة بالسكري من النوع الثاني",
  "home_disc":"💡 هذه الأداة لا تُقدّم تشخيصاً طبياً. تساعدك على فهم تأثير عاداتك اليومية وحالتك الصحية على احتمالية إصابتك بالسكري من النوع الثاني.",
  "btn_assess":"🤖 التقييم الذكي","btn_guide":"📚 دليل السكري",
  "home_src":"مبني على بيانات CDC BRFSS 2015",
  "assess_title":"التقييم الذكي","assess_sub":"تنبؤ بخطر السكري من النوع الثاني — مبني على CDC BRFSS 2015",
  "disc_main":"💡 هذه الأداة لا تُغني عن التشخيص الطبي. النتائج تعكس مؤشرات نمط الحياة والصحة المرتبطة بخطر الإصابة بالسكري من النوع الثاني.",
  "sec_demo":"👤 المعلومات الشخصية","sec_body":"📏 الجسم والصحة العامة",
  "bmi_q":"كيف تريد إدخال مؤشر كتلة الجسم؟",
  "bmi_c":"احسب لي (الطول والوزن)","bmi_e":"أدخل الرقم مباشرة","bmi_s":"اختر فئتي",
  "bmi_h":"الطول (سم)","bmi_w":"الوزن (كغ)","bmi_lbl":"مؤشر كتلة الجسم","bmi_hint":"BMI = الوزن(كغ) ÷ الطول(م)²",
  "bmi_res":"مؤشر كتلة جسمك",
  "bmi_cats":["نحيف (< 18.5)","طبيعي (18.5–24.9)","زيادة وزن (25–29.9)","سمنة درجة أولى (30–34.9)","سمنة درجة ثانية (35–39.9)","سمنة مفرطة (≥ 40)"],
  "bmi_vals":[17.0,22.0,27.0,32.0,37.0,45.0],
  "q_gh":"كيف تقيّم صحتك العامة؟","gh_opts":["ممتاز","جيد جداً","جيد","مقبول","سيئ"],
  "sec_cond":"❤️ الحالات الطبية",
  "q_bp":"هل تعاني من ارتفاع ضغط الدم (تم تشخيصه من قِبل طبيب)؟",
  "q_chol":"هل تعاني من ارتفاع الكوليسترول (تم تشخيصه من قِبل طبيب)؟",
  "q_stroke":"هل سبق أن أُصبت بجلطة دماغية؟",
  "q_heart":"هل تعاني من مرض قلبي أو أصبت بنوبة قلبية من قبل؟",
  "q_walk":"هل تعاني من صعوبة شديدة في المشي أو صعود السلالم؟",
  "sec_life":"🏃 نمط الحياة",
  "q_smoke":"هل دخّنت 100 سيجارة أو أكثر في حياتك؟",
  "q_phys":"هل مارست أي نشاط بدني خلال الـ 30 يوماً الماضية؟",
  "sec_days":"📅 أيام الصحة (الـ 30 يوم الماضية)",
  "q_ment":"كم يوماً لم تكن صحتك النفسية جيدة؟ (0–30)","q_phys2":"كم يوماً لم تكن صحتك الجسدية جيدة؟ (0–30)",
  "q_age":"الفئة العمرية","q_edu":"أعلى مستوى تعليمي","q_inc":"إجمالي دخل الأسرة السنوي",
  "age_opts":["18–24","25–29","30–34","35–39","40–44","45–49","50–54","55–59","60–64","65–69","70–74","75–79","80+"],
  "edu_opts":["لم أذهب للمدرسة / روضة","ابتدائية","بعض سنوات الثانوية","ثانوية عامة","بعض سنوات الجامعة","تخرجت من الجامعة"],
  "inc_opts":["أقل من 10,000$","10,000–14,999$","15,000–19,999$","20,000–24,999$","25,000–34,999$","35,000–49,999$","50,000–74,999$","75,000$ أو أكثر"],
  "yes":"نعم","no":"لا","submit":"احصل على تقييم الخطر",
  "res_title":"نتيجة تقييمك","risk_lbl":"مستوى الخطر","prob_lbl":"الاحتمالية المتوقعة","rec_title":"التوصيات",
  "nut_btn":"🥗 التوصيات الغذائية",
  "low":"خطر منخفض","mod":"خطر متوسط","high":"خطر مرتفع",
  "rec_low":["✅ بشرى سارة! خطرك منخفض — استمر في عاداتك الصحية.","🏃 حافظ على النشاط البدني — 150 دقيقة أسبوعياً على الأقل.","🩺 أجرِ فحوصات صحية دورية سنوية.","💧 اشرب كمية كافية من الماء واحرص على النوم الجيد.","🥗 واصل تناول الفواكه والخضروات يومياً."],
  "rec_mod":["⚠️ خطر متوسط — ابدأ باتخاذ إجراءات الآن قبل أن يتطور.","🏃 زد نشاطك البدني إلى 150 دقيقة أسبوعياً على الأقل.","🥗 قلّل من الكربوهيدرات المكررة والمشروبات السكرية.","📊 راقب ضغط دمك ومستوى الكوليسترول بانتظام.","🩺 استشر طبيبك لإجراء فحص سكر الدم.","😴 اهتم بجودة نومك وإدارة مستوى التوتر."],
  "rec_high":["🚨 خطر مرتفع — يُرجى مراجعة الطبيب في أقرب وقت ممكن.","🩸 أجرِ فحص سكر الدم الصائم فوراً.","💊 ناقش خيارات العلاج أو الوقاية مع طبيبك.","🥗 اتبع نظاماً غذائياً: قليل السكر وغني بالألياف.","🏃 المشي 30 دقيقة يومياً يساعد بشكل ملحوظ.","📱 فكّر في متابعة مستوى الغلوكوز بانتظام."],
  "guide_title":"دليل السكري","guide_sub":"دليلك الشامل عن السكري من النوع الثاني",
  "g_about":"📖 ما هو السكري من النوع الثاني؟","g_diff":"🔄 النوع الأول مقابل النوع الثاني — ما الفرق؟",
  "g_same":"❓ هل أعراضهما واحدة؟","g_symp":"🤒 أعراض السكري من النوع الثاني",
  "g_risk":"⚠️ عوامل الخطر","g_comp":"🫀 المضاعفات","g_prev":"🛡️ الوقاية",
  "g_stats":"🌍 إحصائيات عالمية (منظمة الصحة العالمية)","g_lab":"🩸 تحاليل المختبر والسكري — بيانات حقيقية من الأردن",
  "g_nut":"🥗 التوصيات الغذائية","nut_soon":"قريباً — بيانات من مركز تغذوي أردني معتمد.",
  "about":"""السكري من النوع الثاني هو حالة مزمنة تؤثر على طريقة استخدام الجسم للجلوكوز (سكر الدم). يحدث إما لأن الجسم لا يُنتج كمية كافية من الأنسولين، أو لأن الخلايا لا تستجيب له بشكل صحيح — مما يُؤدي إلى ارتفاع مستوى السكر في الدم.\n\nالأنسولين هرمون يُنتجه البنكرياس يسمح للسكر بدخول الخلايا وتحويله إلى طاقة. في السكري من النوع الثاني، يتعطل هذا النظام تدريجياً.\n\n**حقيقة مهمة:** السكري من النوع الثاني يمكن الوقاية منه إلى حدٍّ بعيد.""",
  "diff_intro":"رغم أن كلا النوعين يتعلقان بمشاكل في سكر الدم، إلا أنهما يختلفان اختلافاً جوهرياً:",
  "diff_h":["الخاصية","النوع الأول","النوع الثاني"],
  "diff_r":[["السبب","مناعي ذاتي — الجهاز المناعي يهاجم خلايا البنكرياس","مقاومة الأنسولين + عدم كفاية إنتاجه"],["العمر الشائع","الأطفال والشباب في الغالب","عادةً فوق 40 سنة"],["الأنسولين","ضروري دائماً","أحياناً — يمكن الإدارة بالأدوية"],["بداية الأعراض","مفاجئة وحادة","تدريجية وقد لا تُلاحَظ لسنوات"],["الوقاية","لا يمكن الوقاية منه","يمكن الوقاية منه إلى حدٍّ بعيد"],["الوزن","عادةً طبيعي أو نحيف","غالباً مرتبط بزيادة الوزن"],["النسبة","٥–١٠٪","٩٠–٩٥٪"]],
  "same":"""**يتشاركان كثيراً من الأعراض**، لأن كلاهما يُفضي إلى ارتفاع سكر الدم. لكن أعراض النوع الأول تظهر فجأة وبحدة، بينما أعراض النوع الثاني تتطور ببطء.\n\n**الأعراض المشتركة:** كثرة التبول، العطش الشديد، التعب، تشوش الرؤية، وبطء التئام الجروح.\n\n**الفرق الرئيسي:** النوع الأول قد يُصاحبه فقدان وزن سريع ورائحة الفم الكيتونية — نادر في النوع الثاني.""",
  "symp_list":["🚽 كثرة التبول خاصةً في الليل","💧 عطش شديد ومفرط","😴 تعب وإرهاق غير معتاد","👁️ تشوش أو تغيّر في الرؤية","🩹 بطء التئام الجروح والكدمات","🦶 تنميل أو وخز في اليدين والقدمين","⚖️ تغيّرات غير مبررة في الوزن","🍽️ جوع مستمر حتى بعد الأكل","🦠 التهابات متكررة (جلد، لثة، مسالك بولية)"],
  "risk_list":["⚖️ زيادة الوزن أو السمنة (خاصةً الكرش)","🛋️ قلة الحركة ونمط الحياة الخامل","👨‍👩‍👧 تاريخ عائلي بالسكري من النوع الثاني","🩸 ارتفاع ضغط الدم أو الكوليسترول","🎂 العمر فوق 40 سنة","🤰 تاريخ من السكري الحملي","😴 قلة النوم أو التوتر المزمن","🚬 التدخين"],
  "comp_list":[("❤️ القلب والأوعية الدموية","السكري يضاعف خطر الإصابة بأمراض القلب والسكتة الدماغية."),("🫘 الكلى","اعتلال الكلى السكري قد يؤدي إلى الفشل الكلوي والديلزة."),("👁️ العيون","اعتلال الشبكية السكري من أبرز أسباب العمى في العالم."),("🦶 القدمان","تلف الأعصاب وضعف الدورة الدموية قد يُفضيان لمضاعفات خطيرة."),("🧠 الجهاز العصبي","الاعتلال العصبي يُسبب وخزاً وألماً وفقدان الإحساس."),("🦷 صحة الفم","السكري يزيد خطر التهابات اللثة وفقدان الأسنان.")],
  "prev_list":["🏃 150 دقيقة أسبوعياً من النشاط البدني المعتدل على الأقل","⚖️ الحفاظ على وزن صحي — فقدان 5–7٪ من الوزن يُقلل الخطر","🥗 نظام غذائي متوازن غني بالألياف والحبوب الكاملة والخضروات","🚭 تجنب التدخين والكحول","💤 النوم 7–8 ساعات يومياً بجودة جيدة","📊 الفحوصات الدورية (سكر الدم، الكوليسترول، ضغط الدم)","😌 إدارة التوتر بفعالية"],
  "stats":[("830 مليون","شخص يعيش مع السكري في 2022 (منظمة الصحة العالمية)"),("200 مليون ← 830 مليون","الرقم تضاعف أربع مرات منذ 1990 حتى 2022"),("أكثر من 50٪","من مرضى السكري لم يكونوا يتلقون العلاج في 2022"),("السبب الأول","السكري سبب رئيسي للعمى والفشل الكلوي وبتر الأطراف"),("90–95٪","من جميع حالات السكري هي من النوع الثاني")],
  "lab_intro":"هذا التحليل مبني على بيانات حقيقية من Smart Lab الأردن — أكثر من 10,000 مريض. يُظهر أن النتائج المخبرية غير الطبيعية أكثر شيوعاً بشكل ملحوظ عند مرضى السكري.",
  "lab_rank":"🏆 قوة الارتباط بالسكري",
  "lab_f":"🟣 إناث","lab_m":"🩵 ذكور","lab_d":"مرضى السكري","lab_nd":"غير مرضى السكري",
  "lab_note":"* نسبة المرضى الذين أظهرت نتائجهم قيماً غير طبيعية. البيانات: Smart Lab الأردن، 10,067 مريض.",
  "lab_cap":"فرق النسبة المئوية: مرضى السكري مقابل غيرهم",
  "lab_tests":[
    {"name":"Triglycerides (ثلاثي الغليسريد)","rank":"#1 الأقوى","desc":"دهون الدم التي ترتفع عندما لا يستطيع الجسم استخدام الأنسولين بشكل صحيح. مرتبطة بقوة بالسكري من النوع الثاني.","fd":47.7,"fnd":25.3,"md":43.6,"mnd":34.5,"gf":"+22.4%","gm":"+9.1%"},
    {"name":"CRP (بروتين سي التفاعلي)","rank":"#2","desc":"مؤشر الالتهاب. ارتفاعه يعني وجود التهاب منهجي يُقلل من حساسية الخلايا للأنسولين.","fd":49.4,"fnd":34.0,"md":33.5,"mnd":25.4,"gf":"+15.3%","gm":"+8.1%"},
    {"name":"GGT (غاما غلوتاميل)","rank":"#3","desc":"إنزيم الكبد. ارتفاعه يعكس ضغطاً على الكبد — مرتبط بالكبد الدهني الذي يسبق السكري غالباً.","fd":17.8,"fnd":6.5,"md":14.7,"mnd":10.6,"gf":"+11.2%","gm":"+4.1%"},
    {"name":"Creatinine (كرياتينين)","rank":"#4","desc":"مؤشر وظائف الكلى. ارتفاعه عند مرضى السكري يعكس بدايات تأثر الكلى — من أبرز مضاعفات المرض.","fd":17.5,"fnd":7.8,"md":15.1,"mnd":8.0,"gf":"+9.7%","gm":"+7.1%"},
  ],
},
}
 
# ── Model ─────────────────────────────────────
@st.cache_resource
def load_model():
    base = os.path.dirname(__file__)
    m  = joblib.load(os.path.join(base,"diabetes_model.pkl"))
    p  = joblib.load(os.path.join(base,"preprocessor.pkl"))
    fn = joblib.load(os.path.join(base,"feature_names.pkl"))
    th = joblib.load(os.path.join(base,"threshold.pkl"))
    return m, p, fn, th
 
try:
    model, preprocessor, feature_names, threshold = load_model()
    model_ok = True
except Exception as e:
    model_ok = False; _err = str(e)
 
def _bmi_cat(bmi):
    if bmi<20: return 'Underweight'
    elif bmi<25: return 'Normal weight'
    elif bmi<30: return 'Overweight/Preobesity'
    elif bmi<35: return 'Class I Obesity'
    elif bmi<40: return 'Class II Obesity'
    else: return 'Class III Obesity'
 
DROP = ['AnyHealthcare','NoDocbcCost','Sex','BMI_Category_Normal weight']
 
def predict(inp):
    import sklearn.compose._column_transformer as _ct
    if not hasattr(_ct,'_RemainderColsList'):
        class _RemainderColsList(list): pass
        _ct._RemainderColsList = _RemainderColsList
    bmi=inp["BMI"]; mh=inp["MentHlth"]; ph=inp["PhysHlth"]; gh=inp["GenHlth"]
    row={"HighBP":inp["HighBP"],"HighChol":inp["HighChol"],"CholCheck":1,
         "Smoker":inp["Smoker"],"Stroke":inp["Stroke"],"HeartDiseaseorAttack":inp["HeartDiseaseorAttack"],
         "PhysActivity":inp["PhysActivity"],"Fruits":1,"Veggies":1,"HvyAlcoholConsump":0,
         "AnyHealthcare":1,"NoDocbcCost":0,"DiffWalk":inp["DiffWalk"],"Sex":0,
         "GenHlth":gh,"Age":inp["Age"],"Education":inp["Education"],"Income":inp["Income"],
         "BMI_Category":_bmi_cat(bmi),"MentHlth_log":np.log1p(mh),"PhysHlth_log":np.log1p(ph),
         "health_interaction":mh*ph,"health_score":(mh+ph)/(gh+1),
         "Metabolic_Risk":inp["HighBP"]+inp["HighChol"],
         "Lifestyle_Score":inp["PhysActivity"]+1+1-0,
         "Comorbidity_Score":inp["Stroke"]+inp["HeartDiseaseorAttack"]+inp["DiffWalk"]}
    df=pd.DataFrame([row])
    proc=preprocessor.transform(df)
    nc=['MentHlth_log','PhysHlth_log','GenHlth','health_interaction','health_score']
    cc=preprocessor.named_transformers_['cat'].get_feature_names_out(['BMI_Category']).tolist()
    pc=[c for c in df.columns if c not in nc+['BMI_Category']]
    df2=pd.DataFrame(proc,columns=nc+cc+pc)
    df2=df2.drop(columns=[f for f in DROP if f in df2.columns])
    return float(model.predict_proba(df2[feature_names])[0,1])
 
def yn(q,t,k):
    return 1 if st.radio(q,[t["yes"],t["no"]],horizontal=True,key=k)==t["yes"] else 0
 
def risk_cls(p):
    return "low" if p<0.40 else ("mod" if p<0.70 else "high")
 
 
# ── HOME ──────────────────────────────────────
def render_home():
    t = T[st.session_state.lang]
    _, cl = st.columns([8,2])
    with cl:
        if st.button(t["lang_btn"], key="lang_h"):
            st.session_state.lang = "ar" if st.session_state.lang=="en" else "en"
            st.rerun()
    st.markdown(f"""
    <div class="hero">
      <div class="hero-bg"></div>
      <div class="hero-content">
        <div class="hero-title">🩺 {t['home_title']}</div>
        <div class="hero-sub">{t['home_sub']}</div>
        <div class="hero-disc">{t['home_disc']}</div>
        <div class="hero-source">{t['home_src']}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button(t["btn_assess"], key="ga"):
            st.session_state.page="assess"; st.rerun()
    with c2:
        if st.button(t["btn_guide"], key="gg"):
            st.session_state.page="guide"; st.rerun()
 
# ── ASSESS ────────────────────────────────────
def render_assess():
    t = T[st.session_state.lang]
    c_bk, _, c_lg = st.columns([2,6,2])
    with c_bk:
        if st.button(t["back"], key="bk_a2"): st.session_state.page="home"; st.rerun()
    with c_lg:
        if st.button(t["lang_btn"], key="lang_a"):
            st.session_state.lang = "ar" if st.session_state.lang=="en" else "en"
            st.rerun()
    if False: st.session_state.page="home"; st.rerun()
    st.markdown(f'<div class="app-header"><div class="app-title">🤖 {t["assess_title"]}</div><div class="app-subtitle">{t["assess_sub"]}</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="disc-blue">{t["disc_main"]}</div>', unsafe_allow_html=True)
    if not model_ok:
        st.error("Model files not found. Place diabetes_model.pkl, preprocessor.pkl, feature_names.pkl, threshold.pkl in the app folder.")
        return
    with st.form("rf"):
        st.markdown(f'<div class="card-title">{t["sec_demo"]}</div>', unsafe_allow_html=True)
        c1,c2=st.columns(2)
        with c1:
            ai=st.selectbox(t["q_age"],t["age_opts"]); av=t["age_opts"].index(ai)+1
        with c2:
            ei=st.selectbox(t["q_edu"],t["edu_opts"]); ev=t["edu_opts"].index(ei)+1
        ii=st.selectbox(t["q_inc"],t["inc_opts"]); iv=t["inc_opts"].index(ii)+1
        st.divider()
        st.markdown(f'<div class="card-title">{t["sec_body"]}</div>', unsafe_allow_html=True)
        bm=st.radio(t["bmi_q"],[t["bmi_c"],t["bmi_e"],t["bmi_s"]],horizontal=True,key="bm")
        bv=25.0
        if bm==t["bmi_c"]:
            c1,c2=st.columns(2)
            with c1: hh=st.number_input(t["bmi_h"],100,250,170)
            with c2: ww=st.number_input(t["bmi_w"],30,300,70)
            bv=round(ww/((hh/100)**2),1)
            st.markdown(f'<div style="color:#a78bfa;font-weight:700;">📊 {t["bmi_res"]}: {bv}</div>',unsafe_allow_html=True)
        elif bm==t["bmi_e"]:
            bv=st.number_input(t["bmi_lbl"],10.0,80.0,25.0,0.1,help=t["bmi_hint"])
        else:
            ci=st.selectbox(t["bmi_lbl"],t["bmi_cats"]); bv=t["bmi_vals"][t["bmi_cats"].index(ci)]
        c1,_=st.columns(2)
        with c1: gi=st.selectbox(t["q_gh"],t["gh_opts"]); gv=t["gh_opts"].index(gi)+1
        st.divider()
        st.markdown(f'<div class="card-title">{t["sec_cond"]}</div>', unsafe_allow_html=True)
        c1,c2=st.columns(2)
        with c1: bp=yn(t["q_bp"],t,"bp"); ch=yn(t["q_chol"],t,"ch")
        with c2: sk=yn(t["q_stroke"],t,"sk"); ht=yn(t["q_heart"],t,"ht"); wk=yn(t["q_walk"],t,"wk")
        st.divider()
        st.markdown(f'<div class="card-title">{t["sec_life"]}</div>', unsafe_allow_html=True)
        c1,c2=st.columns(2)
        with c1: sm=yn(t["q_smoke"],t,"sm")
        with c2: pa=yn(t["q_phys"],t,"pa")
        st.divider()
        st.markdown(f'<div class="card-title">{t["sec_days"]}</div>', unsafe_allow_html=True)
        c1,c2=st.columns(2)
        with c1: mh=st.slider(t["q_ment"],0,30,0)
        with c2: ph=st.slider(t["q_phys2"],0,30,0)
        sub=st.form_submit_button(t["submit"])
    if sub:
        inp={"HighBP":bp,"HighChol":ch,"Smoker":sm,"Stroke":sk,"HeartDiseaseorAttack":ht,
             "PhysActivity":pa,"DiffWalk":wk,"GenHlth":gv,"Age":av,"Education":ev,
             "Income":iv,"BMI":bv,"MentHlth":mh,"PhysHlth":ph}
        with st.spinner("⏳"):
            try: prob=predict(inp)
            except Exception as e: st.error(f"Error: {e}"); return
        r=risk_cls(prob); pct=round(prob*100,1)
        rl={"low":t["low"],"mod":t["mod"],"high":t["high"]}
        rc={"low":"risk-low","mod":"risk-mod","high":"risk-high"}
        bc={"low":"pbar-low","mod":"pbar-mod","high":"pbar-high"}
        st.markdown("---")
        st.markdown(f"### 📊 {t['res_title']}")
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:16px;margin-bottom:14px;">
          <span style="color:#9ca3af;">{t['risk_lbl']}:</span>
          <span class="{rc[r]}">{rl[r]}</span>
        </div>
        <div style="color:#9ca3af;font-size:.9rem;margin-bottom:6px;">{t['prob_lbl']}: <strong style="color:#fff">{pct}%</strong></div>
        <div class="pbar-bg"><div class="{bc[r]}" style="width:{pct}%"></div></div>
        """,unsafe_allow_html=True)
        st.markdown(f"### 💡 {t['rec_title']}")
        rk={"low":"rec_low","mod":"rec_mod","high":"rec_high"}
        html="".join([f'<div class="rec-item">{x}</div>' for x in t[rk[r]]])
        st.markdown(f'<div class="card">{html}</div>',unsafe_allow_html=True)
        if st.button(t["nut_btn"],key="gn"): st.session_state.page="guide"; st.rerun()
        st.markdown(f'<div class="disc-purple">{t["disc_main"]}</div>',unsafe_allow_html=True)
 
# ── GUIDE ─────────────────────────────────────
def render_guide():
    t = T[st.session_state.lang]
    c_bk, _, c_lg = st.columns([2,6,2])
    with c_bk:
        if st.button(t["back"], key="bk_g2"): st.session_state.page="home"; st.rerun()
    with c_lg:
        if st.button(t["lang_btn"], key="lang_g"):
            st.session_state.lang = "ar" if st.session_state.lang=="en" else "en"
            st.rerun()
    if False: st.session_state.page="home"; st.rerun()
    st.markdown(f'<div class="app-header"><div class="app-title">📚 {t["guide_title"]}</div><div class="app-subtitle">{t["guide_sub"]}</div></div>',unsafe_allow_html=True)
 
    with st.expander(t["g_about"]): st.markdown(t["about"])
 
    with st.expander(t["g_diff"]):
        st.markdown(t["diff_intro"])
        h=t["diff_h"]; rows=t["diff_r"]
        st.markdown(f'<table class="ctable"><tr>{"".join(f"<th>{x}</th>" for x in h)}</tr>{"".join(f"""<tr><td class="feat">{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>""" for r in rows)}</table>',unsafe_allow_html=True)
 
    with st.expander(t["g_same"]): st.markdown(t["same"])
 
    with st.expander(t["g_symp"]):
        for s in t["symp_list"]: st.markdown(f"- {s}")
 
    with st.expander(t["g_risk"]):
        for r in t["risk_list"]: st.markdown(f"- {r}")
 
    with st.expander(t["g_comp"]):
        for nm,dc in t["comp_list"]: st.markdown(f"**{nm}** — {dc}")
 
    with st.expander(t["g_prev"]):
        for p in t["prev_list"]: st.markdown(f"- {p}")
 
    with st.expander(t["g_stats"]):
        for stat,desc in t["stats"]:
            st.markdown(f'<div style="display:flex;gap:16px;padding:10px 0;border-bottom:1px solid #2a2a4a;align-items:center;"><div style="color:#c084fc;font-size:1.1rem;font-weight:800;min-width:150px;">{stat}</div><div style="color:#d1d5db;">{desc}</div></div>',unsafe_allow_html=True)
 
    with st.expander(t["g_lab"]):
        st.markdown(f'<div class="disc-blue">{t["lab_intro"]}</div>',unsafe_allow_html=True)
        st.markdown(f"#### {t['lab_rank']}")
        lts=t["lab_tests"]
        names=[x["name"].split(" (")[0] for x in lts]
        gf=[float(x["gf"].replace("+","").replace("%","")) for x in lts]
        gm=[float(x["gm"].replace("+","").replace("%","")) for x in lts]
        df=pd.DataFrame({t["lab_f"]:gf,t["lab_m"]:gm},index=names)
        st.bar_chart(df,color=["#a855f7","#2dd4bf"])
        st.caption(f"📊 {t['lab_cap']}")
        st.markdown("---")
        for x in lts:
            st.markdown(f"""
            <div class="lcard">
              <div class="lname">{x['rank']} — {x['name']}</div>
              <div class="ldesc">{x['desc']}</div>
              <div style="font-size:.8rem;color:#9ca3af;margin-bottom:4px;">
                {t['lab_f']}: {t['lab_d']} <b style="color:#c084fc">{x['fd']}%</b> | {t['lab_nd']} <b>{x['fnd']}%</b> — Gap: <b style="color:#c084fc">{x['gf']}</b>
              </div>
              <div class="lbar"><div class="lbar-f" style="width:{x['fd']}%"></div></div>
              <div class="lbar"><div class="lbar-f" style="width:{x['fnd']}%;opacity:.4"></div></div>
              <div style="font-size:.8rem;color:#9ca3af;margin:6px 0 4px;">
                {t['lab_m']}: {t['lab_d']} <b style="color:#2dd4bf">{x['md']}%</b> | {t['lab_nd']} <b>{x['mnd']}%</b> — Gap: <b style="color:#2dd4bf">{x['gm']}</b>
              </div>
              <div class="lbar"><div class="lbar-m" style="width:{x['md']}%"></div></div>
              <div class="lbar"><div class="lbar-m" style="width:{x['mnd']}%;opacity:.4"></div></div>
            </div>""",unsafe_allow_html=True)
        st.markdown(f"<div style='color:#6b7280;font-size:.78rem;margin-top:6px;'>{t['lab_note']}</div>",unsafe_allow_html=True)
 
    with st.expander(t["g_nut"]):
        st.markdown(f'<div class="disc-blue">🔜 {t["nut_soon"]}</div>',unsafe_allow_html=True)
 
# ── Router ────────────────────────────────────
p = st.session_state.page
if p=="home":   render_home()
elif p=="assess": render_assess()
elif p=="guide":  render_guide()
