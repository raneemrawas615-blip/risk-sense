import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

st.set_page_config(page_title="Risk Sense | ريسك سينس", page_icon="🩺", layout="centered")

if "lang"  not in st.session_state: st.session_state.lang  = "en"
if "page"  not in st.session_state: st.session_state.page  = "home"


BG = "url('https://raw.githubusercontent.com/raneemrawas615-blip/risk-sense/main/bg.png')"

st.markdown(f"""
<style>
*, body, html {{ box-sizing: border-box; }}
html, body, [class*="css"] {{ background-color: #0f0f1a !important; color: #ffffff !important; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif; }}
.stApp {{ background-color: #0a0414; background-image: {BG}; background-size: cover; background-position: center; background-repeat: no-repeat; background-attachment: fixed; }}
.stApp::after {{ content: ''; position: fixed; inset: 0; background: rgba(5,2,15,0.62); z-index: 0; pointer-events: none; }}
.block-container {{ position: relative; z-index: 1; }}

[data-baseweb="select"] > div, [data-baseweb="select"] > div > div {{ background-color: #1e0f4a !important; border: 1px solid #6d28d9 !important; border-radius: 10px !important; color: #ddd6fe !important; }}
[data-baseweb="select"] input, [data-baseweb="select"] span {{ color: #ddd6fe !important; }}
[data-baseweb="select"] svg path {{ fill: #a78bfa !important; }}
[role="listbox"], [data-baseweb="popover"] {{ background: #1e0f4a !important; border: 1px solid #6d28d9 !important; }}
[role="option"] {{ background: #1e0f4a !important; color: #ddd6fe !important; }}
[role="option"]:hover {{ background: #2d1b69 !important; }}

input[type="number"] {{ background: #1e0f4a !important; color: #ddd6fe !important; border: 1px solid #6d28d9 !important; border-radius: 10px !important; }}
[data-testid="stNumberInput"] button {{ background: #2d1b69 !important; color: #ddd6fe !important; border: none !important; }}
[data-testid="stNumberInput"] {{ background: #1e0f4a !important; border: 1px solid #6d28d9 !important; border-radius: 10px !important; }}

.hero {{ position: relative; min-height: 60vh; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 48px 24px 32px; border-radius: 20px; margin-bottom: 16px; }}
.hero-bg {{ position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: -1; background: {BG}; background-size: cover; background-position: center; background-repeat: no-repeat; filter: brightness(0.42); }}
.hero-content {{ position: relative; z-index: 1; width: 100%; max-width: 680px; margin: 0 auto; }}
.hero-title {{ font-size: 3.2rem; font-weight: 800; line-height: 1.1; background: linear-gradient(135deg, #c084fc 30%, #38bdf8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 14px; }}
.hero-sub {{ color: #ffffff; font-size: 1.05rem; margin-bottom: 24px; font-weight: 500; }}
.hero-disc {{ background: rgba(124,58,237,0.18); border: 1px solid rgba(167,139,250,0.45); border-radius: 14px; padding: 14px 22px; font-size: 0.9rem; color: #e9d5ff; margin-bottom: 16px; line-height: 1.6; }}
.hero-source {{ color: rgba(255,255,255,0.35); font-size: 0.75rem; margin-top: 12px; }}

.stButton > button {{ background: linear-gradient(135deg, #7c3aed, #2dd4bf) !important; color: #ffffff !important; border: none !important; border-radius: 12px !important; padding: 11px 28px !important; font-size: 1rem !important; font-weight: 700 !important; width: 100%; margin-top: 8px; letter-spacing: 0.02em; transition: opacity .2s; }}
.stButton > button:hover {{ opacity: 0.88; }}
[data-testid="stFormSubmitButton"] > button {{ background: linear-gradient(135deg, #7c3aed, #2dd4bf) !important; color: #ffffff !important; border: none !important; border-radius: 12px !important; padding: 11px 28px !important; font-size: 1rem !important; font-weight: 700 !important; width: 100%; margin-top: 8px; }}

.card {{ background: #1a1a2e; border: 1px solid #2a2a4a; border-radius: 16px; padding: 22px; margin-bottom: 18px; }}
.card-title {{ font-size: 1rem; font-weight: 700; color: #a78bfa; margin-bottom: 14px; padding-bottom: 8px; border-bottom: 1px solid #2a2a4a; }}
.app-header {{ text-align: center; padding: 20px 16px 6px; }}
.app-title {{ font-size: 1.85rem; font-weight: 800; background: linear-gradient(135deg, #a78bfa, #38bdf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
.app-subtitle {{ color: #9ca3af; font-size: 0.82rem; margin-top: 4px; }}
.disc-purple {{ background: #1e1a2e; border-left: 4px solid #7c3aed; border-radius: 8px; padding: 12px 16px; font-size: 0.85rem; color: #9ca3af; margin: 12px 0; }}
.disc-blue {{ background: rgba(56,189,248,.08); border-left: 4px solid #38bdf8; border-radius: 8px; padding: 12px 16px; font-size: 0.85rem; color: #bae6fd; margin: 12px 0; }}

.risk-low  {{ background:#064e3b;color:#6ee7b7;border:1px solid #10b981;border-radius:12px;padding:6px 18px;font-weight:700; }}
.risk-mod  {{ background:#78350f;color:#fcd34d;border:1px solid #f59e0b;border-radius:12px;padding:6px 18px;font-weight:700; }}
.risk-high {{ background:#7f1d1d;color:#fca5a5;border:1px solid #ef4444;border-radius:12px;padding:6px 18px;font-weight:700; }}
.pbar-bg   {{ background:#2a2a4a;border-radius:12px;overflow:hidden;height:22px;margin:10px 0; }}
.pbar-low  {{ background:linear-gradient(90deg,#10b981,#34d399);height:100%;border-radius:12px; }}
.pbar-mod  {{ background:linear-gradient(90deg,#f59e0b,#fbbf24);height:100%;border-radius:12px; }}
.pbar-high {{ background:linear-gradient(90deg,#ef4444,#f87171);height:100%;border-radius:12px; }}

.nut-section {{ background: #12102a; border: 1px solid #2a2a4a; border-radius: 14px; padding: 20px; margin: 12px 0; }}
.nut-title {{ color: #2dd4bf; font-weight: 700; font-size: 1rem; margin-bottom: 8px; }}
.nut-item {{ padding: 6px 0; border-bottom: 1px solid #1e1e3a; font-size: 0.9rem; color: #e0e0f0; }}
.nut-item:last-child {{ border-bottom: none; }}
.nut-cat {{ color: #a78bfa; font-weight: 600; font-size: 0.85rem; margin-top: 10px; margin-bottom: 4px; }}
.nut-note {{ background: rgba(45,212,191,0.08); border-left: 3px solid #2dd4bf; border-radius: 6px; padding: 10px 14px; font-size: 0.82rem; color: #99f6e4; margin-top: 12px; }}

.rec-item  {{ display:flex;gap:10px;padding:10px 0;border-bottom:1px solid #2a2a4a;font-size:.95rem; }}
.rec-item:last-child {{ border-bottom:none; }}
.ctable {{ width:100%;border-collapse:collapse;font-size:.88rem; }}
.ctable th {{ background:linear-gradient(135deg,#7c3aed,#2563eb);color:#fff;padding:10px 14px;text-align:right; }}
.ctable td {{ padding:10px 14px;border-bottom:1px solid #2a2a4a;border:1px solid #3a2a5a;color:#ffffff; }}
.ctable tr:hover td {{ background:#1e1e35; }}
.ctable .feat {{ color:#a78bfa;font-weight:600; }}
.lcard {{ background:#1a1a2e;border:1px solid #2a2a4a;border-radius:12px;padding:16px;margin-bottom:12px; }}
.lname {{ color:#c084fc;font-weight:700;font-size:1rem;margin-bottom:4px; }}
.ldesc {{ color:#d1d5db;font-size:.84rem;margin-bottom:10px; }}
.lbar  {{ background:#2a2a4a;border-radius:8px;overflow:hidden;height:15px;margin:4px 0; }}
.lbar-f {{ background:linear-gradient(90deg,#a855f7,#c084fc);height:100%;border-radius:8px; }}
.lbar-m {{ background:linear-gradient(90deg,#2dd4bf,#38bdf8);height:100%;border-radius:8px; }}

header[data-testid="stHeader"] {{ display: none !important; }}
footer {{ display: none !important; }}
#MainMenu {{ display: none !important; }}
.stDeployButton {{ display: none !important; }}
:root {{ --primary: #2dd4bf !important; }}
[data-baseweb="radio"] [data-checked="true"] div {{ background: #2dd4bf !important; border-color: #2dd4bf !important; }}
[data-baseweb="radio"] div:first-child {{ border-color: #2dd4bf !important; }}
[data-testid="stSlider"] div[role="slider"] {{ background: #2dd4bf !important; }}
[data-testid="stSlider"] > div > div > div {{ background: #2dd4bf !important; }}
.stRadio > label, .stSlider > label, .stSelectbox > label, .stNumberInput > label {{ color:#c4b5fd !important;font-weight:600; }}
.stExpander {{ background:#1a1a2e !important;border:1px solid #2a2a4a !important;border-radius:12px !important; }}
[data-testid="stRadio"] div {{ color:#ffffff !important; }}
p, li, span {{ color:#ffffff; }}
</style>
""", unsafe_allow_html=True)

