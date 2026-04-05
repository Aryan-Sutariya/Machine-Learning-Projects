# 🧠 Mental Health in Tech — Prediction System

> A machine learning–powered web application that predicts whether a tech industry employee is likely to seek mental health treatment, based on personal and workplace factors.

---

## 📌 Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Dataset](#dataset)
- [Features Used](#features-used)
- [Preprocessing Pipeline](#preprocessing-pipeline)
- [Exploratory Data Analysis](#exploratory-data-analysis)
- [Machine Learning Models](#machine-learning-models)
- [Final Model](#final-model)
- [Streamlit Application](#streamlit-application)
- [Setup & Installation](#setup--installation)
- [How to Run](#how-to-run)
- [Tech Stack](#tech-stack)
- [Disclaimer](#disclaimer)

---

## 📖 Overview

Mental health issues are widespread in the tech industry, yet many employees never seek treatment due to stigma, lack of employer support, or simply unawareness of available resources.

This project builds an **end-to-end ML pipeline** — from raw survey data to a fully deployed interactive web application — to:

- Identify key factors that predict treatment-seeking behavior
- Provide a real-time prediction tool for individuals or HR teams
- Visualize workforce mental health trends through an interactive dashboard

---

## 📁 Project Structure

```
mental-health-in-tech/
│
├── models/                        # Saved trained ML model
│   └── rf_atf_model.pkl           # Fine-tuned Random Forest (final model)
│
├── venv/                          # Python virtual environment
│
├── .ipynb_checkpoints/            # Jupyter auto-save checkpoints
│
├── mental_health_prediction.py    # Main Streamlit application
├── Progress Report 2.ipynb        # EDA, preprocessing & model training notebook
├── survey.csv                     # Raw dataset (OSMI Mental Health in Tech Survey)
├── analysis.jpg                   # EDA analysis output image
├── index.html                     # Static HTML page (project summary/landing)
├── project_summary.md             # High-level project summary document
├── setup_guide.md                 # Environment setup instructions
└── README.md                      # This file
```

---

## 📊 Dataset

| Property | Details |
|---|---|
| **Source** | [OSMI Mental Health in Tech Survey](https://www.kaggle.com/datasets/osmi/mental-health-in-tech-survey) |
| **File** | `survey.csv` |
| **Respondents** | ~1,200+ tech workers globally |
| **Target Variable** | `treatment` — Has the person sought mental health treatment? (Yes / No) |
| **Total Features** | 27 raw columns |

---

## 🔧 Features Used

After preprocessing, the following **7 features** were selected for model training:

| Feature | Description | Type |
|---|---|---|
| `work_interfere` | How much mental health interferes with work | Ordinal (Never → Often) |
| `Age` | Age of the respondent | Numerical |
| `self_employed` | Whether the respondent is self-employed | Binary (0 / 1) |
| `care_options` | Does employer offer mental health care? | Ordinal (No / Not Sure / Yes) |
| `seek_help` | Does employer provide seek-help resources? | Ordinal (No / Don't Know / Yes) |
| `family_history` | Family history of mental illness | Binary (0 / 1) |
| `benefits` | Does employer offer mental health benefits? | Ordinal (No / Don't Know / Yes) |

---

## ⚙️ Preprocessing Pipeline

The following steps were applied to `survey.csv` before model training:

1. **Drop irrelevant columns** — Removed `Timestamp`, `comments`, `state`, `Country`
2. **Age filtering** — Kept respondents aged **18–100** only
3. **Gender normalization** — Mapped 20+ raw gender labels → `male` / `female` / `other`
4. **Missing value imputation** — Mode-filled `self_employed` and `work_interfere`
5. **Label encoding** — Applied `LabelEncoder` to 7 categorical columns
6. **Feature selection** — Narrowed down to the 7 most predictive features

---

## 📈 Exploratory Data Analysis

Key insights discovered during EDA (see `Progress Report 2.ipynb` — Week 4):

- **Gender & Treatment:** Females showed slightly higher treatment-seeking rates than males
- **Age Distribution:** Most respondents are aged 25–40, peaking around early career (30s)
- **Family History Impact:** Employees with a family history of mental illness report greater work interference
- **Company Size & Stigma:** Smaller companies show less awareness of mental vs. physical health parity
- **Coworker–Supervisor Correlation:** Positive correlation between coworker and supervisor support ratings
- **Top Correlates of Treatment:** `work_interfere`, `family_history`, and `care_options`

Visual outputs are available in `analysis.jpg`.

---

## 🤖 Machine Learning Models

All models were trained on a **70% / 30% train-test split** (`random_state=43`).

### Regression Models (Baseline)
| Model | Metric |
|---|---|
| Linear Regression | R² Score |
| Decision Tree Regressor | R² Score |
| KNN Regressor | R² Score |

### Classification Models
| Model | Notes |
|---|---|
| Logistic Regression | Baseline classifier |
| Decision Tree Classifier | Tuned with `max_depth=6`, `class_weight='balanced'` |
| KNN Classifier | `n_neighbors=5` |
| Random Forest Classifier | ✅ **Selected as final model** |
| XGBoost Classifier | `n_estimators=123`, `learning_rate=0.09`, `max_depth=3` |

---

## 🏆 Final Model

**Model:** Tuned Random Forest Classifier
**Saved at:** `models/rf_atf_model.pkl`

### Hyperparameters

```python
RandomForestClassifier(
    n_estimators     = 300,
    max_depth        = 12,
    min_samples_split= 10,
    min_samples_leaf = 4,
    max_features     = 'sqrt',
    class_weight     = 'balanced',
    random_state     = 42
)
```

### Why Random Forest?
- Handles class imbalance with `balanced` class weights
- Controlled depth and leaf size prevent overfitting
- Provides built-in **feature importance** scores for interpretability
- Consistently outperformed other models on test accuracy

### Feature Importance Ranking
1. `work_interfere` ← Most influential
2. `family_history`
3. `Age`
4. `care_options`
5. `seek_help`
6. `benefits`
7. `self_employed`

---

## 🖥️ Streamlit Application

The app (`mental_health_prediction.py`) has two pages:

### 📊 Page 1 — Dashboard
An interactive analytics dashboard displaying:
- **Key Metrics:** Total respondents, % seeking treatment, average age
- **Charts:**
  - Treatment rates by Gender
  - Age Distribution with career-phase markers
  - Company Size vs. Mental Health Stigma
  - Coworker–Supervisor Correlation Heatmap
  - Random Forest Feature Importance chart

### 🔮 Page 2 — Prediction
A real-time treatment likelihood predictor:
- Input 7 features via sliders and dropdowns
- **Output:**
  - ✅ Green card: *"Likely to Seek Treatment"* with model confidence %
  - ⚠️ Pink card: *"Unlikely to Seek Treatment"* with model confidence %
  - Probability breakdown bar chart
  - Feature importance reference table for the current prediction

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.8+
- pip

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/mental-health-in-tech.git
cd mental-health-in-tech
```

### 2. Create & Activate Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install streamlit pandas numpy matplotlib seaborn scikit-learn xgboost joblib
```

> For detailed setup steps, refer to [`setup_guide.md`](setup_guide.md)

---

## ▶️ How to Run

Make sure `survey.csv` and `models/rf_atf_model.pkl` are present in the project root, then run:

```bash
streamlit run mental_health_prediction.py
```

The app will open automatically at `http://localhost:8501`

---

## 🛠️ Tech Stack

| Category | Tools |
|---|---|
| Language | Python 3.x |
| Web App | Streamlit |
| ML / Modeling | Scikit-learn, XGBoost |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| Model Persistence | Joblib |
| Notebook | Jupyter Notebook |
| Dataset | OSMI Mental Health in Tech Survey |

---

## ⚠️ Disclaimer

> This tool is intended for **educational and research purposes only**.
> It is **not** a substitute for professional mental health advice, diagnosis, or treatment.
> If you or someone you know is struggling with mental health, please consult a qualified healthcare professional.


*Made with ❤️ to raise awareness about mental health in the tech industry.*
