import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.let_it_rain import rain
import os
import time

# Set page config
st.set_page_config(page_title="Medicano", page_icon="💊", layout="wide", initial_sidebar_state="expanded")

# Import internal modules
import Blogs, Home, Alternatives, DiagnoseDisease, MedicineInformation, NearbyPharmacies, Ambulance, About_Contact
from PillRemainder import app as PillRemainderApp
from DiabetesChecker.app import app as DiabetesCheckerApp
from auth import register_user, login_user
from MedicalDocumentVault.app import app as MedicalDocumentVaultApp

# Session state initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "popup_shown" not in st.session_state:
    st.session_state.popup_shown = False
if "popup_message" not in st.session_state:
    st.session_state.popup_message = ""

# ---------------- Header ----------------
st.markdown("<h1 style='text-align: center;'>💊 Welcome to <span style='color:#4a4aff;'>Medicano</span></h1>", unsafe_allow_html=True)

# ---------------- Login / Register ----------------
if not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])

    # --- Login Tab ---
    with tab1:
        st.markdown("### 👤 Login to your account")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.form("login_form", clear_on_submit=False):
                username = st.text_input("👨‍⚕️ Username", placeholder="Enter your username")
                password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")
                submit_login = st.form_submit_button("🚪 Login")

            if submit_login:
                success, user = login_user(username, password)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.username = user["username"]

                    # ✅ Create user folder if not exists
                    user_folder = os.path.join("uploaded_docs", st.session_state.username)
                    os.makedirs(user_folder, exist_ok=True)

                    st.success("🎉 Login successful!")
                    rain(emoji="💊", font_size=30, falling_speed=5, animation_length="medium")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials.")

    # --- Register Tab ---
    with tab2:
        st.markdown("### 🆕 Create a new account")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            new_username = st.text_input("👤 Username", key="reg_username", placeholder="Choose a username")
            new_email = st.text_input("📧 Email", key="reg_email", placeholder="Enter your email")
            new_password = st.text_input("🔐 Password", type="password", key="reg_password", placeholder="Create a password")
            confirm_password = st.text_input("🔐 Confirm Password", type="password", key="reg_confirm", placeholder="Re-enter password")

            if st.button("✅ Register"):
                if new_password != confirm_password:
                    st.warning("⚠️ Passwords do not match.")
                elif len(new_password) < 6:
                    st.warning("⚠️ Password should be at least 6 characters.")
                else:
                    success, msg = register_user(new_username, new_email, new_password)
                    if success:
                        st.session_state.popup_message = "✅ Registration successful!"
                        st.session_state.popup_shown = True
                        st.session_state.username = new_username
                    else:
                        st.error("❌ " + msg)

# ---------------- Registration Success Popup ----------------
if st.session_state.popup_shown:
    st.markdown(f"""
        <style>
            .popup {{
                background-color: #4CAF50;
                color: white;
                border-radius: 10px;
                padding: 20px;
                position: fixed;
                top: 40%;
                left: 50%;
                transform: translate(-50%, -40%);
                text-align: center;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
            }}
        </style>
        <div class="popup">
            <h3>{st.session_state.popup_message}</h3>
            <p>Please login from the Login tab.</p>
        </div>
    """, unsafe_allow_html=True)

    time.sleep(3)
    st.session_state.popup_shown = False
    st.experimental_rerun()

# ---------------- Load App If Logged In ----------------
if st.session_state.logged_in:

    class MultiApp:
        def __init__(self):
            self.apps = []

        def add_apps(self, title, function):
            self.apps.append({"title": title, "function": function})

        def run(self):
            titles = [app['title'] for app in self.apps]

            with st.sidebar:
                st.markdown(f"👋 Logged in as **{st.session_state.username}**")

                if st.button("🚪 Logout"):
                    st.session_state.logged_in = False
                    st.session_state.username = ""
                    st.rerun()

                app_title = option_menu(
                    menu_title='Medicano',
                    options=titles,
                    icons=['house-fill', 'heart-pulse', 'capsule', 'info-circle', 'journal-text',
                           'geo-alt', 'exclamation-triangle-fill', 'bell', 'activity', 'info-square-fill', 'file-earmark-text'],
                    menu_icon='chat-text-fill',
                    default_index=0,
                    styles={
                        "container": {"padding": "5!important", "background-color": 'white'},
                        "icon": {"color": "black", "font-size": "23px"},
                        "nav-link": {"color": "black", "font-size": "20px", "text-align": "left"},
                        "nav-link-selected": {"background-color": "#f0f0f0"}
                    }
                )

            selected_app = next((app for app in self.apps if app['title'] == app_title), None)
            if selected_app:
                selected_app['function']()

    # Register all app pages
    Medical = MultiApp()
    Medical.add_apps("Home", Home.Homes.app)
    Medical.add_apps("Diagnose Disease", lambda: DiagnoseDisease.Diagnose().app())
    Medical.add_apps("Diabetes Checker", DiabetesCheckerApp)
    Medical.add_apps("Medicine Alternatives", lambda: Alternatives.Alternatives().app())
    Medical.add_apps("Medicine Information", lambda: MedicineInformation.Information().app())
    Medical.add_apps("Nearby Pharmacies", lambda: NearbyPharmacies.Pharmacies().app())
    Medical.add_apps("Blogs", lambda: Blogs.Blogs().app())
    Medical.add_apps("Emergency Ambulance", lambda: Ambulance.AmbulanceFinder().app())
    Medical.add_apps("Pill Reminder", PillRemainderApp)
    Medical.add_apps("About&Contact", lambda: About_Contact.app())
    Medical.add_apps("Health Records", MedicalDocumentVaultApp)

    Medical.run()
