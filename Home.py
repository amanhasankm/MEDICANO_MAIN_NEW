import streamlit as st
import time

# Import sub-feature apps
from PCOS.pcospredicter.pcos_predicter import app as PCOSApp
from RPPG.app import app as RPPGApp
from PCOS.Diet_Plan_Generator.dietplanner import app as DP
from DiabetesChecker import app as DiabetesCheckerApp

class Homes:
    @staticmethod
    def app():
        # Session states
        if "selected_feature" not in st.session_state:
            st.session_state.selected_feature = None
        if "pcos_subfeature" not in st.session_state:
            st.session_state.pcos_subfeature = None

        # Back to Home Button (Floating Top-Left)
        if st.session_state.selected_feature:
            st.markdown("""
                <style>
                    .top-left-button {
                        position: absolute;
                        top: 20px;
                        left: 20px;
                        background-color: #000000;
                        color: white;
                        border: none;
                        padding: 10px 20px;
                        border-radius: 8px;
                        font-size: 16px;
                        cursor: pointer;
                        z-index: 9999;
                    }
                    .top-left-button:hover {
                        background-color: #333333;
                    }
                </style>
                <script>
                    const backBtn = document.querySelector("button[aria-label='🔙 Back to Home']");
                    if (backBtn) backBtn.classList.add("top-left-button");
                </script>
            """, unsafe_allow_html=True)

            if st.button("🔙 Back to Home", key="top_back_button"):
                st.session_state.selected_feature = None
                st.session_state.pcos_subfeature = None
                st.rerun()

        # Header Styling
        st.markdown("""
        <style>
        .header-container {
            background: linear-gradient(135deg, #003366, #006699);
            border-radius: 10px;
            padding: 30px 20px;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }

        .header-container h1 {
            color: white;
            font-size: 60px;
            margin-bottom: 10px;
        }

        .header-container h2 {
            color: #e0e0e0;
            font-size: 22px;
        }

        .stButton button {
            width: 100%;
            height: 80px;
            font-size: 24px;
            background-color: #006699;
            color: white;
            border-radius: 10px;
            border: none;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }

        .stButton button:hover {
            background-color: #004466;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        }
        </style>
        """, unsafe_allow_html=True)

        # Header Content
        st.markdown("""
        <div class="header-container">
            <h1>Medicano</h1>
            <h2>A Smart Medical Assistant</h2>
        </div>
        """, unsafe_allow_html=True)

        # Selected Feature Logic
        if st.session_state.selected_feature == "PCOS":
            st.subheader("💊 PCOS Tools")

            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("🧬 PCOS Predictor", key="pcos_predictor_btn"):
                    st.session_state.pcos_subfeature = "predictor"
                    st.rerun()
            with col2:
                if st.button("🥗 Diet Plan Generator", key="diet_plan_btn"):
                    st.session_state.pcos_subfeature = "diet"
                    st.rerun()

            # Sub-feature loaders
            if st.session_state.pcos_subfeature == "predictor":
                with st.spinner("🔄 Loading PCOS Predictor..."):
                    time.sleep(1)
                    PCOSApp()
            elif st.session_state.pcos_subfeature == "diet":
                with st.spinner("🔄 Loading Diet Plan Generator..."):
                    time.sleep(1)
                    DP()

        elif st.session_state.selected_feature == "RPPG":
            with st.spinner("🔄 Loading RPPG..."):
                time.sleep(1.5)
                RPPGApp()

        elif st.session_state.selected_feature == "Diabetes":
            with st.spinner("🔄 Loading Diabetes Checker..."):
                time.sleep(1.5)
                DiabetesCheckerApp()

        else:
            # Main Home Screen Buttons (Large Size)
            col1, col2 = st.columns(2)

            with col1:
                if st.button("🩺 RPPG", key="rppg_btn"):
                    st.session_state.selected_feature = "RPPG"
                    st.rerun()

                if st.button("🩸 Diabetes Check", key="diabetes_btn"):
                    st.session_state.selected_feature = "Diabetes"
                    st.rerun()

            with col2:
                if st.button("🧬 PCOS Management", key="pcos_btn"):
                    st.session_state.selected_feature = "PCOS"
                    st.rerun()
