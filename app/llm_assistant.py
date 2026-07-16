import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

client = InferenceClient(
    provider="auto",
    api_key=HF_TOKEN,
    timeout=30
)


SYSTEM_PROMPT = """
You are an LC-MS troubleshooting assistant.

You help bioanalytical scientists troubleshoot LC-MS assays.

Rules:
- Do not change the diagnosis from the rule engine.
- Explain possible causes.
- Suggest practical experiments.
- Be concise and scientific.
"""


def generate_scientist_summary(
        symptom,
        problem_type,
        likely_causes,
        document=""
):

    try:

        causes_text = ""

        for item in likely_causes:

            causes_text += f"""
Problem:
{item.get('problem_type')}

Cause:
{item.get('likely_cause')}

Recommended Check:
{item.get('recommended_check')}

Severity:
{item.get('severity')}

"""


        # Limit document context
        document_context = document[:3000]


        prompt = f"""

{SYSTEM_PROMPT}


Scientist reported:

Symptom:
{symptom}


Rule engine diagnosis:

Problem category:
{problem_type}


Likely causes:

{causes_text}


Reference document information:

{document_context}


Generate a troubleshooting report containing:

1. Summary
2. Likely root causes
3. Recommended experiments
4. Next troubleshooting steps

"""


        response = client.chat.completions.create(

            model="mistralai/Mistral-7B-Instruct-v0.3",

            messages=[

                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },

                {
                    "role": "user",
                    "content": prompt
                }

            ],

            max_tokens=400

        )


        return response.choices[0].message.content



    except Exception as e:

        print(
            "LLM ERROR:",
            str(e)
        )


        # Fallback response
        summary = f"""
LC-MS Troubleshooting Summary

Problem Category:
{problem_type}


Likely causes:

"""


        for item in likely_causes:

            summary += f"""

- {item.get('problem_type')}

  Cause:
  {item.get('likely_cause')}

  Recommended check:
  {item.get('recommended_check')}

"""


        summary += """

Next Steps:

1. Verify instrument performance.
2. Review recent method changes.
3. Analyze standards, QCs, and blanks.
"""


        return summary
