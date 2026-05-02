
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os


import sklearn.compose._column_transformer as _ct
if not hasattr(_ct, '_RemainderColsList'):
    class _RemainderColsList(list):
        @property
        def dict(self):
            return {i: v for i, v in enumerate(self)}
        def __reduce__(self):
            return (self.__class__, (list(self),))
    _ct._RemainderColsList = _RemainderColsList

st.set_page_config(
    page_title="Risk Sense | تنبؤ خطر السكري",
    page_icon="🩺",
    layout="centered",
)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&family=Inter:wght@400;600;700&display=swap');

  html, body, [class*="css"] {
    background-color: #0f0f1a !important;
    color: #e0e0f0 !important;
  }
  .stApp { background-color: #0f0f1a; }

  .card {
    background: #1a1a2e;
    border: 1px solid #2a2a4a;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
  }
  .card-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #a78bfa;
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 1px solid #2a2a4a;
  }

  .app-header { text-align: center; padding: 32px 16px 16px; }
  .app-title {
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #a78bfa, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
  }
  .app-subtitle { color: #6b7280; font-size: 0.9rem; }

  .risk-low  { background:#064e3b; color:#6ee7b7; border:1px solid #10b981; border-radius:12px; padding:6px 18px; font-weight:700; }
  .risk-mod  { background:#78350f; color:#fcd34d; border:1px solid #f59e0b; border-radius:12px; padding:6px 18px; font-weight:700; }
  .risk-high { background:#7f1d1d; color:#fca5a5; border:1px solid #ef4444; border-radius:12px; padding:6px 18px; font-weight:700; }

  .prob-bar-container { background:#2a2a4a; border-radius:12px; overflow:hidden; height:22px; margin:10px 0; }
  .prob-bar-fill-low  { background:linear-gradient(90deg,#10b981,#34d399); height:100%; border-radius:12px; }
  .prob-bar-fill-mod  { background:linear-gradient(90deg,#f59e0b,#fbbf24); height:100%; border-radius:12px; }
  .prob-bar-fill-high { background:linear-gradient(90deg,#ef4444,#f87171); height:100%; border-radius:12px; }

  .rec-item { display:flex; gap:10px; padding:10px 0; border-bottom:1px solid #2a2a4a; font-size:0.95rem; }
  .rec-item:last-child { border-bottom:none; }

  .disclaimer {
    background:#1e1a2e;
    border-left:4px solid #7c3aed;
    border-radius:8px;
    padding:12px 16px;
    font-size:0.85rem;
    color:#9ca3af;
    margin:16px 0;
  }

  .stRadio > label { color:#c4b5fd !important; font-weight:600; }
  .stSlider > label { color:#c4b5fd !important; font-weight:600; }
  .stSelectbox > label { color:#c4b5fd !important; font-weight:600; }
  .stNumberInput > label { color:#c4b5fd !important; font-weight:600; }
  div[data-baseweb="select"] { background:#1a1a2e !important; border-color:#3a3a5a !important; }
  .stButton > button {
    background: linear-gradient(135deg, #7c3aed, #2563eb) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 40px !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    width: 100%;
    margin-top: 8px;
  }
  .stButton > button:hover { opacity: 0.9; }
  [data-testid="stRadio"] div { color: #d1d5db !important; }
</style>
""", unsafe_allow_html=True)

T = {
    "en": {
        "title": "Risk Sense",
        "subtitle": "Diabetes Risk Predictor — Based on CDC BRFSS 2015",
        "lang_btn": "🌐 عربي",
        "disclaimer": "⚠️ This tool is for educational purposes only and is not a medical diagnosis. Please consult a healthcare professional.",
        "sec_demo": "👤 Demographics",
        "sec_body": "📏 Body & General Health",
        "sec_conditions": "❤️ Medical Conditions",
        "sec_lifestyle": "🏃 Lifestyle",
        "sec_days": "📅 Health Days (Past 30 Days)",
        "submit": "Get My Risk Assessment",
        "result_title": "Your Risk Assessment",
        "risk_label": "Risk Level",
        "prob_label": "Predicted Probability",
        "rec_title": "Recommendations",
        "low": "Low Risk", "mod": "Moderate Risk", "high": "High Risk",
        "q_age":   "Age Group",
        "q_edu":   "Highest Education Level",
        "q_inc":   "Annual Household Income",
        "q_bmi":   "Body Mass Index (BMI)",
        "q_bmi_h": "BMI = weight(kg) / height(m)²",
        "q_gh":    "How would you rate your general health?",
        "q_bp":    "High blood pressure (ever told by a doctor)?",
        "q_chol":  "High cholesterol (ever told by a doctor)?",
        "q_stroke":"Have you ever had a stroke?",
        "q_heart": "Coronary heart disease or heart attack?",
        "q_walk":  "Serious difficulty walking or climbing stairs?",
        "q_smoke": "Smoked at least 100 cigarettes in your life?",
        "q_phys":  "Any physical activity in the past 30 days?",
        "q_ment":  "Days mental health was NOT good (0–30)",
        "q_phys2": "Days physical health was NOT good (0–30)",
        "yes": "Yes", "no": "No",
        "age_opts": ["18–24","25–29","30–34","35–39","40–44","45–49","50–54","55–59","60–64","65–69","70–74","75–79","80+"],
        "gh_opts":  ["Excellent","Very Good","Good","Fair","Poor"],
        "edu_opts": ["Never attended / Kindergarten","Elementary","Some high school","High school graduate","Some college","College graduate"],
        "inc_opts": ["< $10,000","$10,000–$14,999","$15,000–$19,999","$20,000–$24,999","$25,000–$34,999","$35,000–$49,999","$50,000–$74,999","$75,000+"],
        "rec_low": [
            "✅ Great news! Keep maintaining your healthy habits.",
            "🥗 Continue eating fruits and vegetables daily.",
            "🏃 Stay physically active — aim for 150 min/week.",
            "🩺 Schedule annual health check-ups.",
            "💧 Stay hydrated and maintain quality sleep.",
        ],
        "rec_mod": [
            "⚠️ Moderate risk detected. Take action now.",
            "🏃 Increase physical activity to at least 150 minutes per week.",
            "🥗 Reduce refined carbohydrates and sugary drinks.",
            "📊 Monitor blood pressure and cholesterol regularly.",
            "🩺 Consult your doctor for a blood glucose test.",
            "😴 Prioritize sleep and stress management.",
        ],
        "rec_high": [
            "🚨 High risk detected. Please see a doctor soon.",
            "🩸 Request a fasting blood glucose test immediately.",
            "💊 Discuss medication options with your healthcare provider.",
            "🥗 Follow a diabetes-friendly diet: low sugar, high fiber.",
            "🏃 Even a 30-minute daily walk can help significantly.",
            "📱 Consider tracking blood glucose regularly.",
        ],
    },
    "ar": {
        "title": "ريسك سينس",
        "subtitle": "تنبؤ خطر الإصابة بالسكري — مبني على مؤشرات صحة CDC BRFSS 2015",
        "lang_btn": "🌐 English",
        "disclaimer": "⚠️ هذه الأداة للأغراض التعليمية فقط وليست تشخيصاً طبياً. يُرجى استشارة طبيبك.",
        "sec_demo": "👤 المعلومات الشخصية",
        "sec_body": "📏 الجسم والصحة العامة",
        "sec_conditions": "❤️ الحالات الطبية",
        "sec_lifestyle": "🏃 نمط الحياة",
        "sec_days": "📅 أيام الصحة (الـ 30 يوم الماضية)",
        "submit": "احصل على تقييم الخطر",
        "result_title": "نتيجة تقييمك",
        "risk_label": "مستوى الخطر",
        "prob_label": "الاحتمالية المتوقعة",
        "rec_title": "التوصيات",
        "low": "خطر منخفض", "mod": "خطر متوسط", "high": "خطر مرتفع",
        "q_age":   "الفئة العمرية",
        "q_edu":   "أعلى مستوى تعليمي",
        "q_inc":   "إجمالي دخل الأسرة السنوي",
        "q_bmi":   "مؤشر كتلة الجسم (BMI)",
        "q_bmi_h": "BMI = الوزن(كغ) ÷ الطول(م)²",
        "q_gh":    "كيف تقيّم صحتك العامة؟",
        "q_bp":    "هل أُخبرت بأن لديك ضغط دم مرتفع؟",
        "q_chol":  "هل أُخبرت بأن لديك كوليسترول مرتفع؟",
        "q_stroke":"هل أصبت بجلطة دماغية من قبل؟",
        "q_heart": "هل أصبت بمرض قلبي أو نوبة قلبية؟",
        "q_walk":  "هل تعاني صعوبة شديدة في المشي أو السلالم؟",
        "q_smoke": "هل دخّنت 100 سيجارة أو أكثر في حياتك؟",
        "q_phys":  "هل مارست نشاطاً بدنياً خلال الـ 30 يوماً الماضية؟",
        "q_ment":  "كم يوماً لم تكن صحتك النفسية جيدة؟ (0–30)",
        "q_phys2": "كم يوماً لم تكن صحتك الجسدية جيدة؟ (0–30)",
        "yes": "نعم", "no": "لا",
        "age_opts": ["18–24","25–29","30–34","35–39","40–44","45–49","50–54","55–59","60–64","65–69","70–74","75–79","80+"],
        "gh_opts":  ["ممتاز","جيد جداً","جيد","مقبول","سيئ"],
        "edu_opts": ["لم أذهب للمدرسة / روضة","ابتدائية","بعض سنوات الثانوية","ثانوية عامة","بعض سنوات الجامعة","تخرجت من الجامعة"],
        "inc_opts": ["أقل من 10,000$","10,000–14,999$","15,000–19,999$","20,000–24,999$","25,000–34,999$","35,000–49,999$","50,000–74,999$","75,000$ أو أكثر"],
        "rec_low": [
            "✅ بشرى سارة! استمر في نمط حياتك الصحي.",
            "🥗 واصل تناول الفواكه والخضروات يومياً.",
            "🏃 حافظ على النشاط البدني — 150 دقيقة أسبوعياً على الأقل.",
            "🩺 أجرِ فحوصات صحية دورية سنوية.",
            "💧 اشرب كمية كافية من الماء واحرص على النوم الجيد.",
        ],
        "rec_mod": [
            "⚠️ خطر متوسط. ابدأ باتخاذ إجراءات الآن.",
            "🏃 زد نشاطك البدني إلى 150 دقيقة أسبوعياً على الأقل.",
            "🥗 قلّل من الكربوهيدرات المكررة والمشروبات السكرية.",
            "📊 راقب ضغط دمك ومستوى الكوليسترول بانتظام.",
            "🩺 استشر طبيبك لإجراء فحص سكر الدم.",
            "😴 اهتم بجودة نومك وإدارة مستوى التوتر.",
        ],
        "rec_high": [
            "🚨 خطر مرتفع. يُرجى مراجعة الطبيب في أقرب وقت.",
            "🩸 أجرِ فحص سكر الدم الصائم فوراً.",
            "💊 ناقش خيارات العلاج مع طبيبك.",
            "🥗 اتبع نظاماً غذائياً مناسباً لمرضى السكري: قليل السكر وغني بالألياف.",
            "🏃 المشي 30 دقيقة يومياً يساعد بشكل ملحوظ.",
            "📱 فكّر في متابعة مستوى الغلوكوز بانتظام.",
        ],
    }
}

if "lang" not in st.session_state:
    st.session_state.lang = "en"

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
        "CholCheck":            inputs["CholCheck"],
        "Smoker":               inputs["Smoker"],
        "Stroke":               inputs["Stroke"],
        "HeartDiseaseorAttack": inputs["HeartDiseaseorAttack"],
        "PhysActivity":         inputs["PhysActivity"],
        "Fruits":               inputs["Fruits"],
        "Veggies":              inputs["Veggies"],
        "HvyAlcoholConsump":    inputs["HvyAlcoholConsump"],
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
        "Lifestyle_Score":      inputs["PhysActivity"] + inputs["Fruits"] + inputs["Veggies"] - inputs["HvyAlcoholConsump"],
        "Comorbidity_Score":    inputs["Stroke"] + inputs["HeartDiseaseorAttack"] + inputs["DiffWalk"],
    }
    return pd.DataFrame([row])

def predict(inputs):
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
    if prob < 0.40:   return "low"
    elif prob < 0.70: return "mod"
    else:             return "high"

t = T[st.session_state.lang]

col_spacer, col_btn = st.columns([5, 1])
with col_btn:
    if st.button(t["lang_btn"]):
        st.session_state.lang = "ar" if st.session_state.lang == "en" else "en"
        st.rerun()

st.markdown(f"""
<div class="app-header">
  <div class="app-title">🩺 {t['title']}</div>
  <div class="app-subtitle">{t['subtitle']}</div>
</div>
""", unsafe_allow_html=True)

st.markdown(f'<div class="disclaimer">{t["disclaimer"]}</div>', unsafe_allow_html=True)

if not model_loaded:
    st.error(f"⚠️ Model files not found. Place diabetes_model.pkl, preprocessor.pkl, feature_names.pkl, threshold.pkl in the same folder as app.py\n\nError: {load_error}")
    st.stop()

with st.form("risk_form"):

    st.markdown(f'<div class="card-title">{t["sec_demo"]}</div>', unsafe_allow_html=True)
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

    st.markdown(f'<div class="card-title">{t["sec_body"]}</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        bmi_val = st.number_input(t["q_bmi"], min_value=10.0, max_value=80.0, value=25.0, step=0.1, help=t["q_bmi_h"])
    with col2:
        gh_idx = st.selectbox(t["q_gh"], t["gh_opts"])
        gh_val = t["gh_opts"].index(gh_idx) + 1

    st.divider()

    st.markdown(f'<div class="card-title">{t["sec_conditions"]}</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        bp_v   = yn(t["q_bp"],    t, "bp")
        chol_v = yn(t["q_chol"], t, "chol")
    with col2:
        stroke_v = yn(t["q_stroke"], t, "stroke")
        heart_v  = yn(t["q_heart"],  t, "heart")
        walk_v   = yn(t["q_walk"],   t, "walk")

    chk_v   = 1
    fruit_v = 1
    veg_v   = 1
    alc_v   = 0

    st.divider()

    st.markdown(f'<div class="card-title">{t["sec_lifestyle"]}</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        smoke_v = yn(t["q_smoke"], t, "smoke")
    with col2:
        phys_v  = yn(t["q_phys"],  t, "phys")

    st.divider()

    st.markdown(f'<div class="card-title">{t["sec_days"]}</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        ment_v  = st.slider(t["q_ment"],  0, 30, 0)
    with col2:
        phys2_v = st.slider(t["q_phys2"], 0, 30, 0)

    submitted = st.form_submit_button(t["submit"])

if submitted:
    inputs = {
        "HighBP": bp_v, "HighChol": chol_v, "CholCheck": chk_v,
        "Smoker": smoke_v, "Stroke": stroke_v, "HeartDiseaseorAttack": heart_v,
        "PhysActivity": phys_v, "Fruits": fruit_v, "Veggies": veg_v,
        "HvyAlcoholConsump": alc_v, "DiffWalk": walk_v,
        "GenHlth": gh_val, "Age": age_val, "Education": edu_val,
        "Income": inc_val, "BMI": bmi_val,
        "MentHlth": ment_v, "PhysHlth": phys2_v,
    }

    with st.spinner("Analyzing..." if st.session_state.lang == "en" else "جاري التحليل..."):
        try:
            prob = predict(inputs)
        except Exception as e:
            st.error(f"Prediction error: {e}")
            st.stop()

    risk = classify_risk(prob)
    pct  = round(prob * 100, 1)

    risk_labels = {"low": t["low"], "mod": t["mod"], "high": t["high"]}
    risk_css    = {"low": "risk-low",         "mod": "risk-mod",         "high": "risk-high"}
    bar_css     = {"low": "prob-bar-fill-low", "mod": "prob-bar-fill-mod", "high": "prob-bar-fill-high"}
    rec_key     = {"low": "rec_low",           "mod": "rec_mod",           "high": "rec_high"}

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

    st.markdown(f'<div class="disclaimer">{t["disclaimer"]}</div>', unsafe_allow_html=True)
    