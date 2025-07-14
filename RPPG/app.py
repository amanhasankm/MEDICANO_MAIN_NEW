import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(__file__))  # Adds RPPG folder to path

from models.video_processing import process_video


def app():
    st.title("🩺 RPPG - Remote Vital Detection via Webcam")

    if st.button("Start RPPG"):
        with st.spinner("Capturing and analyzing video..."):
            result = process_video()

        if result:
            heart_rate, respiration_rate, spO2, stress, hrv, blood_pressure, emotion = result
            st.success(f"Heart Rate: {heart_rate} BPM")
            st.success(f"Respiration Rate: {respiration_rate} breaths/min")
            st.success(f"SpO₂: {spO2}%")
            st.success(f"Stress Level: {stress}")
            st.success(f"HRV: {hrv} ms")
            st.success(f"Blood Pressure: {blood_pressure} mmHg")
            st.success(f"Emotion: {emotion}")

    st.markdown("""
    ⚠️ **Instructions**:
    - Sit still and face the webcam
    - Ensure good lighting
    - Avoid facial obstructions

    🔍 **Metrics Extracted**:
    - Heart Rate (via green channel)
    - Respiration Rate (via red channel)
    - HRV (Heart Rate Variability)
    - Blood Pressure (Estimated)
    - Stress & Emotion (Basic classifier)
    """)
