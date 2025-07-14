# DiabetesChecker.py

import streamlit as st

class DiabetesCheck:
    def app(self):
        st.title("🩺 Diabetes Risk Prediction")
        st.info("Please fill in the details below:")

        col1, col2 = st.columns(2)

        with col1:
            pregnancies = st.number_input("Pregnancies", min_value=0, max_value=20, value=1)
            glucose = st.number_input("Glucose Level", min_value=0, max_value=300, value=110)
            blood_pressure = st.number_input("Blood Pressure", min_value=0, max_value=150, value=70)
            skin_thickness = st.number_input("Skin Thickness", min_value=0, max_value=100, value=20)

        with col2:
            insulin = st.number_input("Insulin", min_value=0, max_value=900, value=80)
            bmi = st.number_input("BMI", min_value=0.0, max_value=70.0, value=25.0)
            dpf = st.number_input("Diabetes Pedigree Function", min_value=0.0, max_value=2.5, value=0.5)
            age = st.number_input("Age", min_value=1, max_value=120, value=33)

        if st.button("🔍 Predict"):
            # Simple risk estimation logic
            risk_score = (glucose + bmi + age + dpf * 100) / 4
            st.subheader("📊 Prediction Result:")
            if risk_score > 120:
                st.error("⚠️ High risk of diabetes. Please consult a doctor.")
            elif risk_score > 90:
                st.warning("⚠️ Moderate risk. Consider lifestyle improvements.")
            else:
                st.success("✅ Low risk. Keep maintaining a healthy lifestyle.")

            st.markdown("📘 [Learn more](https://www.cdc.gov/diabetes/prevention/index.html)")
