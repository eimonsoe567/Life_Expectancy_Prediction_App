import pickle
import streamlit as st
import pandas as pd
from PIL import Image

# 1. Load trained model package
with open("life_expectancy_app.pkl", "rb") as f:
    model_package = pickle.load(f)

model = model_package["model"]
encoders = model_package["encoders"] 
columns_order = model_package["columns"]

# Extract specific encoders
le_country = encoders["Country"]
le_status = encoders["Status"]

# Sidebar (Student info and logo)
st.sidebar.markdown("---")
try:
    logo = Image.open("images/parami_logo.png") 
    st.sidebar.image(logo, use_container_width=True)
except Exception:
    st.sidebar.error("Logo not found.")

st.sidebar.subheader("Student Information")
st.sidebar.markdown("""
**Name:** Ei Mon Soe<br>
**Major:** Statistics and Data Science<br>
**University:** PARAMI University
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

st.sidebar.header("How it works")
st.sidebar.markdown("""
1. Select your **Country** and **Status**.
2. Input immunization, mortality, and socio-economic factors.  
3. Click Predict.
4. See life stage:
   - **Critical** 🔴
   - **At Risk** 🟠
   - **Unhealthy** 🟢
   - **Healthy** 🔵
""")

# App Title
st.title("🌍 Life Expectancy Prediction App")

# --- Input Section ---
st.subheader("General Information")
col_a, col_b = st.columns(2)

with col_a:
    country_list = list(le_country.classes_)
    selected_country = st.selectbox("📍 Select Country", country_list)

with col_b:
    status_list = list(le_status.classes_)
    selected_status = st.selectbox("🌎 Country Status", status_list)

st.markdown("---")
st.subheader("Health & Socio-Economic Indicators")
col1, col2 = st.columns(2)

with col1:
    Schooling = st.slider("📚 Schooling", min_value=0.0, max_value=20.0, value=12.0, step=0.1)
    Income_comp = st.slider("💵 Income Composition", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
    GDP = st.number_input("💰 GDP per Capita", min_value=0.0, value=5000.0)
    Immunization = st.slider("Immunization %", min_value=0.0, max_value=100.0, value=95.0)

with col2:
    Alcohol = st.slider("🍷 Alcohol Consumption", min_value=0.0, max_value=20.0, value=5.0)
    Adult_Mortality = st.number_input("💀 Adult Mortality", min_value=1.0, max_value=1000.0, value=150.0)
    HIV_AIDS = st.number_input("🎗️ HIV/AIDS Deaths", min_value=0.0, value=0.1)
    BMI = st.slider("⚖️ BMI", min_value=1.0, max_value=70.0, value=25.0)

st.markdown("---")
col3, col4 = st.columns(2)
with col3:
    percentage_expenditure = st.slider("🏥 Health Expenditure", min_value=0.0, max_value=30.0, value=5.0)
    Total_expenditure = st.slider("🏛️ Gov Health Spending", min_value=0.0, max_value=20.0, value=6.0)
with col4:
    under_five = st.number_input("🧒 Under-Five Deaths", min_value=0, value=20)
    thinness_mean = st.slider("👶 Thinness Mean", min_value=0.0, max_value=30.0, value=5.0)

# --- THE FIX: Encode the selections ---
country_encoded = le_country.transform([selected_country])[0]
status_encoded = le_status.transform([selected_status])[0]

# Create Input DataFrame
# I removed "Status_encoded" because your model expects "Status" (containing the number)
input_data = pd.DataFrame({
    "Country": [country_encoded],
    "Status": [status_encoded],
    "Adult Mortality": [Adult_Mortality],
    "Alcohol": [Alcohol],
    "percentage expenditure": [percentage_expenditure],
    " BMI ": [BMI],
    "under-five deaths ": [under_five],
    "Total expenditure": [Total_expenditure],
    " HIV/AIDS": [HIV_AIDS],
    "GDP": [GDP],
    "Income composition of resources": [Income_comp],
    "Schooling": [Schooling],
    "Immunization": [Immunization],
    "thinness_mean": [thinness_mean]
})

# Reorder columns to match model training exactly
input_data = input_data[columns_order]

# --- Prediction Logic ---
if st.button("Predict Life Expectancy"):
    try:
        prediction = model.predict(input_data)[0]
        st.markdown("---")
        st.success(f"Predicted Life Expectancy: **{round(prediction, 2)} years**")
        
        # Health stage logic
        if prediction <= 45: health_stage, image = "Critical 🔴", "critical_image.jpg"
        elif prediction <= 55: health_stage, image = "At Risk 🟠", "at_risk_image.jpg"
        elif prediction <= 70: health_stage, image = "Unhealthy 🟢", "unhealthy_image.jpg"
        else: health_stage, image = "Healthy 🔵", "healthy_image.jpg"

        st.write(f"Health Stage: **{health_stage}**")
        
        # Display Image
        try:
            img = Image.open(f"images/{image}").resize((300, 300))
            st.image(img)
        except:
            st.info("Stage image not found.")

        # --- THE FIX: Summary Section showing NAMES, not Numbers ---
        st.markdown("### 📋 Summary of Chosen Factors")
        summary_df = pd.DataFrame({
            "Factor": ["Country", "Status", "Schooling", "GDP", "Immunization"],
            "Value": [selected_country, selected_status, f"{Schooling} yrs", f"${GDP:,.2f}", f"{Immunization}%"]
        })
        st.table(summary_df)
        
    except Exception as e:
        st.error(f"Error: {e}")
