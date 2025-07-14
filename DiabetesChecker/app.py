# DiabetesChecker/app.py
import streamlit as st

def app():
    st.title("🩸 Diabetes Risk Checker")

    st.markdown("### Enter your health metrics:")

    pregnancies = st.number_input("Pregnancies", 0, 20, 1)
    glucose = st.number_input("Glucose Level", 0, 300, 110)
    blood_pressure = st.number_input("Blood Pressure", 0, 180, 70)
    skin_thickness = st.number_input("Skin Thickness", 0, 100, 20)
    insulin = st.number_input("Insulin Level", 0, 900, 85)
    bmi = st.number_input("BMI", 0.0, 70.0, 24.0)
    diabetes_pedigree = st.number_input("Diabetes Pedigree Function", 0.0, 2.5, 0.5)
    age = st.number_input("Age", 1, 100, 30)

    if st.button("🔍 Predict"):
        if glucose > 130 or bmi > 30 or age > 45:
            st.error("⚠️ You may be at risk of diabetes. Please consult your doctor.")
        else:
            st.success("✅ You are likely not diabetic. Stay healthy!")
