# Mental Health in Tech - Project Summary

## Overview
This project is an interactive data dashboard and predictive web application developed using **Streamlit**. Its core objective is to analyze trends surrounding mental health in the technology sector and to estimate the likelihood of an individual seeking mental health treatment based on specific personal and workplace factors.

## Core Features

### 1. Analytical Dashboard (EDA)
The app features a rich dashboard that processes raw survey data (`survey.csv`) to show meaningful insights about mental health in the tech industry:
- **Treatment Rates & Demographics:** Visualizes the gap in treatment rates across different genders and age distributions.
- **Workplace Support:** Explores how company size correlates with mental health stigma.
- **Work Interference:** Provides insights on how a family history of mental illness can increase work interference.
- **Coworker & Supervisor Correlation:** Uses heatmaps to show the correlation regarding support from co-workers relative to supervisors.

### 2. Treatment Likelihood Predictor
The application integrates a pre-trained **Random Forest Machine Learning model** (`models/rf_atf_model.pkl`) that can classify new data. 
On the "Prediction" page, users can supply profile details including:
- Age and Self-Employment status
- Family history of mental illness
- Levels of work interference
- The availability of corporate mental health benefits and care options

The system predicts if the inputted profile is **likely or unlikely to seek treatment**. It outputs the model's confidence probability as well as an explanation of which factors (Feature Importances) were primarily responsible for the decision.

## File & Directory Structure
- **`mental_health_prediction.py`**: The central application script built with Streamlit. It handles UI rendering, data preprocessing, model loading, and result generation.
- **`models/`**: A folder housing the serialized version of the trained model (`rf_atf_model.pkl`).
- **`survey.csv` & `customers.csv`**: Datasets utilized for analytical rendering and underlying data structures.
- **`Progress Report 2.ipynb`**: A Jupyter Notebook highlighting the progression of the development (specifically weeks 4 & 5).
- **`index.html`** & **`analysis.jpg`**: Extra supporting files related to the project's frontend landing or manual documentation.

## Technologies Utilized
- **Application Framework**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualizations**: Matplotlib, Seaborn
- **Machine Learning**: Scikit-Learn, Joblib
