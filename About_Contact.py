import streamlit as st

def app():
    # About & Contact Page content
    st.title("About & Contact")

    # About section
    st.subheader("About Medicano")
    st.write("""
    Medicano is a Smart Medical Assistant that helps users with various health-related tasks such as:
    - Disease diagnosis
    - Medicine information
    - Nearby pharmacies
    - Medicine alternatives
    - Health blogs
    - Emergency services (like Ambulance Finder)
    """)

    # Contact section
    st.subheader("Contact Us")
    st.write("""
    For any inquiries, suggestions, or feedback, please reach out to us:
    
    **Email**: contact@medicano.com  
    **Phone**: +123-456-7890
    """)

    # Team section
    st.subheader("Meet Our Team")
    st.write("""
    Our team is dedicated to providing you with the best health assistance. The team members are:
    
    - Yashas Kumar
    - Aman Hasan
    - Sujal R Bangera
    - Madhukar
    """)

    st.write("Thank you for using Medicano!")
