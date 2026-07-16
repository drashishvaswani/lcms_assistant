from fastapi import FastAPI, UploadFile, File, HTTPException
from app.rule_engine import classify_problem
from app.llm_assistant import generate_scientist_summary
from app.database import engine, SessionLocal
from app.models import Base, Document
from app.schemas import TroubleshootingRequest

from datetime import datetime
from dotenv import load_dotenv

import pdfplumber
import io
import os


HF_TOKEN = os.getenv("HF_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")


app = FastAPI(
    title="LC-MS Troubleshooting Assistant"
)


Base.metadata.create_all(bind=engine)


# -------------------------------------------------------
# Extract PDF text
# -------------------------------------------------------

def extract_pdf_text(file_bytes):

    text = ""

    try:

        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=f"PDF extraction failed: {str(e)}"
        )

    return text



# -------------------------------------------------------
# Health check
# -------------------------------------------------------

@app.get("/")
def health():

    return {
        "status": "running",
        "application": "LC-MS Troubleshooting Assistant"
    }



# -------------------------------------------------------
# Upload document
# -------------------------------------------------------

@app.post("/upload")
async def upload_document(
        file: UploadFile = File(...)
):

    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )


    file_bytes = await file.read()


    document_text = extract_pdf_text(
        file_bytes
    )


    db = SessionLocal()


    try:

        doc = Document(
            filename=file.filename,
            upload_date=datetime.now(),
            text=document_text
        )


        db.add(doc)

        db.commit()


    finally:

        db.close()



    return {

        "message": "Document uploaded successfully",

        "filename": file.filename,

        "characters_extracted": len(document_text)

    }




# -------------------------------------------------------
# Troubleshooting
# -------------------------------------------------------

@app.post("/troubleshoot")
async def troubleshoot(
    request: TroubleshootingRequest
):

    db = SessionLocal()

    try:

        documents = db.query(Document).all()

        kb_text = ""

        for doc in documents:
            kb_text += "\n\n" + doc.text[:1000]

    finally:

        db.close()


    rule_result = classify_problem(
        request.symptom
    )


    problem_type = rule_result["problem_category"]

    likely_causes = rule_result["likely_causes"]

    follow_up_questions = rule_result["follow_up_questions"]


    print("STARTING LLM")

    summary = generate_scientist_summary(
        symptom=request.symptom,
        problem_type=problem_type,
        likely_causes=likely_causes,
        document=kb_text
    )

    print("LLM COMPLETED")


    return {
        "problem_category": problem_type,
        "likely_causes": likely_causes,
        "follow_up_questions": follow_up_questions,
        "scientist_summary": summary
    }
