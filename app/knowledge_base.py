import pandas as pd


def load_knowledge_base(path="data/lcms_troubleshooting_kb.csv"):
    return pd.read_csv(path)


def search_knowledge_base(symptom, kb):

    symptom = symptom.lower()

    matches = []

    for _, row in kb.iterrows():

        score = 0

        kb_symptom = str(row["symptom"]).lower()

        kb_problem = str(row["problem_type"]).lower()

        # score symptom overlap
        for word in symptom.split():

            if word in kb_symptom:
                score += 2

            if word in kb_problem:
                score += 3

        if score > 0:
            matches.append((score, row))

    matches.sort(key=lambda x: x[0], reverse=True)

    if len(matches) == 0:
        return pd.DataFrame()

    rows = [m[1] for m in matches]

    return pd.DataFrame(rows)