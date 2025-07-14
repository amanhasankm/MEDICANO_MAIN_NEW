import streamlit as st
import os
from datetime import datetime
from pathlib import Path

# 🔒 Restrict access to logged-in users
def app():
    if not st.session_state.get("logged_in", False):
        st.warning("🔒 You must be logged in to access the Document Vault.")
        return

    username = st.session_state.get("username", "guest")
    UPLOAD_DIR = os.path.join("uploaded_docs", username)
    Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

    st.title("📁 Medical Record Vault")
    st.markdown(f"Manage your medical documents securely.\n\n👤 **User:** `{username}`")

    # ------------------ Upload Section ------------------
    st.subheader("📤 Upload Document")
    doc_type = st.selectbox("📂 Document Type", ["Prescription", "Lab Report", "Discharge Summary", "Other"])
    uploaded_file = st.file_uploader("Upload PDF/Image", type=["pdf", "png", "jpg", "jpeg"])
    upload_date = st.date_input("📅 Document Date", datetime.today())
    custom_name = st.text_input("✏️ Custom File Name (Optional)", placeholder="e.g. blood_test_report")

    if st.button("📤 Upload"):
        if uploaded_file:
            safe_name = custom_name.strip().replace(" ", "_") if custom_name else uploaded_file.name.replace(" ", "_")
            filename = f"{upload_date}_{doc_type.replace(' ', '_')}_{safe_name}"
            filepath = os.path.join(UPLOAD_DIR, filename)
            with open(filepath, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"✅ Uploaded as `{filename}`")
        else:
            st.warning("⚠️ Please select a file to upload.")

    st.markdown("---")

    # ------------------ Filter & Search Section ------------------
    st.subheader("🔍 View & Manage Documents")
    filter_type = st.selectbox("📁 Filter by Type", ["All", "Prescription", "Lab Report", "Discharge Summary", "Other"])
    filter_date_option = st.selectbox("📅 Filter by Date", ["Always", "Pick a Date"])
    filter_date = None
    if filter_date_option == "Pick a Date":
        filter_date = st.date_input("📅 Select a Date", datetime.today())
    search_query = st.text_input("🔎 Search by File Name")

    docs = os.listdir(UPLOAD_DIR)
    filtered_docs = []
    for doc in docs:
        if filter_type != "All" and filter_type.replace(" ", "_") not in doc:
            continue
        if filter_date and filter_date.strftime("%Y-%m-%d") not in doc:
            continue
        if search_query.lower() not in doc.lower():
            continue
        filtered_docs.append(doc)

    # ------------------ Display Files ------------------
    if filtered_docs:
        for i, file in enumerate(sorted(filtered_docs)):
            file_path = os.path.join(UPLOAD_DIR, file)
            with open(file_path, "rb") as f:
                with st.expander(f"📄 {file}"):
                    col1, col2 = st.columns([1, 1])

                    with col1:
                        st.download_button(
                            label="⬇️ Download",
                            data=f,
                            file_name=file,
                            mime="application/octet-stream",
                            key=f"download_{i}"
                        )

                    with col2:
                        if st.button("🗑️ Delete", key=f"delete_{i}"):
                            try:
                                os.remove(file_path)
                                st.success(f"🗑️ Deleted {file}")
                                st.rerun()
                            except:
                                st.error("❌ Could not delete file.")

                    new_name = st.text_input(f"✏️ Rename File", value=file, key=f"rename_input_{i}")
                    if st.button("✅ Apply Rename", key=f"rename_btn_{i}"):
                        new_path = os.path.join(UPLOAD_DIR, new_name.replace(" ", "_"))
                        if os.path.exists(new_path):
                            st.error("❌ A file with this name already exists.")
                        else:
                            os.rename(file_path, new_path)
                            st.success(f"✅ Renamed to {new_name}")
                            st.rerun()
    else:
        st.info("ℹ️ No matching documents found.")

    st.markdown("---")

    # ------------------ Share Link ------------------
    st.subheader("👨‍⚕️ Share with Doctor")
    if st.button("🔗 Generate Sharing Link"):
        fake_token = "secure123"  # TODO: Implement real token logic later
        share_url = f"https://medicano.fake/documents/view/{username}/{fake_token}"
        st.success("🔗 Copy the link below to share:")
        st.code(share_url)
