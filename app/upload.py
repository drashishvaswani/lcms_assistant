from database import SessionLocal
from models import Document

db = SessionLocal()

document = Document(
    filename=file.filename,
    text=extracted_text
)

db.add(document)
db.commit()

db.refresh(document)

db.close()