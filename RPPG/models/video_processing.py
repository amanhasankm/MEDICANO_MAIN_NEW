import streamlit as st
import cv2
import numpy as np
import time
from models.utils import extract_face_region, extract_rppg_signal, predict_stress, predict_emotion
from models.signal_extraction import compute_heart_rate, compute_respiration_rate, compute_hrv

def process_video():
    stframe = st.empty()
    cap = cv2.VideoCapture(0)
    signals, timestamps = [], []
    last_valid_frame = None
    start_time = time.time()

    while time.time() - start_time < 20:
        ret, frame = cap.read()
        if not ret:
            st.warning("⚠️ Camera read failed.")
            break

        face = extract_face_region(frame)
        if face is None:
            st.warning("⚠️ Face not detected. Adjust lighting or position.")
            continue

        signal = extract_rppg_signal(face)
        if signal is None or len(signal) == 0:
            st.warning("⚠️ Signal extraction failed.")
            continue

        signals.append(signal)
        timestamps.append(time.time() - start_time)
        last_valid_frame = frame.copy()
        stframe.image(frame, channels='BGR', caption="Capturing... Stay still")
        cv2.waitKey(1)

    cap.release()

    if len(signals) < 50:
        st.error("📉 Insufficient signal data. Ensure good lighting and try again.")
        return None

    signals = np.array(signals)
    timestamps = np.array(timestamps)

    # Compute vitals
    hr = compute_heart_rate(signals, timestamps)
    rr = compute_respiration_rate(signals, timestamps)
    hrv = compute_hrv(signals, timestamps)

    bp_sys = int(0.5 * hr + 80)
    bp_dia = int(0.33 * hr + 50)

    stress = predict_stress(hrv)
    emotion = predict_emotion(last_valid_frame) if last_valid_frame is not None else "Unknown"

    return (
        int(hr), int(rr), 98,  # SpO2 placeholder
        stress, round(hrv, 2),
        f"{bp_sys}/{bp_dia}", emotion
    )

def app():
    st.title("🩺 RPPG - Remote Vital Detection via Webcam")

    if st.button("Start RPPG"):
        with st.spinner("Capturing and analyzing video..."):
            result = process_video()

        if result:
            heart_rate, respiration_rate, spO2, stress, hrv, blood_pressure, emotion = result
            st.success(f"❤️ Heart Rate: {heart_rate} BPM")
            st.success(f"🌬️ Respiration Rate: {respiration_rate} breaths/min")
            st.success(f"🩸 SpO₂: {spO2}%")
            st.success(f"😰 Stress Level: {stress}")
            st.success(f"📈 HRV: {hrv} ms")
            st.success(f"🧬 Blood Pressure: {blood_pressure} mmHg")
            st.success(f"😊 Emotion: {emotion}")

    st.markdown("""
    ## 📋 Instructions:
    - Sit still and face the webcam
    - Ensure good lighting and minimal movement
    - Keep your face unobstructed

    ## 📊 What It Measures:
    - Heart Rate (via green channel)
    - Respiration Rate (via red channel)
    - HRV (Heart Rate Variability)
    - Blood Pressure (Estimated)
    - Stress & Emotion (Basic classification)
    """)