# ── Nutritional Recommendations ───────────────
NUT = {
"ar": {
  "low": {
    "goal": "الهدف: الوقاية والحفاظ على نمط الحياة الصحي",
    "source": "إسلام جادالله — NutriPlus",
    "note": "هذه توصيات عامة، قد يختلف الاحتياج الغذائي من شخص لآخر حسب حالته الصحية. إذا كنت مصاباً بأمراض مزمنة يرجى مراجعة طبيب مختص.",
    "cats": [
      ("🌾 الكربوهيدرات والنشويات", "ركّز على البرغل والشعير والشوفان وخبز القمح الكامل. أدخل البقوليات (عدس، حمص، فول) 3-4 مرات أسبوعياً. قلّل من الخبز الأبيض والسكريات المكررة. لا تتناول النشويات وحدها — ادمجها مع بروتين وألياف."),
      ("🍗 البروتينات", "الأفضل: دجاج بدون جلد، سمك، بيض، لبن، لبنة، بقوليات. قلّل من اللحوم المصنعة (نقانق، مرتديلا). وزّع البروتين على 3 وجبات رئيسية."),
      ("🫒 الدهون والزيوت", "دهون صحية: زيت الزيتون، أفوكادو، مكسرات. تجنّب: المقالي، الدهون المتحولة، السمن الصناعي."),
      ("🥗 الخضار والفاكهة", "3 حصص خضار أو أكثر يومياً. 2-3 حصص فاكهة منخفضة المؤشر الجلايسمي (تفاح، كمثرى، فراولة). الفاكهة الكاملة أفضل من العصير."),
      ("🍬 الحلويات والسكريات", "اعتدال وليس حرماناً — لا تزيد عن مرة إلى مرتين بالأسبوع بكمية بسيطة. استبدل السكر بالستيفيا."),
      ("💧 المشروبات", "الماء هو الخيار الأول دائماً. تجنّب المشروبات المحلاة والعصائر المصنعة. الشاي والقهوة بدون سكر أو بكميات قليلة جداً."),
      ("🍽️ الوجبات اليومية", "5-6 وجبات صغيرة متفرقة يومياً. لا تتخطَّ الوجبات."),
    ]
  },
  "mod": {
    "goal": "الهدف: التعديل الغذائي المبكر وتصحيح العادات — توصيات للتدخل الوقائي",
    "source": "إسلام جادالله — NutriPlus",
    "note": "هذه توصيات عامة، قد يختلف الاحتياج الغذائي من شخص لآخر حسب حالته الصحية. إذا كنت مصاباً بأمراض مزمنة يرجى مراجعة طبيب مختص.",
    "cats": [
      ("🌾 الكربوهيدرات والنشويات", "ركّز على البرغل والشعير والشوفان والبقوليات. وزّع الكربوهيدرات على الوجبات — لا دفعة واحدة. تجنّب: خبز أبيض، معجنات، حلويات، مشروبات محلاة. لا تتناول كربوهيدرات وحدها — دائماً مع بروتين وألياف."),
      ("🍗 البروتينات", "الأفضل: دجاج بدون جلد، سمك، بيض، لبنة، بقوليات. لحم أحمر بكميات معقولة. تجنّب اللحوم المصنعة تماماً."),
      ("🫒 الدهون والزيوت", "زيت الزيتون هو الخيار الأول للطهي. مكسرات غير مملحة كوجبة خفيفة. تجنّب: السمن الصناعي، الدهون المتحولة. استبدل المقلي بالمشوي أو المسلوق."),
      ("🥗 الخضار والفاكهة", "4-5 حصص خضار يومياً. اجعل نصف الطبق خضار في كل وجبة رئيسية. فاكهة: تفاح، إجاص، فراولة — 1-2 حصة يومياً. قلّل: تمر، عنب، موز ناضج. الفاكهة الكاملة فقط — لا عصائر."),
      ("🍬 الحلويات والسكريات", "تجنّب السكر الأبيض والمشروبات الغازية والعصائر المصنعة. استخدم الستيفيا كبديل. حلويات المناسبات: حصص صغيرة ولا تكررها باستمرار."),
      ("💧 المشروبات", "ماء كافٍ طوال اليوم. تجنّب تماماً المشروبات الغازية والعصائر المصنعة. قهوة وشاي بدون سكر أو بكميات قليلة جداً."),
      ("🍽️ الوجبات اليومية", "5-6 وجبات صغيرة يومياً. لا تتخطَّ وجبة الإفطار. نصف الطبق خضار — ربع نشويات — ربع بروتين مع دهون صحية بكمية معتدلة."),
    ]
  },
  "high": {
    "goal": "الهدف: التدخل الغذائي الفوري — توصيات علاجية وقائية مكثفة",
    "source": "إسلام جادالله — NutriPlus",
    "note": "هذه توصيات عامة، قد يختلف الاحتياج الغذائي من شخص لآخر حسب حالته الصحية. إذا كنت مصاباً بأمراض مزمنة يرجى مراجعة طبيب مختص وأخصائي تغذية للحصول على استشارة مناسبة لك.",
    "cats": [
      ("🌾 الكربوهيدرات والنشويات", "مسموح بتحكم دقيق: برغل، شعير، شوفان، عدس، حمص، فول، قمح كامل. البقوليات يومياً. تجنّب: أرز قصير الحبة، خبز أبيض، معجنات، مشروبات محلاة، حلويات. لا تتناول كربوهيدرات وحدها أبداً — دائماً مع بروتين وألياف ودهون صحية."),
      ("🍗 البروتينات", "دجاج بدون جلد مسلوق/مشوي — لا مقلي. سمك 2-3 مرات أسبوعياً. بقوليات يومياً. تجنّب تماماً: اللحوم المصنعة والنقانق والمرتديلا. لحم أحمر: لا تتجاوز مرة بالأسبوع بكميات صغيرة بلا شحوم."),
      ("🫒 الدهون والزيوت", "زيت الزيتون: ملعقة كبيرة يومياً. 6-8 حبات مكسرات غير محمصة وغير مملحة. تجنّب تماماً: السمن الصناعي، الدهون المتحولة، المقالي. طريقة الطهي: شوي، سلق، بخار."),
      ("🥗 الخضار والفاكهة", "خضار غير نشوية بحرية واسعة: سبانخ، خيار، كوسا، خس، بروكلي. 4-5 حصص يومياً إلزامية. نصف الطبق خضار في كل وجبة. تقليل: بطاطا، ذرة، شمندر. فاكهة منخفضة السكر فقط: تفاح، كمثرى، فراولة — حصة إلى 2 يومياً. تجنّب: موز ناضج، عنب، تمر بكميات كبيرة، مانجا. لا عصائر فاكهة يومياً."),
      ("🍬 الحلويات والسكريات", "تجنّب: سكر مضاف، عسل، دبس، مشروبات غازية. في المناسبات: حصة صغيرة جداً وليس روتيناً يومياً. بديل: الستيفيا."),
      ("💧 المشروبات", "ماء كافٍ طوال اليوم — قبل وأثناء وبعد أي نشاط بدني. تجنّب تماماً: مشروبات غازية وعصائر مصنعة. الشاي والقهوة بدون سكر تماماً أو مع الستيفيا."),
      ("🍽️ نموذج الطبق الغذائي", "نصف الطبق: خضار غير نشوية. ربع الطبق: بروتين خالٍ من الدهون (دجاج/سمك/بقوليات). ربع الطبق: نشويات عالية الألياف (برغل/شعير/قمح كامل). 5-6 وجبات يومياً — الإفطار إلزامي."),
    ]
  }
},
"en": {
  "low": {
    "goal": "Goal: Prevention & maintaining a healthy lifestyle",
    "source": "Islam Jadallah — NutriPlus",
    "note": "These are general recommendations. Nutritional needs vary by individual health status. Consult a specialist if you have chronic conditions.",
    "cats": [
      ("🌾 Carbohydrates & Starches", "Focus on complex carbs: bulgur, barley, oats, whole wheat bread. Include legumes (lentils, chickpeas, fava beans) 3-4 times/week. Reduce white bread and refined sugars. Always combine starches with protein and fiber."),
      ("🍗 Proteins", "Best: skinless chicken, fish, eggs, yogurt, labneh, legumes. Moderate: lean red meat. Reduce: processed meats (sausages, luncheon meat)."),
      ("🫒 Fats & Oils", "Healthy fats: olive oil, avocado, nuts. Avoid: fried foods, trans fats, artificial ghee."),
      ("🥗 Vegetables & Fruits", "3+ servings of vegetables daily. 2-3 servings of low-GI fruits (apple, pear, strawberry). Whole fruit is better than juice."),
      ("🍬 Sweets & Sugars", "Moderation, not deprivation — max 1-2 times per week in small amounts. Use stevia as a substitute."),
      ("💧 Beverages", "Water is always the first choice. Avoid sweetened drinks and packaged juices. Tea and coffee without sugar or very little."),
      ("🍽️ Daily Meals", "5-6 small meals spread throughout the day. Never skip meals."),
    ]
  },
  "mod": {
    "goal": "Goal: Early dietary modification & correcting habits — preventive intervention",
    "source": "Islam Jadallah — NutriPlus",
    "note": "These are general recommendations. Nutritional needs vary by individual health status. Consult a specialist if you have chronic conditions.",
    "cats": [
      ("🌾 Carbohydrates & Starches", "Focus on bulgur, barley, oats, and legumes. Distribute carbs across meals — not all at once. Avoid: white bread, pastries, sweets, sweetened drinks. Never eat carbs alone — always with protein and fiber."),
      ("🍗 Proteins", "Best: skinless chicken, fish, eggs, labneh, legumes. Moderate red meat. Avoid processed meats entirely."),
      ("🫒 Fats & Oils", "Olive oil is the first choice for cooking. Unsalted nuts as a healthy snack. Avoid: artificial ghee, trans fats. Replace fried food with grilled or boiled."),
      ("🥗 Vegetables & Fruits", "4-5 servings of vegetables daily. Make half your plate vegetables at each main meal. Fruits: apple, pear, strawberry — 1-2 servings daily. Reduce: dates, grapes, ripe banana. Whole fruit only — no juices."),
      ("🍬 Sweets & Sugars", "Avoid white sugar, carbonated drinks, packaged juices. Use stevia. Occasional sweets at events: small portions, not regularly."),
      ("💧 Beverages", "Sufficient water throughout the day. Completely avoid carbonated drinks and packaged juices. Coffee without sugar or very little."),
      ("🍽️ Daily Meals", "5-6 small meals daily. Never skip breakfast. Half plate vegetables — quarter starches — quarter protein with moderate healthy fats."),
    ]
  },
  "high": {
    "goal": "Goal: Immediate dietary intervention — intensive therapeutic & preventive recommendations",
    "source": "Islam Jadallah — NutriPlus",
    "note": "These are general recommendations. Nutritional needs vary by individual health status. Please consult a specialist and a dietitian for a personalized plan.",
    "cats": [
      ("🌾 Carbohydrates & Starches", "Allowed with precise control: bulgur, barley, oats, lentils, chickpeas, whole wheat. Legumes daily. Avoid: short-grain rice, white bread, pastries, sweetened drinks, sweets. Never eat carbs alone — always with protein, fiber and healthy fats."),
      ("🍗 Proteins", "Skinless chicken, boiled/grilled — no fried. Fish 2-3 times/week. Legumes daily. Completely avoid: processed meats, sausages. Red meat: max once/week in small lean portions."),
      ("🫒 Fats & Oils", "Olive oil: 1 tablespoon daily. 6-8 unsalted, unroasted nuts. Completely avoid: artificial ghee, trans fats, frying. Cooking method: grill, boil, steam."),
      ("🥗 Vegetables & Fruits", "Non-starchy vegetables freely: spinach, cucumber, zucchini, lettuce, broccoli. 4-5 servings daily — mandatory. Half your plate vegetables at every meal. Reduce: potatoes, corn, beets. Low-sugar fruits only: apple, pear, strawberry — 1-2 daily. Avoid: ripe banana, grapes, large amounts of dates, mango. No daily fruit juices."),
      ("🍬 Sweets & Sugars", "Avoid: added sugar, honey, molasses, carbonated drinks. At events: very small portion — not a daily routine. Alternative: stevia."),
      ("💧 Beverages", "Sufficient water throughout the day — before, during and after physical activity. Completely avoid: carbonated drinks and packaged juices. Tea and coffee completely without sugar or with stevia."),
      ("🍽️ Meal Plate Model", "Half plate: non-starchy vegetables. Quarter plate: lean protein (chicken/fish/legumes). Quarter plate: high-fiber starches (bulgur/barley/whole wheat). 5-6 meals daily — breakfast is mandatory."),
    ]
  }
}
}

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
  "bmi_h":"Height (cm)","bmi_w":"Weight (kg)","bmi_res":"Your BMI",
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
  "res_title":"Your Risk Assessment","risk_lbl":"Risk Level","prob_lbl":"Predicted Probability","rec_title":"Key Recommendations",
  "nut_title":"🥗 Nutritional Recommendations",
  "nut_src":"Source","nut_note_lbl":"💙 Note",
  "jordan_title":"🇯🇴 Jordanian Community Notes",
  "jordan_items":[
    ("🍵 Common dietary issues in Jordan linked to diabetes","Excessive sweetened tea — very common in Jordanian culture. Over-reliance on white rice and white bread. Low legume consumption despite availability. Easy access to fast food and sweets via delivery apps. Excessive animal fats and ghee in cooking. Large portions of traditional sweets at events. Few vegetables in main meals."),
    ("🕌 Ramadan, events & hospitality","Iftar: start with 1-2 dates + water + homemade soup, wait 10 min before main meal. Half plate vegetables, quarter starches, quarter protein. Avoid excessive Ramadan sweets (qatayef, awameh). Mansaf: small portions of lean meat, reduce jameed sauce. Hospitality: small amounts of sweets at events is okay — in moderation."),
    ("🏃 Physical activity & nutrition","150 minutes/week of moderate activity (walking, swimming, cycling) reduces risk significantly. Resistance training 2-3 times/week improves insulin sensitivity. Reduce prolonged sitting — walking after meals lowers blood sugar spikes. Monitor blood sugar before and after exercise, especially at high risk."),
  ],
  "low":"Low Risk","mod":"Moderate Risk","high":"High Risk",
  "rec_low":["✅ Your risk is low — keep your healthy habits.","🏃 Stay active — aim for 150 min/week.","🩺 Schedule regular annual check-ups.","💧 Stay hydrated and get quality sleep."],
  "rec_mod":["⚠️ Moderate risk — take action now.","🏃 Increase physical activity to 150 min/week.","📊 Monitor blood pressure and cholesterol.","🩺 Consult your doctor for a blood glucose test."],
  "rec_high":["🚨 High risk — please consult a doctor soon.","🩸 Request a fasting blood glucose test immediately.","💊 Discuss treatment options with your doctor.","🏃 Even 30 min daily walk can significantly help."],
  "guide_title":"Diabetes Guide","guide_sub":"Your Comprehensive Guide to Type 2 Diabetes",
  "g_about":"📖 What is Type 2 Diabetes?","g_diff":"🔄 Type 1 vs Type 2 — What's the Difference?",
  "g_same":"❓ Do They Share the Same Symptoms?","g_symp":"🤒 Symptoms of Type 2 Diabetes",
  "g_risk":"⚠️ Risk Factors","g_comp":"🫀 Complications","g_prev":"🛡️ Prevention",
  "g_stats":"🌍 Global Statistics (WHO)","g_lab":"🩸 Lab Tests & Diabetes — Real Data from Jordan",
  "g_nut":"🥗 Nutritional Recommendations",
  "about":"""Type 2 Diabetes is a chronic condition affecting how the body uses glucose (blood sugar). It occurs when the body doesn't produce enough insulin or cells don't respond properly to it — leading to high blood sugar levels.\n\nInsulin is a hormone produced by the pancreas allowing sugar to enter cells for energy. In Type 2 Diabetes, this system breaks down gradually — often due to lifestyle, genetics, or both.\n\n**Key fact:** Type 2 Diabetes is largely preventable and manageable through lifestyle changes.""",
  "diff_intro":"Although both types involve blood sugar problems, they differ significantly in cause, mechanism, and management:",
  "diff_h":["Feature","Type 1","Type 2"],
  "diff_r":[["Cause","Autoimmune — immune attacks insulin-producing cells","Insulin resistance + insufficient production"],["Typical Age","Children & young adults","Usually 40+ (increasingly younger)"],["Insulin","Always required","Sometimes; often managed with lifestyle/meds"],["Onset","Sudden, rapid","Gradual, often unnoticed for years"],["Prevention","Not preventable","Largely preventable"],["Weight","Usually normal/underweight","Often overweight/obese"],["% of cases","~5–10%","~90–95%"]],
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
  "bmi_h":"الطول (سم)","bmi_w":"الوزن (كغ)","bmi_res":"مؤشر كتلة جسمك",
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
  "res_title":"نتيجة تقييمك","risk_lbl":"مستوى الخطر","prob_lbl":"الاحتمالية المتوقعة","rec_title":"التوصيات الرئيسية",
  "nut_title":"🥗 التوصيات الغذائية",
  "nut_src":"المصدر","nut_note_lbl":"💙 ملاحظة",
  "jordan_title":"🇯🇴 ملاحظات خاصة بالمجتمع الأردني",
  "jordan_items":[
    ("🍵 أبرز المشكلات الغذائية الشائعة في المجتمع الأردني","الإفراط في الشاي المحلى بالسكر — شائع جداً في الثقافة الأردنية. الإفراط في تناول الأرز الأبيض والخبز الأبيض. قلة البقوليات رغم توافرها. سهولة توافر الأكل الجاهز والحلويات عبر تطبيقات الهاتف. الإفراط في الدهون الحيوانية والسمن في الطهي. تناول الحلويات التقليدية بكميات كبيرة في المناسبات. قلة الخضار في الوجبات الرئيسية."),
    ("🕌 رمضان والمناسبات والضيافة","الإفطار: على تمرة أو اثنتين + ماء + شوربة منزلية، ثم انتظار 10 دقائق قبل الوجبة الرئيسية. نصف الطبق خضار وربعه نشويات وربعه بروتين. تجنب الإفراط في حلويات رمضان (قطايف، عوامة). المنسف: كميات صغيرة من اللحم بلا شحوم مع تقليل الجميد. الضيافة: يمكن تناول كميات صغيرة من الحلويات في المناسبات مع الاعتدال."),
    ("🏃 دور النشاط البدني مع التغذية","150 دقيقة أسبوعياً من النشاط المعتدل (مشي، سباحة، ركوب دراجة) يُقلل الخطر بشكل ملحوظ. تمارين مقاومة 2-3 مرات أسبوعياً تُحسّن حساسية الأنسولين. تقليل الجلوس الطويل — المشي بعد الوجبات يُقلل ارتفاع السكر. مراقبة السكر قبل وبعد التمرين خصوصاً في مرحلة الخطر المرتفع."),
  ],
  "low":"خطر منخفض","mod":"خطر متوسط","high":"خطر مرتفع",
  "rec_low":["✅ خطرك منخفض — استمر في عاداتك الصحية.","🏃 حافظ على النشاط البدني — 150 دقيقة أسبوعياً.","🩺 أجرِ فحوصات صحية دورية سنوية.","💧 اشرب كمية كافية من الماء واحرص على النوم الجيد."],
  "rec_mod":["⚠️ خطر متوسط — ابدأ باتخاذ إجراءات الآن.","🏃 زد نشاطك البدني إلى 150 دقيقة أسبوعياً.","📊 راقب ضغط دمك ومستوى الكوليسترول.","🩺 استشر طبيبك لإجراء فحص سكر الدم."],
  "rec_high":["🚨 خطر مرتفع — يُرجى مراجعة الطبيب في أقرب وقت.","🩸 أجرِ فحص سكر الدم الصائم فوراً.","💊 ناقش خيارات العلاج مع طبيبك.","🏃 المشي 30 دقيقة يومياً يساعد بشكل ملحوظ."],
  "guide_title":"دليل السكري","guide_sub":"دليلك الشامل عن السكري من النوع الثاني",
  "g_about":"📖 ما هو السكري من النوع الثاني؟","g_diff":"🔄 النوع الأول مقابل النوع الثاني — ما الفرق؟",
  "g_same":"❓ هل أعراضهما واحدة؟","g_symp":"🤒 أعراض السكري من النوع الثاني",
  "g_risk":"⚠️ عوامل الخطر","g_comp":"🫀 المضاعفات","g_prev":"🛡️ الوقاية",
  "g_stats":"🌍 إحصائيات عالمية (منظمة الصحة العالمية)","g_lab":"🩸 تحاليل المختبر والسكري — بيانات حقيقية من الأردن",
  "g_nut":"🥗 التوصيات الغذائية",
  "about":"""السكري من النوع الثاني هو حالة مزمنة تؤثر على طريقة استخدام الجسم للجلوكوز. يحدث إما لأن الجسم لا يُنتج كمية كافية من الأنسولين، أو لأن الخلايا لا تستجيب له بشكل صحيح.\n\nالأنسولين هرمون يُنتجه البنكرياس يسمح للسكر بدخول الخلايا وتحويله إلى طاقة. في السكري من النوع الثاني، يتعطل هذا النظام تدريجياً.\n\n**حقيقة مهمة:** السكري من النوع الثاني يمكن الوقاية منه إلى حدٍّ بعيد.""",
  "diff_intro":"رغم أن كلا النوعين يتعلقان بمشاكل في سكر الدم، إلا أنهما يختلفان اختلافاً جوهرياً:",
  "diff_h":["الخاصية","النوع الأول","النوع الثاني"],
  "diff_r":[["السبب","مناعي ذاتي — الجهاز المناعي يهاجم خلايا البنكرياس","مقاومة الأنسولين + عدم كفاية إنتاجه"],["العمر الشائع","الأطفال والشباب في الغالب","عادةً فوق 40 سنة"],["الأنسولين","ضروري دائماً","أحياناً — يمكن الإدارة بالأدوية"],["بداية الأعراض","مفاجئة وحادة","تدريجية وقد لا تُلاحَظ لسنوات"],["الوقاية","لا يمكن الوقاية منه","يمكن الوقاية منه إلى حدٍّ بعيد"],["الوزن","عادةً طبيعي أو نحيف","غالباً مرتبط بزيادة الوزن"],["النسبة","٥–١٠٪","٩٠–٩٥٪"]],
  "same":"""**يتشاركان كثيراً من الأعراض**، لأن كلاهما يُفضي إلى ارتفاع سكر الدم. لكن أعراض النوع الأول تظهر فجأة وبحدة، بينما أعراض النوع الثاني تتطور ببطء.\n\n**الأعراض المشتركة:** كثرة التبول، العطش الشديد، التعب، تشوش الرؤية، وبطء التئام الجروح.\n\n**الفرق الرئيسي:** النوع الأول قد يُصاحبه فقدان وزن سريع ورائحة الفم الكيتونية — نادر في النوع الثاني.""",
  "symp_list":["🚽 كثرة التبول خاصةً في الليل","💧 عطش شديد ومفرط","😴 تعب وإرهاق غير معتاد","👁️ تشوش أو تغيّر في الرؤية","🩹 بطء التئام الجروح والكدمات","🦶 تنميل أو وخز في اليدين والقدمين","⚖️ تغيّرات غير مبررة في الوزن","🍽️ جوع مستمر حتى بعد الأكل","🦠 التهابات متكررة (جلد، لثة، مسالك بولية)"],
  "risk_list":["⚖️ زيادة الوزن أو السمنة (خاصةً الكرش)","🛋️ قلة الحركة ونمط الحياة الخامل","👨‍👩‍👧 تاريخ عائلي بالسكري من النوع الثاني","🩸 ارتفاع ضغط الدم أو الكوليسترول","🎂 العمر فوق 40 سنة","🤰 تاريخ من السكري الحملي","😴 قلة النوم أو التوتر المزمن","🚬 التدخين"],
  "comp_list":[("❤️ القلب والأوعية الدموية","السكري يضاعف خطر الإصابة بأمراض القلب والسكتة الدماغية."),("🫘 الكلى","اعتلال الكلى السكري قد يؤدي إلى الفشل الكلوي والديلزة."),("👁️ العيون","اعتلال الشبكية السكري من أبرز أسباب العمى في العالم."),("🦶 القدمان","تلف الأعصاب وضعف الدورة الدموية قد يُفضيان لمضاعفات خطيرة."),("🧠 الجهاز العصبي","الاعتلال العصبي يُسبب وخزاً وألماً وفقدان الإحساس."),("🦷 صحة الفم","السكري يزيد خطر التهابات اللثة وفقدان الأسنان.")],
  "prev_list":["🏃 150 دقيقة أسبوعياً من النشاط البدني المعتدل على الأقل","⚖️ الحفاظ على وزن صحي — فقدان 5–7٪ من الوزن يُقلل الخطر","🥗 نظام غذائي متوازن غني بالألياف والحبوب الكاملة والخضروات","🚭 تجنب التدخين والكحول","💤 النوم 7–8 ساعات يومياً بجودة جيدة","📊 الفحوصات الدورية (سكر الدم، الكوليسترول، ضغط الدم)","😌 إدارة التوتر بفعالية"],
  "stats":[("830 مليون","شخص يعيش مع السكري في 2022 (منظمة الصحة العالمية)"),("200 مليون ← 830 مليون","الرقم تضاعف أربع مرات منذ 1990 حتى 2022"),("أكثر من 50٪","من مرضى السكري لم يكونوا يتلقون العلاج في 2022"),("السبب الأول","السكري سبب رئيسي للعمى والفشل الكلوي وبتر الأطراف"),("90–95٪","من جميع حالات السكري هي من النوع الثاني")],
  "lab_intro":"هذا التحليل مبني على بيانات حقيقية من Smart Lab الأردن — أكثر من 10,000 مريض.",
  "lab_rank":"🏆 قوة الارتباط بالسكري",
  "lab_f":"🟣 إناث","lab_m":"🩵 ذكور","lab_d":"مرضى السكري","lab_nd":"غير مرضى السكري",
  "lab_note":"* نسبة المرضى الذين أظهرت نتائجهم قيماً غير طبيعية. البيانات: Smart Lab الأردن، 10,067 مريض.",
  "lab_cap":"فرق النسبة المئوية: مرضى السكري مقابل غيرهم",
  "lab_tests":[
    {"name":"Triglycerides (ثلاثي الغليسريد)","rank":"#1 الأقوى","desc":"دهون الدم التي ترتفع عندما لا يستطيع الجسم استخدام الأنسولين بشكل صحيح.","fd":47.7,"fnd":25.3,"md":43.6,"mnd":34.5,"gf":"+22.4%","gm":"+9.1%"},
    {"name":"CRP (بروتين سي التفاعلي)","rank":"#2","desc":"مؤشر الالتهاب. ارتفاعه يعني وجود التهاب منهجي يُقلل من حساسية الخلايا للأنسولين.","fd":49.4,"fnd":34.0,"md":33.5,"mnd":25.4,"gf":"+15.3%","gm":"+8.1%"},
    {"name":"GGT (غاما غلوتاميل)","rank":"#3","desc":"إنزيم الكبد. ارتفاعه يعكس ضغطاً على الكبد — مرتبط بالكبد الدهني الذي يسبق السكري غالباً.","fd":17.8,"fnd":6.5,"md":14.7,"mnd":10.6,"gf":"+11.2%","gm":"+4.1%"},
    {"name":"Creatinine (كرياتينين)","rank":"#4","desc":"مؤشر وظائف الكلى. ارتفاعه عند مرضى السكري يعكس بدايات تأثر الكلى.","fd":17.5,"fnd":7.8,"md":15.1,"mnd":8.0,"gf":"+9.7%","gm":"+7.1%"},
  ],
},
}

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

