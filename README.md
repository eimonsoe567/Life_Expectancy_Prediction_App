# Life_Expectancy_Prediction_App

Global Life Expectancy Prediction App
Developed by: Ei Mon Soe

Major: Statistics and Data Science (Parami University)

📌 Project Overview
This project leverages Machine Learning to predict life expectancy based on health, immunization, and socio-economic factors. Using a dataset sourced from Kaggle (originally provided by the World Health Organization), the goal was to transform complex global health data into an intuitive tool that provides immediate insights into a country’s health profile.

Data Science Workflow
1. Data Preprocessing & Cleaning
Real-world data is often messy. I implemented several statistical techniques to ensure data integrity:

(1) Intelligent Imputation: Used SimpleImputer (mean strategy) for columns with minimal missing values. For Alcohol, I used a Grouped Mean (by Country) to reflect regional cultural patterns.

(2) Outlier Handling: For skewed features like GDP, Hepatitis B, and Population, I applied Median Imputation to prevent extreme values from biasing the model.

(3) Feature Extraction (Dimensionality Reduction): To make the app user-friendly, I combined related features:
    - Immunization Index: Averaged Hepatitis B, Polio, and Diphtheria into one score.
    - Thinness Index: Combined child and adolescent thinness metrics using Log Transformation and Min-Max Scaling to handle non-normal distributions.

2. Model Training
(1) Algorithm: Linear Regression.
(2) Encoding: Used LabelEncoder for categorical variables like Country and Status.
(3) Performance:
    - R2 Score of 0.81: The model explains 81% of the variance in life expectancy.
    - MAE of 2.92: On average, predictions are within 3 years of the actual values.

Web Application Features
The app was built using Streamlit with a focus on User Experience (UX):

(1) Geographic Context: Users select a country, and the app automatically identifies its development status (locked via a disabled selectbox to maintain data accuracy).
(2) Interactive Controls: Used sliders and numeric inputs (preset to global means) for easy data entry.
(3) Real-time Summary: A dynamic "Snapshot" table updates instantly as users adjust parameters.
(4) Health Stage Classification: Based on the prediction, the app categorizes life expectancy into four stages:
    - 🔴 Critical (≤ 45 years)
    - 🟠 At Risk (45-55 years)
    - 🟢 Unhealthy (55–70 years)
    - 🔵 Healthy (> 70 years)

🚀 Tech Stack
Language: Python
Libraries: Pandas, NumPy, Scikit-learn, Matplotlib, PIL
Deployment: Streamlit Cloud
Model Persistence: Pickle
