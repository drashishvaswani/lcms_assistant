import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

client = InferenceClient(
    provider="auto",
    api_key=os.getenv("HF_TOKEN")
)


def generate_scientist_summary(
    symptom,
    problem_type,
    likely_causes,
    document=""
):

    causes = ""

    for item in likely_causes:

        causes += f"""
Problem Type: {item['problem_type']}
Likely Cause: {item['likely_cause']}
Recommended Check: {item['recommended_check']}
Severity: {item['severity']}
"""

    prompt = f"""
You are an experienced LC-MS bioanalytical scientist.

Scientist observed:

Symptom:
{symptom}

Problem Category:
{problem_type}

Likely causes:
{causes}

Relevant document context:
{document[:3000]}

Write a troubleshooting report.

Include:

1. Summary
2. Scientific rationale
3. Recommended checks
4. Next experiments

Do NOT invent causes that are not listed above.
"""

    completion = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=500
    )

    return completion.choices[0].message.content