def yn(q, t, k):
    v = st.radio(q, [t["yes"], t["no"]], index=None, horizontal=True, key=k)
    return 1 if v == t["yes"] else (0 if v == t["no"] else None)

def risk_cls(p):
    return "low" if p<0.40 else ("mod" if p<0.70 else "high")

def render_nut(r, lang):
    t = T[lang]
    nd = NUT[lang][r]
    st.markdown(f"### {t['nut_title']}")
    st.markdown(f'<div class="nut-section"><div class="nut-title">{nd["goal"]}</div>', unsafe_allow_html=True)
    for cat, desc in nd["cats"]:
        st.markdown(f'<div class="nut-cat">{cat}</div><div class="nut-item">{desc}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="nut-note"><b>{t["nut_note_lbl"]}:</b> {nd["note"]}<br><small style="color:#5eead4">{t["nut_src"]}: {nd["source"]}</small></div></div>', unsafe_allow_html=True)

def render_jordan(lang):
    t = T[lang]
    st.markdown(f"### {t['jordan_title']}")
    for title, desc in t["jordan_items"]:
        with st.expander(title):
            st.markdown(desc)

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
    _, c1, c2, _ = st.columns([0.5, 2, 2, 0.5])
    with c1:
        if st.button(t["btn_assess"], key="ga"): st.session_state.page="assess"; st.rerun()
    with c2:
        if st.button(t["btn_guide"], key="gg"): st.session_state.page="guide"; st.rerun()

