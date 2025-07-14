import streamlit as st
from ai71 import AI71
from dotenv import load_dotenv
import os
import pdfkit
import tempfile

# Required as first Streamlit command
#st.set_page_config(page_title="Medicano Diagnosis", page_icon="🧠", layout="centered")

class Diagnose:
    def __init__(self):
        load_dotenv()
        self.AI71_API_KEY = os.getenv("AI71_API_KEY")
        self.client = AI71(self.AI71_API_KEY)

    def app(self):
        options = [
            "🤒 Fever", "🤧 Cough", "🤕 Headache", "🥱 Fatigue", "🤢 Nausea",
            "🤮 Vomiting", "😤 Sore throat", "🤧 Runny nose", "💪 Muscle pain",
            "😮‍💨 Shortness of breath"
        ]

        # Styling
        st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
            html, body, [class*="css"] {
                font-family: 'Poppins', sans-serif;
            }
            .title-box {
                background: linear-gradient(to right, #00c6ff, #0072ff);
                padding: 30px;
                border-radius: 15px;
                text-align: center;
                color: white;
                margin-bottom: 30px;
            }
            .stButton>button {
                background: linear-gradient(135deg, #00c6ff, #0072ff);
                color: white;
                border: none;
                border-radius: 50px;
                font-size: 16px;
                padding: 0.7em 2em;
                transition: all 0.3s ease-in-out;
            }
            .stButton>button:hover {
                background: linear-gradient(135deg, #0072ff, #00c6ff);
                transform: scale(1.05);
            }
            .diagnosis-result {
                background: #f5faff;
                padding: 30px;
                border-radius: 20px;
                box-shadow: 0px 0px 15px rgba(0, 114, 255, 0.1);
                margin-top: 30px;
            }

            /* Custom cursor for selectbox */
            .stSelectbox select {
                cursor: pointer !important;
            }
        </style>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="title-box">
            <h1>Medicano</h1>
            <h2>AI-Powered Symptom Checker</h2>
        </div>
        """, unsafe_allow_html=True)

        with st.form("diagnose_form"):
            name = st.text_input(" Your Name")
         
            gender = st.selectbox(" Gender", ["Prefer not to say", "Male", "Female", "Other"])

            symptoms = st.multiselect("🩺 Select Your Symptoms", options)
            submit_diagnose = st.form_submit_button("🔍 Diagnose Now")

        if submit_diagnose:
            if not symptoms:
                st.warning("Please select at least one symptom.")
                return

            with st.spinner("Analyzing symptoms... This might take a few seconds 💭"):
                clean_symptoms = [sym.strip("🩺🤒🤧🤕🥱🤢🤮😤🤧💪😮‍💨") for sym in symptoms]
                prompt = (
                    f"You are a medical assistant diagnosing a patient.\n\n"
                    f"Patient Info:\n"
                    f"Name: {name or 'Anonymous'}\n"
                
                    f"Gender: {gender}\n"
                    f"Symptoms: {', '.join(clean_symptoms)}\n\n"
                    f"Provide a diagnosis with the following format:\n"
                    f"- **Disease Name**\n"
                    f"- **Brief History**\n"
                    f"- **Causes**\n"
                    f"- **Symptoms**\n"
                    f"- **Possible Side Effects**\n"
                    f"- **Preventive and Curative Measures** (detailed)\n"
                    f"- **Medicinal Recommendations** (general OTC or common drugs)\n"
                    f"- **When to Seek Emergency Help**\n"
                    f"- **External References** (Markdown links if available)"
                )

                response = self.client.chat.completions.create(
                    model="tiiuae/falcon-180b-chat",
                    messages=[{"role": "system", "content": "You are a medical assistant."},
                              {"role": "user", "content": prompt}],
                    stream=True,
                )

                response_content = ""
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        response_content += chunk.choices[0].delta.content

            # ✅ Display the diagnosis result
            st.markdown('<div class="diagnosis-result">', unsafe_allow_html=True)
            st.markdown("### 🧠 Diagnosis Result")
            st.markdown(response_content, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # ✅ Generate PDF and provide download button
            try:
                config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
                html_content = f"<h1>Diagnosis Report</h1><div>{response_content}</div>"

                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                    pdfkit.from_string(html_content, tmp_pdf.name, configuration=config)
                    with open(tmp_pdf.name, "rb") as file:
                        st.download_button(
                            label="📄 Download Diagnosis as PDF",
                            data=file,
                            file_name=f"{name or 'diagnosis'}_report.pdf",
                            mime="application/pdf"
                        )
            except Exception as e:
                st.error(f"PDF generation failed: {e}")
