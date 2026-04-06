import html

import requests

from config import API_URL, QUESTION_AMOUNT, QUESTION_TYPE


def fetch_questions(category: int = 0) -> list[dict]:
    parameters: dict[str, str | int] = {
        "amount": QUESTION_AMOUNT,
        "type": QUESTION_TYPE,
    }
    if category:
        parameters["category"] = category
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
