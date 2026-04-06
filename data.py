# data.py
import requests
import html   # For decoding HTML entities

# Parameters for the API request
parameters = {
    "amount": 10,        # Number of questions
    "type": "boolean",   # Question type: "boolean" = True/False
    "category": 18,    # (Optional) Example: 18 = Computers
    # "difficulty": "easy"  # (Optional) easy / medium / hard
}

# Send the GET request with parameters
response = requests.get("https://opentdb.com/api.php", params=parameters)
response.raise_for_status()
data = response.json()

# Extract and clean the question list
question_data = [
    {
        "question": html.unescape(q["question"]),
        "correct_answer": html.unescape(q["correct_answer"])
    }
    for q in data["results"]
]
