from typing import List, Dict

def classify_problem(symptom: str) -> Dict:

    symptom = symptom.lower()

    # -------------------------
    # Sensitivity loss
    # -------------------------
    if any(keyword in symptom for keyword in [
        "signal dropped",
        "low signal",
        "signal intensity",
        "loss of sensitivity",
        "low sensitivity",
        "response decreased",
        "signal decreased"
    ]):

        return {
            "problem_category": "sensitivity_loss",
            "likely_causes": [
                {
                    "problem_type": "Ion Suppression",
                    "likely_cause": "Matrix effects reducing ionization efficiency",
                    "recommended_check": "Perform post-column infusion or post-extraction spike experiment",
                    "severity": "High"
                },
                {
                    "problem_type": "Source Contamination",
                    "likely_cause": "Dirty ion source reducing ion transmission",
                    "recommended_check": "Clean source and verify spray stability",
                    "severity": "High"
                },
                {
                    "problem_type": "Mobile Phase",
                    "likely_cause": "Contaminated or incorrectly prepared mobile phase",
                    "recommended_check": "Prepare fresh mobile phases",
                    "severity": "Medium"
                },
                {
                    "problem_type": "Spray Instability",
                    "likely_cause": "Incorrect spray voltage or unstable electrospray",
                    "recommended_check": "Check spray stability and tune report",
                    "severity": "Medium"
                },
                {
                    "problem_type": "Column Installation",
                    "likely_cause": "Incorrect installation or damaged column",
                    "recommended_check": "Verify flow direction and column performance",
                    "severity": "Medium"
                }
            ],

            "follow_up_questions": [
                "Did internal standard response also decrease?",
                "Did all analytes decrease or only specific compounds?",
                "Was the source cleaned recently?",
                "Were new mobile phases prepared?",
                "Did the issue begin immediately after the new column was installed?"
            ]
        }

    # -------------------------
    # Carryover
    # -------------------------

    if any(keyword in symptom for keyword in [
        "carryover",
        "peak in blank",
        "blank injection",
        "blank has peak",
        "blank has signal",
        "signal in blank",
        "response in blank",
        "analyte in blank",
        "blank after high standard",
        "after highest standard",
        "after high standards",
        "wash blank",
        "carry over",
        "ghost peak"
    ]):

        return {
            "problem_category": "carryover",
            "likely_causes": [
                {
                    "problem_type": "Carryover",
                    "likely_cause": "Needle contamination",
                    "recommended_check": "Optimize needle wash",
                    "severity": "High"
                }
            ],

            "follow_up_questions": [
                "Does the blank contain analyte peaks after high standards?"
            ]
        }

    # -------------------------
    # Pressure
    # -------------------------

    if any(keyword in symptom for keyword in [
        "high pressure",
        "pressure increased",
        "backpressure"
    ]):

        return {
            "problem_category": "pressure_issue",
            "likely_causes": [
                {
                    "problem_type": "Column Blockage",
                    "likely_cause": "Blocked frit or column contamination",
                    "recommended_check": "Disconnect column and check pressure",
                    "severity": "High"
                }
            ],

            "follow_up_questions": [
                "Did pressure increase suddenly?"
            ]
        }

    # -------------------------
    # Default
    # -------------------------

    return {

        "problem_category": "general_lcms_issue",

        "likely_causes": [],

        "follow_up_questions": [
            "When did the issue first appear?",
            "What changed recently?"
        ]
    }
    
def generate_follow_up_questions(problem_type: str) -> list[str]:
    question_bank = {
        "low_sensitivity": [
            "Did both analyte and internal standard response decrease?",
            "Was there a recent source cleaning, column change, or mobile phase change?",
            "Are tune/calibration results within expected range?"
        ],
        "carryover": [
            "Does the blank after the highest standard show the same analyte peak?",
            "Does carryover reduce after stronger needle wash?",
            "Is the carryover present in solvent blanks and matrix blanks?"
        ],
        "retention_shift": [
            "Did the mobile phase composition, pH, or column lot change?",
            "Is the shift seen for all analytes or only one compound?",
            "Has the column been flushed or replaced?"
        ],
        "internal_standard_failure": [
            "Did the internal standard drop in all samples or only matrix samples?",
            "Was the IS working solution freshly prepared?",
            "Were autosampler temperature and storage conditions appropriate?"
        ],
        "high_backpressure": [
            "Did pressure increase suddenly or gradually?",
            "Have the guard column and inline filter been replaced?",
            "Is pressure high without the analytical column attached?"
        ],
    }

    return question_bank.get(problem_type, [
        "When did the issue first appear?",
        "Was there any recent change in column, mobile phase, source, method, or sample prep?",
        "Is the issue present in standards, QCs, blanks, and study samples?"
    ])
