from pydantic import BaseModel
from typing import Optional, List


class TroubleshootingRequest(BaseModel):
    symptom: str
    instrument: str
    analyte_type: str
    ionization_mode: str
    column_type: str
    mobile_phase: str
    recent_changes: str


class TroubleshootingFinding(BaseModel):
    problem_type: str
    likely_cause: str
    recommended_check: str
    severity: str


class TroubleshootingResponse(BaseModel):
    problem_category: str
    likely_causes: List[TroubleshootingFinding]
    follow_up_questions: List[str]
    scientist_summary: str