import pickle
import streamlit as st
import pandas as pd
from PIL import Image

#Load trained model package
with open("life_expectancy_app.pkl", "rb") as f:
    model_package = pickle.load(f)
model = model_package["model"]
encoders = model_package["encoders"] 
columns_order = model_package["columns"]

#Extract specific encoders
le_country = encoders["Country"]
le_status = encoders["Status"]

#Sidebar (Student info and logo)
st.sidebar.markdown("---")
try:
    logo = Image.open("images/parami_logo.png") 
    st.sidebar.image(logo, use_container_width=True)
except Exception:
    st.sidebar.error("Logo not found. Please add 'parami_logo.png' to the images folder.")

st.sidebar.subheader("Student Information")
st.sidebar.markdown("""
**Name:** Ei Mon Soe<br>
**Major:** Statistics and Data Science<br>
**University:** PARAMI University
""", unsafe_allow_html=True)
st.sidebar.markdown("---")

#App Title
st.title("🌍 Life Expectancy Prediction App")
st.sidebar.header("How it works")
st.sidebar.markdown("""
1. Select your **Country** and **Status**.
2. Input immunization, mortality, and socio-economic factors.  
3. Click Predict.
4. See life stage:
   - Critical, 
   - At Risk,
   - Unhealthy, and 
   - Healthy.  
""")

#Input Section
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
    GDP = st.number_input("💰 GDP per Capita in USD", min_value=0.0, value=5000.0, step=100.0)
    Immunization = st.slider("Immunization (Hepatitis B, Polio, Diphtheria)", min_value=0.0, max_value=100.0, value=95.0)

with col2:
    Alcohol = st.slider("🍷 Alcohol Consumption in Liters", min_value=0.0, max_value=20.0, value=5.0, step=0.1)
    Adult_Mortality = st.number_input("💀 Adult Mortality per 1000", min_value=1.0, max_value=1000.0, value=150.0)
    HIV_AIDS = st.number_input("🎗️ HIV/AIDS Deaths", min_value=0.0, value=0.1, step=0.01)
    BMI = st.slider("⚖️ Body Mass Index", min_value=1.0, max_value=70.0, value=25.0, step=0.1)

st.markdown("---")
col3, col4 = st.columns(2)
with col3:
    percentage_expenditure = st.slider("🏥 Health Expenditure", min_value=0.0, max_value=30.0, value=5.0, step=0.1)
    Total_expenditure = st.slider("🏛️ Gov Health Spending", min_value=0.0, max_value=20.0, value=6.0, step=0.1)

with col4:
    under_five = st.number_input("🧒 Under-Five Deaths per 1000", min_value=0, max_value=1000, value=20)
    thinness_mean = st.slider("👶 Prevalence of Thinness", min_value=0.0, max_value=30.0, value=5.0, step=0.1)

Status = st.selectbox("🌎 Country Status", ["Developed", "Developing"])
Status_encoded = le.transform([Status])[0]

#Input DataFrame
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
    "Status_encoded": [Status_encoded],
    "Immunization": [Immunization], # Ensure this key matches your specific model's 'Immunization' key
    "thinness_mean": [thinness_mean]
})
#Reorder columns to match my model's training order exactly
input_data = input_data[columns_order]

#Prediction button
if st.button("Predict Life Expectancy"):
    try:
        prediction = model.predict(input_data)[0]
        rounded_prediction = round(prediction)
        
        st.markdown("---")
        st.success(f"Predicted Life Expectancy: **{rounded_prediction} years**")
        
        # Display health stage logic
        if prediction <= 45:
            health_stage, image = "Critical 🔴", "critical_image.jpg"
        elif prediction <= 55:
            health_stage, image = "At Risk 🟠", "at_risk_image.jpg"
        elif prediction <= 70:
            health_stage, image = "UnHealthy 🟢", "unhealthy_image.jpg"
        else:
            health_stage, image = "Healthy 🔵", "healthy_image.jpg"

        st.write(f"Health Stage: **{health_stage}**")
        
        #Display Image
        try:
            img = Image.open(f"images/{image}").resize((300, 300))
            st.image(img, use_container_width=False)
        except:
            st.info("Stage image not found.")

        #Summary Section
st.markdown("📋 Summary of Chosen Factors")

display_country = le_country.inverse_transform([country_encoded])[0]
display_status = le_status.inverse_transform([status_encoded])[0]

summary_df = pd.DataFrame({
    "Factor": [
        "Country", 
        "Status", 
        "Schooling Years", 
        "GDP per Capita", 
        "Immunization %", 
        "Adult Mortality"
    ],
    "Your Selection": [
        display_country,    
        display_status,    
        f"{Schooling} years", 
        f"${GDP:,.2f}", 
        f"{Immunization}%", 
        Adult_Mortality
    ]
})

#Display as a static table
st.table(summary_df)  
    except Exception as e:
        st.error(f"Prediction failed: {e}")