def render_assess():
    t = T[st.session_state.lang]
    c_bk, _, c_lg = st.columns([2,6,2])
    with c_bk:
        if st.button(t["back"], key="bk_a"): st.session_state.page="home"; st.rerun()
    with c_lg:
        if st.button(t["lang_btn"], key="lang_a"):
            st.session_state.lang = "ar" if st.session_state.lang=="en" else "en"; st.rerun()

    st.markdown(f'<div class="app-header"><div class="app-title">🤖 {t["assess_title"]}</div><div class="app-subtitle">{t["assess_sub"]}</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="disc-blue">{t["disc_main"]}</div>', unsafe_allow_html=True)

    if not model_ok:
        st.error("Model files not found."); return

    st.markdown(f'<div class="card-title">{t["sec_body"]}</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        hh = st.number_input(t["bmi_h"], min_value=100, max_value=250, value=170)
    with c2:
        ww = st.number_input(t["bmi_w"], min_value=30, max_value=300, value=70)
    bv = round(ww / ((hh / 100) ** 2), 1)
    st.markdown(f'<div style="color:#2dd4bf;font-weight:700;font-size:1.1rem;margin-bottom:12px;">📊 {t["bmi_res"]}: {bv}</div>', unsafe_allow_html=True)

    with st.form("rf"):
        st.markdown(f'<div class="card-title">{t["sec_demo"]}</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            ai = st.selectbox(t["q_age"], t["age_opts"], index=None, placeholder="—")
            av = t["age_opts"].index(ai)+1 if ai else 5
        with c2:
            ei = st.selectbox(t["q_edu"], t["edu_opts"], index=None, placeholder="—")
            ev = t["edu_opts"].index(ei)+1 if ei else 4
        ii = st.selectbox(t["q_inc"], t["inc_opts"], index=None, placeholder="—")
        iv = t["inc_opts"].index(ii)+1 if ii else 4

        st.divider()
        c1, _ = st.columns(2)
        with c1:
            gi = st.selectbox(t["q_gh"], t["gh_opts"], index=None, placeholder="—")
            gv = t["gh_opts"].index(gi)+1 if gi else 3

        st.divider()
        st.markdown(f'<div class="card-title">{t["sec_cond"]}</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            bp = yn(t["q_bp"],   t, "bp")
            ch = yn(t["q_chol"], t, "ch")
        with c2:
            sk = yn(t["q_stroke"], t, "sk")
            ht = yn(t["q_heart"],  t, "ht")
            wk = yn(t["q_walk"],   t, "wk")

        st.divider()
        st.markdown(f'<div class="card-title">{t["sec_life"]}</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: sm = yn(t["q_smoke"], t, "sm")
        with c2: pa = yn(t["q_phys"],  t, "pa")

        st.divider()
        st.markdown(f'<div class="card-title">{t["sec_days"]}</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: mh = st.slider(t["q_ment"],  0, 30, 0)
        with c2: ph = st.slider(t["q_phys2"], 0, 30, 0)

        sub = st.form_submit_button(t["submit"])

    if sub:
        # Use defaults for unanswered radio buttons
        inp = {
            "HighBP": bp if bp is not None else 0,
            "HighChol": ch if ch is not None else 0,
            "Smoker": sm if sm is not None else 0,
            "Stroke": sk if sk is not None else 0,
            "HeartDiseaseorAttack": ht if ht is not None else 0,
            "PhysActivity": pa if pa is not None else 1,
            "DiffWalk": wk if wk is not None else 0,
            "GenHlth": gv, "Age": av, "Education": ev, "Income": iv,
            "BMI": bv, "MentHlth": mh, "PhysHlth": ph
        }
        with st.spinner("⏳"):
            try: prob = predict(inp)
            except Exception as e: st.error(f"Error: {e}"); return

        r = risk_cls(prob); pct = round(prob*100, 1)
        rl = {"low":t["low"],"mod":t["mod"],"high":t["high"]}
        rc = {"low":"risk-low","mod":"risk-mod","high":"risk-high"}
        bc = {"low":"pbar-low","mod":"pbar-mod","high":"pbar-high"}
        rk = {"low":"rec_low","mod":"rec_mod","high":"rec_high"}

        st.markdown("---")
        st.markdown(f"### 📊 {t['res_title']}")
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:16px;margin-bottom:14px;">
          <span style="color:#9ca3af;">{t['risk_lbl']}:</span>
          <span class="{rc[r]}">{rl[r]}</span>
        </div>
        <div style="color:#9ca3af;font-size:.9rem;margin-bottom:6px;">{t['prob_lbl']}: <strong style="color:#fff">{pct}%</strong></div>
        <div class="pbar-bg"><div class="{bc[r]}" style="width:{pct}%"></div></div>
        """, unsafe_allow_html=True)

        st.markdown(f"### 💡 {t['rec_title']}")
        html = "".join([f'<div class="rec-item">{x}</div>' for x in t[rk[r]]])
        st.markdown(f'<div class="card">{html}</div>', unsafe_allow_html=True)

        # Nutritional recommendations specific to risk level
        render_nut(r, st.session_state.lang)

        # Jordan community notes
        render_jordan(st.session_state.lang)
        st.markdown(f'<div class="disc-purple">{t["disc_main"]}</div>', unsafe_allow_html=True)

def render_guide():
    t = T[st.session_state.lang]
    c_bk, _, c_lg = st.columns([2,6,2])
    with c_bk:
        if st.button(t["back"], key="bk_g"): st.session_state.page="home"; st.rerun()
    with c_lg:
        if st.button(t["lang_btn"], key="lang_g"):
            st.session_state.lang = "ar" if st.session_state.lang=="en" else "en"; st.rerun()

    st.markdown(f'<div class="app-header"><div class="app-title">📚 {t["guide_title"]}</div><div class="app-subtitle">{t["guide_sub"]}</div></div>', unsafe_allow_html=True)

    with st.expander(t["g_about"]): st.markdown(t["about"])
    with st.expander(t["g_diff"]):
        st.markdown(t["diff_intro"])
        h=t["diff_h"]; rows=t["diff_r"]
        st.markdown(f'<table class="ctable"><tr>{"".join(f"<th>{x}</th>" for x in h)}</tr>{"".join(f"""<tr><td class="feat">{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>""" for r in rows)}</table>', unsafe_allow_html=True)
    with st.expander(t["g_same"]): st.markdown(t["same"])
    with st.expander(t["g_symp"]):
        for s in t["symp_list"]: st.markdown(f"- {s}")
    with st.expander(t["g_risk"]):
        for r in t["risk_list"]: st.markdown(f"- {r}")
    with st.expander(t["g_comp"]):
        for nm, dc in t["comp_list"]: st.markdown(f"**{nm}** — {dc}")
    with st.expander(t["g_prev"]):
        for p in t["prev_list"]: st.markdown(f"- {p}")
    with st.expander(t["g_stats"]):
        for stat, desc in t["stats"]:
            st.markdown(f'<div style="display:flex;gap:16px;padding:10px 0;border-bottom:1px solid #2a2a4a;align-items:center;"><div style="color:#c084fc;font-size:1.1rem;font-weight:800;min-width:150px;">{stat}</div><div style="color:#d1d5db;">{desc}</div></div>', unsafe_allow_html=True)
    with st.expander(t["g_lab"]):
        st.markdown(f'<div class="disc-blue">{t["lab_intro"]}</div>', unsafe_allow_html=True)
        st.markdown(f"#### {t['lab_rank']}")
        lts = t["lab_tests"]
        names = [x["name"].split(" (")[0] for x in lts]
        gf = [float(x["gf"].replace("+","").replace("%","")) for x in lts]
        gm = [float(x["gm"].replace("+","").replace("%","")) for x in lts]
        df = pd.DataFrame({t["lab_f"]: gf, t["lab_m"]: gm}, index=names)
        st.bar_chart(df, color=["#a855f7","#2dd4bf"])
        st.caption(f"📊 {t['lab_cap']}")
        st.markdown("---")
        for x in lts:
            st.markdown(f"""<div class="lcard"><div class="lname">{x['rank']} — {x['name']}</div><div class="ldesc">{x['desc']}</div>
              <div style="font-size:.8rem;color:#9ca3af;margin-bottom:4px;">{t['lab_f']}: {t['lab_d']} <b style="color:#c084fc">{x['fd']}%</b> | {t['lab_nd']} <b>{x['fnd']}%</b> — Gap: <b style="color:#c084fc">{x['gf']}</b></div>
              <div class="lbar"><div class="lbar-f" style="width:{x['fd']}%"></div></div>
              <div class="lbar"><div class="lbar-f" style="width:{x['fnd']}%;opacity:.4"></div></div>
              <div style="font-size:.8rem;color:#9ca3af;margin:6px 0 4px;">{t['lab_m']}: {t['lab_d']} <b style="color:#2dd4bf">{x['md']}%</b> | {t['lab_nd']} <b>{x['mnd']}%</b> — Gap: <b style="color:#2dd4bf">{x['gm']}</b></div>
              <div class="lbar"><div class="lbar-m" style="width:{x['md']}%"></div></div>
              <div class="lbar"><div class="lbar-m" style="width:{x['mnd']}%;opacity:.4"></div></div></div>""", unsafe_allow_html=True)
        st.markdown(f"<div style='color:#6b7280;font-size:.78rem;margin-top:6px;'>{t['lab_note']}</div>", unsafe_allow_html=True)

    with st.expander(t["g_nut"]):
        st.markdown("### 🟢 " + T[st.session_state.lang]["low"])
        render_nut("low", st.session_state.lang)
        st.markdown("### 🟡 " + T[st.session_state.lang]["mod"])
        render_nut("mod", st.session_state.lang)
        st.markdown("### 🔴 " + T[st.session_state.lang]["high"])
        render_nut("high", st.session_state.lang)

    with st.expander(t["jordan_title"]):
        for title, desc in t["jordan_items"]:
            st.markdown(f"**{title}**")
            st.markdown(desc)
            st.divider()

p = st.session_state.page
if p=="home":    render_home()
elif p=="assess": render_assess()
elif p=="guide":  render_guide()
