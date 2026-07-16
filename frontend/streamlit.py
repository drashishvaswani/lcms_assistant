import streamlit as st
import requests

st.set_page_config(page_title="LCMS AI Assistant")

st.title("🔬 LCMS Troubleshooting Assistant")

uploaded_file = st.file_uploader(
    "Upload SOP or Instrument Manual",
    type=["pdf","txt","docx"]
)

problem = st.text_area(
    "Describe the issue"
)

if st.button("Analyze"):

    files = {
        "file": uploaded_file.getvalue()
    }

    response = requests.post(
        "http://localhost:8000/troubleshoot",
        files={
            "file":(
                uploaded_file.name,
                uploaded_file,
                uploaded_file.type
            )
        },
        data={
            "problem":problem
        }
    )

    st.write(response.json())