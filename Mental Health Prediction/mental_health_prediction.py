import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import joblib
import warnings
from sklearn.preprocessing import LabelEncoder
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Mental Health in Tech",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
#  CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

[data-testid="stSidebar"] {
    background: linear-gradient(175deg, #0d1b2a 0%, #1b2838 50%, #0d2137 100%);
}
[data-testid="stSidebar"] * { color: #c9d8e8 !important; }

.metric-row { display: flex; gap: 16px; margin-bottom: 28px; flex-wrap: wrap; }
.metric-card {
    flex: 1; min-width: 150px;
    background: linear-gradient(135deg, #0d1b2a, #1b2d45);
    border: 1px solid #1e4060;
    border-radius: 14px;
    padding: 22px 20px;
    text-align: center;
}
.metric-card .val {
    font-family: 'DM Serif Display', serif;
    font-size: 2.2rem;
    color: #00d4ff;
    line-height: 1;
}
.metric-card .lbl {
    font-size: 0.78rem;
    color: #7aaac8;
    margin-top: 6px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
.section-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.6rem;
    color: white;
    border-left: 4px solid #00b4cc;
    padding-left: 12px;
    margin: 32px 0 16px;
}
.page-hero {
    background: linear-gradient(120deg, #0d1b2a 0%, #1b3a52 100%);
    border-radius: 16px;
    padding: 32px 36px;
    margin-bottom: 32px;
    color: white;
}
.page-hero h1 { font-family: 'DM Serif Display', serif; font-size: 2.2rem; margin: 0; color: white; }
.page-hero p  { color: #8ab4d4; margin-top: 8px; font-size: 1.02rem; }

.result-wrap { border-radius: 16px; padding: 32px; text-align: center; margin-top: 24px; }
.result-yes { background: linear-gradient(135deg,#e8f5e9,#c8e6c9); border: 2px solid #43a047; }
.result-no  { background: linear-gradient(135deg,#fce4ec,#f8bbd0); border: 2px solid #e91e63; }
.result-wrap h2 { font-family:'DM Serif Display',serif; font-size:1.9rem; margin:0; }
.result-wrap p  { font-size:0.95rem; color:#444; margin-top:10px; }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    """
    Loads raw survey.csv and applies the exact same preprocessing
    pipeline used during model training.
    Returns two DataFrames:
      - df_raw  : readable version (original string labels) for EDA display
      - df_clean: fully encoded version (mirrors training data)
    """
    try:
        df = pd.read_csv("survey.csv")
    except FileNotFoundError:
        st.error("survey.csv not found. Place the dataset in the same folder as this script.")
        st.stop()

    # ── Step 1: Drop irrelevant columns ──────────────────────────
    df.drop(columns=['Timestamp', 'comments', 'state', 'Country'],
            inplace=True, errors='ignore')

    # ── Step 2: Age filter ────────────────────────────────────────
    df = df[(df['Age'] >= 18) & (df['Age'] <= 100)].copy()

    # ── Step 3: Gender normalisation ─────────────────────────────
    male_terms = [
        'male', 'm', 'male-ish', 'maile', 'cis male', 'mal', 'male (cis)',
        'make', 'guy (-ish) ^_^', 'man', 'msle', 'mail', 'malr', 'cis man'
    ]
    female_terms = [
        'female', 'f', 'woman', 'femake', 'femail', 'cis female',
        'cis-female/femme', 'female (cis)', 'female '
    ]
    df['Gender'] = df['Gender'].str.lower().str.strip()
    def group_gender(g):
        if g in male_terms:   return 'male'
        elif g in female_terms: return 'female'
        else:                   return 'other'
    df['Gender'] = df['Gender'].apply(group_gender)

    # ── Step 4: Fill missing values ───────────────────────────────
    df['self_employed']  = df['self_employed'].fillna(df['self_employed'].mode()[0])
    df['work_interfere'] = df['work_interfere'].fillna(df['work_interfere'].mode()[0])

    # Keep a readable copy BEFORE label-encoding for EDA charts
    df_raw = df.copy()

    # ── Step 5: Label-encode exactly the columns used in training ─
    le = LabelEncoder()
    encode_cols = [
        'mental_health_consequence', 'self_employed', 'care_options',
        'seek_help', 'treatment', 'family_history', 'work_interfere'
    ]
    df_clean = df.copy()
    for col in encode_cols:
        if col in df_clean.columns:
            df_clean[col] = le.fit_transform(df_clean[col])

    return df_raw, df_clean


@st.cache_resource
def load_model():
    try:
        return joblib.load("models/rf_atf_model.pkl")
    except FileNotFoundError:
        st.error("models/rf_atf_model.pkl not found. Train and save the model first.")
        st.stop()


df_raw, df_clean = load_data()
model = load_model()

FEATURES = ['work_interfere', 'Age', 'self_employed',
            'care_options', 'seek_help', 'family_history', 'benefits']


with st.sidebar:
    st.markdown("## 🧠 Mental Health")
    st.markdown("##### Tech Workforce Insights")
    st.markdown("---")
    page = st.radio("Navigation", ["📊  Dashboard", "🔮  Prediction"])
    st.markdown("---")
    st.markdown(
        f"<small style='color:#4a7090'>Records: {len(df_raw):,} &nbsp;|&nbsp; Features: {df_raw.shape[1]}</small>",
        unsafe_allow_html=True
    )


def show_plot(fig):
    st.pyplot(fig)
    plt.close(fig)


if page == "📊  Dashboard":

    st.markdown("""
    <div class="page-hero">
        <h1>🧠 Mental Health in Tech Dashboard</h1>
        <p>Exploring workplace mental health patterns across the tech industry.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Key Metrics ──────────────────────────────────────────────
    total   = len(df_clean)
    treated = int(df_clean['treatment'].sum())
    pct     = round(treated / total * 100, 1)
    avg_age = int(df_raw['Age'].mean())

    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-card"><div class="val">{total:,}</div><div class="lbl">Total Respondents</div></div>
        <div class="metric-card"><div class="val">{treated:,}</div><div class="lbl">Sought Treatment</div></div>
        <div class="metric-card"><div class="val">{pct}%</div><div class="lbl">Treatment Rate</div></div>
        <div class="metric-card"><div class="val">{avg_age}</div><div class="lbl">Average Age</div></div>
    </div>
    """, unsafe_allow_html=True)

    # ── Data preview ─────────────────────────────────────────────
    with st.expander("🗂️  Raw Data Preview (before encoding)", expanded=False):
        st.dataframe(df_raw.head(30), use_container_width=True)
        st.caption(f"Shape: {df_raw.shape[0]} rows × {df_raw.shape[1]} columns")

    with st.expander("🔢  Encoded Data Preview (used for training)", expanded=False):
        st.dataframe(df_clean.head(30), use_container_width=True)
        st.caption("Label-encoded columns: mental_health_consequence, self_employed, care_options, seek_help, treatment, family_history, work_interfere")

    with st.expander("📋  Column Info", expanded=False):
        buf = [{"Column": c, "Dtype": str(df_raw[c].dtype),
                "Unique": df_raw[c].nunique(), "Non-Null": df_raw[c].count()}
               for c in df_raw.columns]
        st.dataframe(pd.DataFrame(buf), use_container_width=True)

    st.markdown('<div class="section-title">Exploratory Data Analysis</div>',
                unsafe_allow_html=True)

    # ── 1 & 2: Treatment by Gender | Age Distribution ────────────
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Treatment Rates by Gender**")
        if 'Gender' in df_raw.columns:
            tr = df_raw.groupby('Gender')['treatment'].value_counts().unstack(fill_value=0)
            fig, ax = plt.subplots(figsize=(6, 4))
            tr.plot(kind='bar', ax=ax, color=['#ef5350', '#42a5f5'], edgecolor='white')
            ax.set_axisbelow(True)
            ax.set_title('Treatment Rates by Gender', fontsize=13, fontweight='bold')
            ax.set_xlabel('Gender', fontsize=11); ax.set_ylabel('Count', fontsize=11)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
            ax.legend(title='Status', labels=['No Treatment', 'Treated'])
            ax.grid(axis='y', linestyle='--', alpha=0.6)
            fig.tight_layout(); show_plot(fig)

    with col2:
        st.markdown("**Age Distribution**")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.histplot(df_raw['Age'], kde=True, color='teal', bins=20,
                     line_kws={'linewidth': 2.5}, ax=ax)
        ax.axvline(30, color='red',    linestyle='--', label='Early Career (30)')
        ax.axvline(45, color='orange', linestyle='--', label='Mid Career (45)')
        ax.set_title('Age Distribution', fontsize=13, fontweight='bold')
        ax.set_xlabel('Age', fontsize=11); ax.set_ylabel('Frequency', fontsize=11)
        ax.legend(fontsize=9); fig.tight_layout(); show_plot(fig)

    # ── 3 & 4: Treatment Gaps | Company Size Stigma ──────────────
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("**Treatment Gaps by Age**")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.histplot(data=df_raw, x='Age', hue='treatment', kde=True,
                     element="step", ax=ax)
        ax.set_title('Treatment Gaps', fontsize=13, fontweight='bold')
        ax.set_xlabel('Age', fontsize=11); ax.set_ylabel('Frequency', fontsize=11)
        fig.tight_layout(); show_plot(fig)

    with col4:
        st.markdown("**Company Size vs. Mental Health Stigma**")
        if 'no_employees' in df_raw.columns and 'mental_vs_physical' in df_raw.columns:
            size_order = ['1-5', '6-25', '26-100', '100-500', '500-1000', 'More than 1000']
            df_s = df_raw.copy()
            df_s['no_employees'] = pd.Categorical(
                df_s['no_employees'], categories=size_order, ordered=True)
            health = df_s.groupby('no_employees', observed=True)['mental_vs_physical']\
                         .value_counts().unstack(fill_value=0)
            fig, ax = plt.subplots(figsize=(6, 4))
            health.plot(kind='bar', ax=ax, edgecolor='white')
            ax.set_axisbelow(True)
            ax.set_title('Company Size vs. Stigma', fontsize=13, fontweight='bold')
            ax.set_xlabel('No. of Employees', fontsize=11); ax.set_ylabel('Frequency', fontsize=11)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha='right')
            ax.grid(axis='y', linestyle='--', alpha=0.6)
            ax.legend(title='Perception', bbox_to_anchor=(1, 1), fontsize=8)
            fig.tight_layout(); show_plot(fig)

    # ── 5 & 6: Violin | Tech Benefits ────────────────────────────
    col5, col6 = st.columns(2)

    with col5:
        st.markdown("**Family History Impact on Work Interference**")
        if 'Gender' in df_raw.columns:
            # work_interfere is still string here (Never/Rarely/Sometimes/Often) in df_raw
            wi_order = {'Never': 0, 'Rarely': 1, 'Sometimes': 2, 'Often': 3}
            df_v = df_raw.copy()
            df_v['wi_num'] = df_v['work_interfere'].map(wi_order) \
                if df_v['work_interfere'].dtype == object \
                else df_v['work_interfere']
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.violinplot(data=df_v, x='family_history', y='wi_num',
                           hue='Gender', inner='quartile', cut=0, ax=ax)
            ax.set_axisbelow(True)
            ax.set_title('Family History vs Work Interference', fontsize=13, fontweight='bold')
            ax.set_xlabel('Family History', fontsize=11)
            ax.set_ylabel('Work Interference', fontsize=11)
            ax.set_xticks([0, 1]); ax.set_xticklabels(['No', 'Yes'])
            ax.set_yticks([0, 1, 2, 3])
            ax.set_yticklabels(['Never', 'Rarely', 'Sometimes', 'Often'])
            ax.grid(axis='y', linestyle='--', alpha=0.6)
            fig.tight_layout(); show_plot(fig)

    with col6:
        st.markdown("**Coworker–Supervisor Support Correlation**")
        if 'coworkers' in df_raw.columns and 'supervisor' in df_raw.columns:
            # st.markdown("**Coworker–Supervisor Support Correlation**")
            le_tmp = LabelEncoder()
            cw = le_tmp.fit_transform(df_raw['coworkers'].astype(str))
            sv = le_tmp.fit_transform(df_raw['supervisor'].astype(str))
            corr = pd.DataFrame({'coworkers': cw, 'supervisor': sv}).corr()
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f",
                        vmin=-1, vmax=1, ax=ax, linewidths=0.5)
            ax.set_title('Coworker–Supervisor Correlation', fontsize=12, fontweight='bold')
            fig.tight_layout(); show_plot(fig)
            c_h, _ = st.columns([1, 2])
            # with c_h:
                

    # with col6:
    #     st.markdown("**Tech vs Non-Tech: Benefits & Wellness Program**")
    #     if 'tech_company' in df_raw.columns:
    #         support_cols = [c for c in ['benefits', 'wellness_program'] if c in df_raw.columns]
    #         if support_cols:
    #             fig, axes = plt.subplots(1, len(support_cols), figsize=(6, 4))
    #             if len(support_cols) == 1:
    #                 axes = [axes]
    #             for i, cname in enumerate(support_cols):
    #                 analysis = pd.crosstab(df_raw['tech_company'], df_raw[cname], normalize='index')
    #                 analysis.plot(kind='bar', stacked=True, ax=axes[i],
    #                               color=['#ff9999', '#66b3ff', '#99ff99'], edgecolor='white')
    #                 for p in axes[i].patches:
    #                     w, h = p.get_width(), p.get_height()
    #                     x, y = p.get_xy()
    #                     if h > 0.05:
    #                         axes[i].text(x + w/2, y + h/2, f'{h*100:.0f}%',
    #                                      ha='center', va='center', fontsize=8)
    #                 axes[i].set_title(cname.replace('_', ' ').title(), fontsize=11, fontweight='bold')
    #                 axes[i].set_ylabel('Proportion'); axes[i].set_xlabel('')
    #                 axes[i].set_xticklabels(['Non-Tech', 'Tech'], rotation=0)
    #                 axes[i].set_axisbelow(True)
    #                 axes[i].grid(axis='y', linestyle='--', alpha=0.6)
    #                 axes[i].legend(title=cname.capitalize(), fontsize=7, bbox_to_anchor=(1, 1))
    #             fig.tight_layout(); show_plot(fig)

    # ── 7: Coworker–Supervisor Heatmap (encode on the fly) ────────
   

    # ── 8: Feature Importance ─────────────────────────────────────
    st.markdown('<div class="section-title">Model Feature Importance</div>',
                unsafe_allow_html=True)
    try:
        importances = model.feature_importances_
        feat_df = pd.DataFrame({'Feature': FEATURES, 'Importance': importances})\
                    .sort_values('Importance', ascending=True)
        fig, ax = plt.subplots(figsize=(7, 3.5))
        colors = plt.cm.viridis(np.linspace(0.25, 0.85, len(feat_df)))
        bars = ax.barh(feat_df['Feature'], feat_df['Importance'], color=colors)
        ax.set_xlabel('Importance Score', fontsize=11)
        ax.set_title('Random Forest Feature Importances', fontsize=13, fontweight='bold')
        for bar, val in zip(bars, feat_df['Importance']):
            ax.text(bar.get_width() + 0.002, bar.get_y() + bar.get_height()/2,
                    f'{val:.3f}', va='center', fontsize=9)
        ax.set_axisbelow(True); ax.grid(axis='x', linestyle='--', alpha=0.5)
        fig.tight_layout(); show_plot(fig)
    except Exception as e:
        st.warning(f"Could not display feature importance: {e}")


else:
    st.markdown("""
    <div class="page-hero">
        <h1>🔮 Treatment Likelihood Prediction</h1>
        <p>Fill in the details below. The Random Forest model will predict whether
        the individual is likely to seek mental health treatment.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Enter Individual Details</div>',
                unsafe_allow_html=True)

    col_a, col_b = st.columns(2, gap="large")

    with col_a:
        st.markdown("#### 👤 Personal Information")
        age = st.slider("Age", min_value=18, max_value=75, value=30)
        self_employed  = st.selectbox("Self-Employed?", ["No", "Yes"])
        family_history = st.selectbox("Family History of Mental Illness?", ["No", "Yes"])

    with col_b:
        st.markdown("#### 🏢 Workplace Factors")

        work_interfere = st.select_slider(
            "How much does mental health interfere with work?",
            options=["Never (0)", "Rarely (1)", "Sometimes (2)", "Often (3)"],
            value="Sometimes (2)"
        )
        care_options = st.select_slider(
            "Does employer offer mental health care options?",
            options=["No (0)", "Not Sure (1)", "Yes (2)"],
            value="Not Sure (1)"
        )
        seek_help = st.select_slider(
            "Does employer provide seek-help resources?",
            options=["No (0)", "Don't Know (1)", "Yes (2)"],
            value="Don't Know (1)"
        )
        benefits = st.select_slider(
            "Are mental health benefits offered?",
            options=["No (0)", "Don't Know (1)", "Yes (2)"],
            value="Don't Know (1)"
        )

    # ── Build input dataframe ─────────────────────────────────────
    def parse_slider_val(s):
        return int(s.split("(")[-1].replace(")", "").strip())

    input_df = pd.DataFrame([{
        'work_interfere': parse_slider_val(work_interfere),
        'Age':            age,
        'self_employed':  1 if self_employed  == "Yes" else 0,
        'care_options':   parse_slider_val(care_options),
        'seek_help':      parse_slider_val(seek_help),
        'family_history': 1 if family_history == "Yes" else 0,
        'benefits':       parse_slider_val(benefits),
    }])

    with st.expander("📋 Review your inputs", expanded=False):
        label_map = {
            'work_interfere': ['Never','Rarely','Sometimes','Often'],
            'care_options':   ['No','Not Sure','Yes'],
            'seek_help':      ['No',"Don't Know",'Yes'],
            'benefits':       ['No',"Don't Know",'Yes'],
        }
        display = input_df.copy()
        for cname, mapping in label_map.items():
            display[cname] = display[cname].apply(lambda x: mapping[int(x)])
        display['self_employed']  = ['Yes' if v else 'No' for v in display['self_employed']]
        display['family_history'] = ['Yes' if v else 'No' for v in display['family_history']]
        st.dataframe(display.T.rename(columns={0: "Value"}), use_container_width=True)

    st.markdown("")
    predict_btn = st.button("🔍  Run Prediction", use_container_width=True, type="primary")

    if predict_btn:
        prediction  = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0]
        prob_yes    = round(probability[1] * 100, 1)
        prob_no     = round(probability[0] * 100, 1)

        if prediction == 1:
            st.markdown(f"""
            <div class="result-wrap result-yes text-black">
                <h2 class="text-black back">✅ Likely to Seek Treatment</h2>
                <p>The model predicts this individual is <strong>likely to seek mental health treatment</strong>.<br>
                Model confidence: <strong>{prob_yes}%</strong></p>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-wrap result-no">
                <h2 class="color:pink">⚠️ Unlikely to Seek Treatment</h2>
                <p>The model predicts this individual is <strong>unlikely to seek mental health treatment</strong>.<br>
                Model confidence: <strong>{prob_no}%</strong></p>
            </div>""", unsafe_allow_html=True)

        # Probability bar chart
        st.markdown(""); st.markdown("**Prediction Probability Breakdown**")
        prob_df = pd.DataFrame({
            'Outcome': ['No Treatment', 'Seeks Treatment'],
            'Probability (%)': [prob_no, prob_yes]
        })
        fig, ax = plt.subplots(figsize=(5, 2.2))
        bars = ax.barh(prob_df['Outcome'], prob_df['Probability (%)'],
                       color=['#ef5350', '#42a5f5'], edgecolor='white', height=0.45)
        for bar, val in zip(bars, prob_df['Probability (%)']):
            ax.text(bar.get_width() + 0.8, bar.get_y() + bar.get_height()/2,
                    f'{val}%', va='center', fontsize=11, fontweight='bold')
        ax.set_xlim(0, 115)
        ax.set_xlabel('Probability (%)', fontsize=10)
        ax.set_title('Model Confidence', fontsize=12, fontweight='bold')
        ax.set_axisbelow(True); ax.grid(axis='x', linestyle='--', alpha=0.5)
        fig.tight_layout()
        c_p, _ = st.columns([2, 3])
        with c_p:
            show_plot(fig)

        # Feature importance table
        st.markdown("**Feature Importance Reference**")
        try:
            readable = {
                'work_interfere': 'Work Interference',
                'Age': 'Age',
                'self_employed': 'Self Employed',
                'care_options': 'Care Options',
                'seek_help': 'Seek Help Resources',
                'family_history': 'Family History',
                'benefits': 'Mental Health Benefits',
            }
            fi_df = pd.DataFrame({
                'Feature': [readable[f] for f in FEATURES],
                'Your Value': input_df.iloc[0].values,
                'Importance (%)': (model.feature_importances_ * 100).round(1)
            }).sort_values('Importance (%)', ascending=False).reset_index(drop=True)
            st.dataframe(fi_df, use_container_width=True)
        except Exception:
            pass

    st.markdown("---")
    st.caption(
        "⚠️ Disclaimer: This tool is for educational and research purposes only. "
        "It is not a substitute for professional mental health advice, diagnosis, or treatment."
    )   