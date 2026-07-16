import streamlit as st
import requests


API_URL = "https://lcms-assistant.onrender.com"


st.set_page_config(
    page_title="LC-MS AI Assistant",
    page_icon="🔬"
)


st.title("🔬 LC-MS Troubleshooting Assistant")


# -------------------------
# Upload document
# -------------------------

uploaded_file = st.file_uploader(
    "Upload LC-MS Paper / SOP / Manual",
    type=["pdf"]
)


if uploaded_file:

    if st.button("Upload Document"):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "application/pdf"
            )
        }


        response = requests.post(
            f"{API_URL}/upload",
            files=files,
            timeout=120
        )


        if response.status_code == 200:
            st.success("Document uploaded successfully")

        else:
            st.error(response.text)



# -------------------------
# Troubleshooting question
# -------------------------

symptom = st.text_area(
    "Describe LC-MS problem",
    placeholder=
    "Example: LC-MS signal intensity dropped by 80% after installing a new column"
)



if st.button("Analyze"):


    if not symptom:

        st.warning(
            "Please describe the problem"
        )

        st.stop()



    payload = {
    "symptom": symptom,
    "instrument": instrument,
    "analyte_type": analyte_type,
    "ionization_mode": ionization_mode,
    "column_type": column_type,
    "mobile_phase": mobile_phase,
    "recent_changes": recent_changes
    }


    response = requests.post(

        f"{API_URL}/troubleshoot",

        json=payload,

        timeout=120

    )


    if response.status_code == 200:

        result = response.json()


        st.subheader("Problem Category")

        st.write(
            result["problem_category"]
        )


        st.subheader("Likely Causes")


        for cause in result["likely_causes"]:

            st.write(
                f"**{cause['problem_type']}**"
            )

            st.write(
                cause["likely_cause"]
            )

            st.write(
                "Check: "
                + cause["recommended_check"]
            )


        st.subheader("Follow-up Questions")


        for q in result["follow_up_questions"]:

            st.write(
                "- " + q
            )


        st.subheader("Scientist Summary")

        st.write(
            result["scientist_summary"]
        )


    else:

        st.error(
            f"Error {response.status_code}"
        )

        st.write(
            response.text
        )
