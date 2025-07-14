import sys
import os
import numpy as np
import pandas as pd  # Needed to fix the warning
import streamlit as st
import joblib

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load the trained model and scaler
model_path = os.path.join(os.path.dirname(__file__), '..', 'pcos_model', 'pcos_model.pkl')
scaler_path = os.path.join(os.path.dirname(__file__), '..', 'pcos_model', 'scaler.pkl')

model = joblib.load(os.path.abspath(model_path))
scaler = joblib.load(os.path.abspath(scaler_path))

def predict_pcos(features):
    """
    Predict whether the patient has PCOS based on input features.
    Scales the features and uses the trained model for prediction.
    """
    # Match feature names used during training exactly
    columns = ['Age', 'BMI', 'Menstrual_Irregularity', 'Testosterone_Level(ng/dL)', 'Antral_Follicle_Count']

    # Convert to DataFrame with correct column names
    features_df = pd.DataFrame(features, columns=columns)

    # Scale the features using the saved scaler
    features_scaled = scaler.transform(features_df)

    # Predict using the model
    prediction = model.predict(features_scaled)

    return prediction[0]

def app():
    # Set the title of the app
    st.title("🩺 PCOS Prediction")

    # Track whether the "Start Prediction" button was clicked
    if 'start_clicked' not in st.session_state:
        st.session_state.start_clicked = False

    # Show instructions and start button
    if not st.session_state.start_clicked:
        st.markdown(""" 
        ## Instructions

        This tool helps predict whether you might have Polycystic Ovary Syndrome (PCOS) based on certain health markers. 
        Enter the following values:

        - Age: Age of the person.
        - BMI: Body Mass Index.
        - Menstrual Irregularity: Whether there is any menstrual irregularity (1 = Yes, 0 = No).
        - **Testosterone Level**: The level of testosterone in ng/dL.
        - **Antral Follicle Count**: The number of antral follicles in the ovaries.

        After entering the values, click **Start Prediction** to receive your result.
        """)

        # Button to start the prediction
        if st.button("🔍 Start Prediction"):
            st.session_state.start_clicked = True
            st.rerun()

    # Show input fields after start
    if st.session_state.start_clicked:
        st.subheader("Enter the following health details:")

        with st.form("pcos_form"):
            age = st.number_input("Age", min_value=0, max_value=100, help="Enter your age", key="age_input")
            bmi = st.number_input("BMI", min_value=10.0, max_value=50.0, help="Enter your BMI", key="bmi_input")
            menstrual_irregularity = st.selectbox("Menstrual Irregularity", [0, 1], help="1 = Yes, 0 = No", key="irregularity_input")
            testosterone_level = st.number_input("Testosterone Level (ng/dL)", min_value=0.0, max_value=200.0, help="Enter testosterone level", key="testosterone_input")
            antral_follicle_count = st.number_input("Antral Follicle Count", min_value=0, max_value=50, help="Enter the number of antral follicles", key="follicle_input")

            submitted = st.form_submit_button("🔍 Predict")

            if submitted:
                if age <= 0 or bmi <= 0 or testosterone_level <= 0 or antral_follicle_count <= 0:
                    st.warning("Please enter valid values for all fields to proceed with the prediction.")
                else:
                    features = np.array([[age, bmi, menstrual_irregularity, testosterone_level, antral_follicle_count]])
                    result = predict_pcos(features)

                    if result == 1:
                        st.markdown(
                            """
                            <div style="background-color: #f8d7da; padding: 15px; border-radius: 8px; color: #721c24; font-size: 18px; font-weight: bold;">
                                <span style="font-size: 24px;">⚠️</span> <strong>You might have PCOS</strong><br>
                                It’s important to consult a gynecologist for further diagnosis and advice. Stay safe and take care!
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.markdown(
                            """
                            <div style="background-color: #d4edda; padding: 15px; border-radius: 8px; color: #155724; font-size: 18px; font-weight: bold;">
                                <span style="font-size: 24px;">✅</span> <strong>You are unlikely to have PCOS</strong><br>
                                Keep up with a healthy lifestyle, but remember to monitor your health regularly.
                            </div>
                            """, unsafe_allow_html=True)

    # Optional: Styling
    st.markdown("""
    <style>
    .custom-container {
        background-color: #F3F4F6;
        padding: 20px;
        border-radius: 8px;
        box-shadow: none;
    }
    h1 {
        font-size: 32px;
        font-weight: bold;
        color: #2C3E50;
    }
    p, label, .stMarkdown, .stNumberInput, .stSelectbox {
        font-size: 16px !important;
        color: #34495E !important;
        filter: none !important;
    }
    input:focus, select:focus, textarea:focus {
        backdrop-filter: none !important;
        filter: none !important;
        outline: 2px solid #2980B9;
    }
    </style>
    """, unsafe_allow_html=True)

    # Optional: Footer
    st.markdown("""
    <footer style="text-align: center; padding: 20px;">
        <p style="font-size: 14px; color: #BDC3C7;">Made with ❤️ by the Medical Team | <a href="https://example.com" style="color: #2980B9;">Learn More</a></p>
    </footer>
    """, unsafe_allow_html=True)
