# app.py inside PillRemainder/
import streamlit as st
from .database import save_medicine


def app():
    st.title("💊 Pill Reminder System")

    name = st.text_input("Medicine Name")
    dose = st.text_input("Dosage")
    phone = st.text_input("Your Phone Number (+91...)")
    time = st.time_input("Time to Take Medicine")

    if st.button("Save Reminder"):
        save_medicine(name, dose, phone, str(time))
        st.success("Reminder Saved!")
