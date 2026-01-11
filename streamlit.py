import pickle
import streamlit as st
import pandas as pd
from PIL import Image

#Load trained model
with open("life_expectancy_app.pkl", "rb") as f:
    model_package = pickle.load(f)

model = model_package["model"]
le = model_package["label_encoder"]
columns_order = model_package["columns"]

#Sidebar (Student info and logo)
st.sidebar.markdown("---")
try:
    # Replace 'images/parami_logo.png' with your actual file path
    logo = Image.open("images/parami_logo.png") 
    st.sidebar.image(logo, use_container_width=True)
except Exception:
    st.sidebar.error("Logo not found. Please add 'parami_logo.png' to the images folder.")

st.sidebar.subheader("Student Information")
st.sidebar.write("**Ei Mon Soe**")
st.sidebar.write("Data Science Senior Student")
st.sidebar.write("Parami University")
st.sidebar.markdown("---") 

#App Title
st.title("🌍 Life Expectancy Prediction App")
try:
    header_img = Image.open("images/life_banner.jpg")
    st.image(header_img, use_container_width=True)
except Exception as e:
    st.warning("Banner image not found. Please place 'life_banner.jpg' in the images folder.")

st.sidebar.header("How it works")
st.sidebar.markdown("""
1. Input immunization factors, mortality factors, and socio-economic information.  
2. Click **Predict Life Expectancy**.  
3. See life stage:
   - Critical 🔴, 
   - At Risk 🟠,
   - Unhealthy 🟢, and 
   - Healthy 🔵.  
""")

#High Importance
Schooling = st.slider("📚 Schooling - Years ", min_value=0.0, value=12.0, step=0.1)
Income_comp = st.slider("💵 Income Composition - Human Development Index (HDI)", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
GDP = st.number_input("💰 GDP per Capita (USD)", min_value=0.0, value=5000.0, step=100.0)
Immunization = st.slider("💉 Immunization - Average of Hepatitis B, Polio, Diphtheria", min_value=0.0, max_value=100.0, value=95.0)
Alcohol = st.selectbox("🍷 Alcohol - Consumption per Liters", ["None", "Low (0-2)", "Moderate (2-5)", "High (>5)"])
Adult_Mortality = st.selectbox("Adult Mortality", ["Low (<150)", "Medium (150-250)", "High (>250)"])
HIV_AIDS = st.number_input("HIV/AIDS - Deaths per 1000 live births", min_value=0.0, value=0.1, step=0.01)
BMI = st.number_input("BMI - Body Mass Index", min_value=0.0, value=25.0, step=0.1)

#Medium Importance
percentage_expenditure = st.selectbox("🏥 Health Expenditure per Capita", ["Low (<5%)", "Medium (5-10%)", "High (>10%)"])
Total_expenditure = st.selectbox("🏛️ Government Health Spending", ["Low (<5%)", "Medium (5-10%)", "High (>10%)"])
under_five = st.selectbox("🧒 Under-Five Deaths", ["Low (<20)", "Medium (20-100)", "High (>100)"])

#Low Importance
thinness_mean = st.number_input("👶 Prevalence of Thinness", min_value=0.0, value=0.2, step=0.01)
Status = st.selectbox("🌎 Country Status", ["Developed", "Developing"])

Status_encoded = le.transform([Status])[0]

adult_mortality_map = {"Low (<150)": 100, "Medium (150-250)": 200, "High (>250)": 300}
alcohol_map = {"None": 0.0, "Low (0-2)": 1.0, "Moderate (2-5)": 3.0, "High (>5)": 6.0}
percentage_map = {"Low (<5%)": 2.0, "Medium (5-10%)": 7.0, "High (>10%)": 12.0}
total_exp_map = {"Low (<5%)": 2.0, "Medium (5-10%)": 7.0, "High (>10%)": 12.0}
under_five_map = {"Low (<20)": 10, "Medium (20-100)": 50, "High (>100)": 150}

Adult_Mortality_val = adult_mortality_map[Adult_Mortality]
Alcohol_val = alcohol_map[Alcohol]
percentage_val = percentage_map[percentage_expenditure]
Total_expenditure_val = total_exp_map[Total_expenditure]
under_five_val = under_five_map[under_five]


input_data = pd.DataFrame({
    "Adult Mortality": [Adult_Mortality_val],
    "Alcohol": [Alcohol_val],
    "percentage expenditure": [percentage_val],
    " BMI ": [BMI],
    "under-five deaths ": [under_five_val],
    "Total expenditure": [Total_expenditure_val],
    " HIV/AIDS": [HIV_AIDS],
    "GDP": [GDP],
    "Income composition of resources": [Income_comp],
    "Schooling": [Schooling],
    "Status_encoded": [Status_encoded],
    "Immunization": [Immunization],
    "thinness_mean": [thinness_mean]
})
input_data = input_data[columns_order]

#Prediction button
if st.button("Predict Life Expectancy"):
    try:
        prediction = model.predict(input_data)[0]
        rounded_prediction = round(prediction)
        st.success(f"Predicted Life Expectancy: **{rounded_prediction} years**")
#Categorize into four health stages 
        if prediction <= 45:
            health_stage = "Critical 🔴"
            image = "critical_image.jpg"  
        elif prediction <= 55:
            health_stage = "At Risk 🟠"
            image = "at_risk_image.jpg"  
        elif prediction <= 70:
            health_stage = "UnHealthy 🟢"
            image = "unhealthy_image.jpg"  
        else:
            health_stage = "Healthy 🔵"
            image = "healthy_image.jpg"  

        st.write(f"Health Stage: **{health_stage}**")
        img = Image.open(f"images/{image}")
        img = img.resize((300, 300))
        st.image(img, use_container_width=False)
    except Exception as e:
        st.error(f"Prediction failed: {e}")



