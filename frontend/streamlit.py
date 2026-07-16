import streamlit as st
import requests

# -----------------------------
# Backend URL
# -----------------------------
API_URL = "https://lcms-assistant.onrender.com"

st.set_page_config(
    page_title="LC-MS AI Assistant",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 LC-MS Troubleshooting Assistant")

st.write(
    "Upload a scientific paper, SOP, or instrument manual and describe your LC-MS issue."
)

# -----------------------------
# Upload document
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload Reference Document",
    type=["pdf"]
)

# -----------------------------
# Symptom
# -----------------------------
symptom = st.text_area(
    "Describe the LC-MS issue",
    placeholder="Example: LC-MS signal intensity dropped by 80% after installing a new C18 column."
)

# -----------------------------
# Analyze
# -----------------------------
if st.button("Analyze"):

    if uploaded_file is None:
        st.error("Please upload a PDF document.")
        st.stop()

    if symptom.strip() == "":
        st.error("Please describe the LC-MS issue.")
        st.stop()

    with st.spinner("Analyzing..."):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file,
                "application/pdf"
            )
        }

        data = {
            "symptom": symptom
        }

        response = requests.post(
            f"{API_URL}/troubleshoot",
            files=files,
            data=data,
            timeout=120
        )

    if response.status_code == 200:

        result = response.json()

        st.success("Analysis Complete")

        st.subheader("Problem Category")
        st.write(result["problem_category"])

        st.subheader("Likely Causes")

        for cause in result["likely_causes"]:

            st.write(f"**{cause['problem_type']}**")

            st.write(f"Cause: {cause['likely_cause']}")

            st.write(f"Recommendation: {cause['recommended_check']}")

            st.write(f"Severity: {cause['severity']}")

            st.divider()

        st.subheader("Follow-up Questions")

        for question in result["follow_up_questions"]:
            st.write("- " + question)

        st.subheader("Scientist Summary")

        st.write(result["scientist_summary"])

    else:

        st.error(f"HTTP {response.status_code}")

        st.write(response.text)
