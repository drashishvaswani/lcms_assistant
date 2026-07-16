import streamlit as st
import requests


API_URL = "https://lcms-assistant.onrender.com"


st.set_page_config(
    page_title="LC-MS AI Assistant",
    page_icon="🔬",
    layout="wide"
)


st.title("🔬 LC-MS Troubleshooting Assistant")

st.write(
    "AI-assisted troubleshooting for LC-MS bioanalytical workflows"
)


# =====================================================
# Document Upload
# =====================================================

st.header("1. Upload Reference Document")

uploaded_file = st.file_uploader(
    "Upload LC-MS paper / SOP / instrument manual",
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


        with st.spinner("Uploading document..."):

            response = requests.post(
                f"{API_URL}/upload",
                files=files,
                timeout=120
            )


        if response.status_code == 200:

            st.success(
                "Document uploaded successfully"
            )

            st.json(response.json())

        else:

            st.error(
                f"Upload failed: {response.status_code}"
            )

            st.write(response.text)



# =====================================================
# LC-MS Context Inputs
# =====================================================

st.header("2. LC-MS Method Information")


instrument = st.text_input(
    "Instrument",
    value="Sciex X500 QTOF"
)


analyte_type = st.text_input(
    "Analyte Type",
    value="Small molecule drug"
)


ionization_mode = st.text_input(
    "Ionization Mode",
    value="ESI positive"
)


column_type = st.text_input(
    "Column Type",
    value="C18 reverse phase"
)


mobile_phase = st.text_input(
    "Mobile Phase",
    value="Water/acetonitrile with 0.1% formic acid"
)


recent_changes = st.text_input(
    "Recent Changes",
    value="New C18 column installed"
)



# =====================================================
# Problem Description
# =====================================================

st.header("3. Describe LC-MS Problem")


symptom = st.text_area(
    "Problem Description",
    value="LC-MS signal intensity dropped by 80% after installing a new C18 column. Internal standard response also decreased.",
    height=150
)



# =====================================================
# Troubleshooting
# =====================================================

if st.button("🔍 Analyze Troubleshooting"):


    if symptom.strip() == "":

        st.warning(
            "Please describe the LC-MS issue"
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



    with st.spinner(
        "Running LC-MS troubleshooting analysis..."
    ):


        response = requests.post(

            f"{API_URL}/troubleshoot",

            json=payload,

            timeout=180

        )



    if response.status_code == 200:


        result = response.json()


        st.success(
            "Analysis Complete"
        )


        st.header("Problem Category")

        st.write(
            result["problem_category"]
        )



        st.header("Likely Causes")


        for cause in result["likely_causes"]:

            with st.expander(
                cause["problem_type"]
            ):

                st.write(
                    "**Likely Cause:**"
                )

                st.write(
                    cause["likely_cause"]
                )


                st.write(
                    "**Recommended Check:**"
                )

                st.write(
                    cause["recommended_check"]
                )


                st.write(
                    "**Severity:**"
                )

                st.write(
                    cause["severity"]
                )



        st.header("Follow-up Questions")


        for question in result["follow_up_questions"]:

            st.write(
                "- " + question
            )



        st.header("Scientist Summary")


        st.write(
            result["scientist_summary"]
        )



    else:


        st.error(
            f"Troubleshooting failed: {response.status_code}"
        )


        st.write(
            response.text
        )
