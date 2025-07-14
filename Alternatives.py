import streamlit as st
from ai71 import AI71
from dotenv import load_dotenv
import os
from streamlit_extras.let_it_rain import rain

class Alternatives:
    def __init__(self):
        load_dotenv()
        self.AI71_API_KEY = os.getenv("AI71_API_KEY")
        self.client = AI71(self.AI71_API_KEY)

    def app(self):
        # 🌈 Custom CSS
        st.markdown("""
        <style>
        .alt-title {
            background: linear-gradient(90deg, #000066, #3366cc);
            padding: 1.2rem;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 2rem;
        }
        .alt-title h1 {
            color: white;
            font-size: 3.5rem;
            margin-bottom: 0;
        }
        .alt-title h2 {
            color: #cce6ff;
            font-size: 1.2rem;
            margin-top: 8px;
            font-weight: 400;
        }
        .form-container {
            background-color: #f9f9f9;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            margin-bottom: 2rem;
        }
        .response-box {
            background-color: #ffffff;
            padding: 1.5rem;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            margin-top: 2rem;
        }
        </style>
        """, unsafe_allow_html=True)

        # 🧠 Title
        st.markdown("""
        <div class="alt-title">
            <h1>💊 Medicano</h1>
            <h2>Find Affordable & Safe Medicine Alternatives</h2>
        </div>
        """, unsafe_allow_html=True)

        # 📥 Input Form
        with st.container():
            st.markdown('<div class="form-container">', unsafe_allow_html=True)
            st.subheader("🔄 Enter Medicine Details for Alternatives")

            name = st.text_input("💬 Medicine Name", placeholder="e.g., Paracetamol")
            symptoms = st.text_input("🩺 Condition/Symptoms", placeholder="e.g., Fever, Headache")
            ingredients = st.text_input("🔬 Active Ingredient (Optional)", placeholder="e.g., Acetaminophen")
            price = st.text_input("💰 Budget Preference (Optional)", placeholder="e.g., Cheaper than $5")

            st.markdown('</div>', unsafe_allow_html=True)

        # 📡 AI Prompt Setup
        prompt = (f"You are provided with the following information about a medicine:\n\n"
                  f"Medicine Name: {name}\n"
                  f"Condition/Symptoms Treated: {symptoms}\n"
                  f"Active Ingredient: {ingredients}\n"
                  f"Price Consideration: {price}\n\n"
                  "Based on this information, your task is to find and suggest alternative medicines that can be used to "
                  "treat the same condition or symptoms. Provide a detailed comparison of the alternatives, including their "
                  "active ingredients, effectiveness, safety profile, availability, and cost in various regions. Make sure to "
                  "highlight the pros and cons of each alternative. Additionally, provide any relevant research or resources "
                  "to support your suggestions.")

        # 🎯 Button + Response
        if st.button("🔎 Find Alternatives"):
            with st.spinner("Finding the best medicine alternatives..."):
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

                st.markdown("## 🧾 Suggested Alternatives")
                rain(emoji="💊", font_size=26, falling_speed=4, animation_length="short")

                st.markdown(f"""
                <div class="response-box">
                    {response_content}
                </div>
                """, unsafe_allow_html=True)
