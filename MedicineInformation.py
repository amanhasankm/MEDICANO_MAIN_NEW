import streamlit as st
from ai71 import AI71
from dotenv import load_dotenv
from streamlit_extras.let_it_rain import rain
import os

class Information:
    def __init__(self):
        load_dotenv()
        self.AI71_API_KEY = os.getenv("AI71_API_KEY")
        self.client = AI71(self.AI71_API_KEY)

    def app(self):
        # 💅 Custom CSS Styling with updated text color
        st.markdown("""
        <style>
        .med-title {
            background: linear-gradient(90deg, #000066, #3366cc);
            padding: 1rem;
            border-radius: 12px;
            text-align: center;
            margin-bottom: 2rem;
        }
        .med-title h1 {
            color: white;
            font-size: 3.5rem;
            margin: 0;
        }
        .med-title h2 {
            color: #cce6ff;
            font-size: 1.2rem;
            margin-top: 5px;
            font-weight: 400;
        }
        .info-card {
            background-color: #f8f9fa;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
            color: black; /* ✅ Sets text color to black */
        }
        </style>
        """, unsafe_allow_html=True)

        # 🌟 Title Section
        st.markdown("""
        <div class="med-title">
            <h1>💊 Medicano</h1>
            <h2>Your Personal Medical Assistant</h2>
        </div>
        """, unsafe_allow_html=True)

        # 🧾 Medicine Input Form
        with st.form("medicine_form"):
            st.subheader("📦 Medicine Description Finder")
            st.markdown("Enter the name of a medicine to get detailed info including **usage, side effects, alternatives, and global prices.**")

            medicine = st.text_input("🔍 Enter Medicine Name", placeholder="e.g., Paracetamol", help="Use generic names for best results")
            submit_medicine = st.form_submit_button("Find Description")

        if submit_medicine and medicine.strip():
            prompt = (
                f"You are provided with a medicine named '{medicine}'. Please perform the following tasks in a detailed and professional manner, ensuring that all headings are bold: \n"
                f"1. **Medicine Name and Detailed Description**\n"
                f"2. **When to Use '{medicine}'**\n"
                f"3. **Disadvantages**\n"
                f"4. **When Not to Use**\n"
                f"5. **Price Comparison in Different Countries**\n"
                f"6. **Pros and Cons**\n"
                f"Ensure the info is clear and professional, with links to authoritative sources."
            )

            with st.spinner("🤖 Fetching detailed information ..."):
                response = self.client.chat.completions.create(
                    model="tiiuae/falcon-180b-chat",
                    messages=[
                        {"role": "system", "content": "You are a medical assistant."},
                        {"role": "user", "content": prompt},
                    ],
                    stream=True,
                )

                response_content = ""
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        response_content += chunk.choices[0].delta.content

            st.markdown("## 📋 Medicine Description")
            rain(emoji="💊", font_size=28, falling_speed=4, animation_length="short")

            st.markdown(f"""
            <div class="info-card">
                {response_content}
            </div>
            """, unsafe_allow_html=True)
