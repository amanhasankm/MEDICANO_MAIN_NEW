import streamlit as st
import os
from datetime import datetime
from pathlib import Path

# Upload directory
UPLOAD_DIR = "uploaded_docs"
Path(UPLOAD_DIR).mkdir(exist_ok=True)

# ------------------ Helper Functions ------------------

def rename_file(old_name, new_name):
    old_path = os.path.join(UPLOAD_DIR, old_name)
    new_name = new_name.replace(" ", "_")
    new_path = os.path.join(UPLOAD_DIR, new_name)
    if os.path.exists(new_path):
        st.error("❌ A file with this name already exists.")
    else:
        os.rename(old_path, new_path)
        st.success(f"✅ Renamed to {new_name}")
        st.session_state["just_renamed"] = True

def delete_file(file):
    path = os.path.join(UPLOAD_DIR, file)
    try:
        os.remove(path)
        st.success(f"🗑️ Deleted {file}")
        st.session_state["just_deleted"] = True
    except:
        st.error("❌ Could not delete file.")

# ------------------ Main App ------------------

def app():
    st.title("📁 Medical Record Vault")
    st.markdown("Upload, filter, search, organize and share your medical documents securely.")

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
            st.warning("⚠️ Please select a file.")

    st.markdown("---")

    # ------------------ Filter & Search Section ------------------
    st.subheader("🔍 View & Manage Documents")
    filter_type = st.selectbox("📁 Filter by Type", ["All", "Prescription", "Lab Report", "Discharge Summary", "Other"])

    # Updated date filter logic
    filter_date_option = st.selectbox("📅 Filter by Date", ["Always", "Pick a Date"])
    filter_date = None
    if filter_date_option == "Pick a Date":
        filter_date = st.date_input("📅 Select a Date", datetime.today())

    search_query = st.text_input("🔎 Search by File Name")

    # Refresh on rename/delete
    if "just_renamed" in st.session_state or "just_deleted" in st.session_state:
        docs = os.listdir(UPLOAD_DIR)
        st.session_state["just_renamed"] = False
        st.session_state["just_deleted"] = False
    else:
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
                            delete_file(file)
                            st.rerun()

                    new_name = st.text_input(f"✏️ Rename File", value=file, key=f"rename_input_{i}")
                    if st.button("✅ Apply Rename", key=f"rename_btn_{i}"):
                        if new_name != file:
                            rename_file(file, new_name)
                            st.rerun()
    else:
        st.info("ℹ️ No matching documents found.")

    st.markdown("---")

    # ------------------ Share Link ------------------
    st.subheader("👨‍⚕️ Share with Doctor")
    if st.button("🔗 Generate Sharing Link"):
        username = st.session_state.get("username", "guest")
        share_url = f"https://medicano.fake/documents/view/{username}/secure123"
        st.success("🔗 Copy the link below to share:")
        st.code(share_url)
