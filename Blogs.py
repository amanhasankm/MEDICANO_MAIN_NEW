import streamlit as st
from ai71 import AI71
from dotenv import load_dotenv
import os


class Blogs:
    def __init__(self):
        load_dotenv()
        self.AI71_API_KEY = os.getenv("AI71_API_KEY")
        self.client = AI71(self.AI71_API_KEY)

    def app(self):
        # Title section with styling
        st.markdown("""
            <div style="background: linear-gradient(to right, #0072ff, #00c6ff); text-align: center; padding: 30px; border-radius: 15px; margin-bottom: 30px; box-shadow: 0 4px 12px rgba(0,0,0,0.2);">
              <h1 style="color: white; font-size: 60px; margin: 0;">Medicano</h1>
              <h3 style="color: white; font-weight: 300;">Your Trusted Medical Assistant</h3>
            </div>
        """, unsafe_allow_html=True)

        topic = st.text_input("🔍 Enter a Medical Topic for Blogs & Articles")

        if st.button("Find Blogs"):
            if topic.strip() == "":
                st.warning("Please enter a valid topic.")
                return

            with st.spinner("Fetching blogs and references... ⏳"):

                # Better prompt for accurate blog results
                prompt = (
                    f"Generate 5 blog titles and 5 reference articles related to the medical topic: **{topic}**.\n\n"
                    "Present them in a markdown table format with the following columns:\n"
                    "- **Title**\n"
                    "- **Summary**\n"
                    "- **Source/Author**\n"
                    "- **Date (if known)**\n"
                    "- **Link**\n\n"
                    "Ensure the blogs are diverse and helpful for readers. Use markdown table format only."
                )

                # Stream AI response
                response = self.client.chat.completions.create(
                    model="tiiuae/falcon-180b-chat",
                    messages=[
                        {"role": "system", "content": "You are a helpful medical blog assistant."},
                        {"role": "user", "content": prompt},
                    ],
                    stream=True,
                )

                response_content = ""
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        response_content += chunk.choices[0].delta.content

            st.subheader(f"📝 Blogs & References for: {topic}")
            st.markdown(response_content, unsafe_allow_html=True)
