import html

import requests

from config import API_URL, QUESTION_AMOUNT, QUESTION_TYPE, QUESTION_CATEGORY


def fetch_questions() -> list[dict]:
    parameters = {
        "amount": QUESTION_AMOUNT,
        "type": QUESTION_TYPE,
        "category": QUESTION_CATEGORY,
    }
    response = requests.get(API_URL, params=parameters)
    response.raise_for_status()
    data = response.json()
    return [
        {
            "question": html.unescape(q["question"]),
            "correct_answer": html.unescape(q["correct_answer"]),
        }
        for q in data["results"]
    ]
