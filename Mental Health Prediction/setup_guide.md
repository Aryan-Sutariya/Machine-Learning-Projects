# Streamlit Mental Health Prediction App - Setup Guide

This guide explains how to set up and run the application after unzipping the project folder.

## Prerequisites
- Python installed on your system (preferably Python 3.8+).

## Step-by-Step Instructions

### 1. Open Terminal/Command Prompt
Navigate to the unzipped folder containing the project files.
```cmd
cd path/to/unzipped_folder
```

### 2. Create a Virtual Environment
It is highly recommended to create a Python virtual environment to manage the project dependencies securely without affecting your global Python setup.
**For Windows:**
```cmd
python -m venv venv
```
**For macOS/Linux:**
```bash
python3 -m venv venv
```

### 3. Activate the Virtual Environment
**For Windows (Command Prompt):**
```cmd
venv\Scripts\activate
```
*(If using PowerShell):*
```powershell
.\venv\Scripts\Activate.ps1
```

**For macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Required Libraries
Install all libraries necessary to run the web application and its machine learning model:
```cmd
pip install streamlit pandas numpy matplotlib seaborn scikit-learn joblib
```

### 5. Running the Application
Once the dependencies install successfully, you can start the Streamlit web application:
```cmd
streamlit run mental_health_prediction.py
```
This command will start a local server and automatically open the application your default web browser (typically at http://localhost:8501).

