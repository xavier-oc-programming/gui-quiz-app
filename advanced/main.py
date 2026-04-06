import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config import CATEGORIES
from data import fetch_questions
from display import Display
from question_model import Question
from quiz_brain import QuizBrain


def select_category() -> int:
    items = list(CATEGORIES.items())
    print("\nSelect a category:")
    for i, (name, _) in enumerate(items, 1):
        print(f"  {i:2}. {name}")
    while True:
        choice = input("\nYour choice (number): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(items):
            return items[int(choice) - 1][1]
        print("Invalid choice. Try again.")


def main() -> None:
    category = select_category()
    question_data = fetch_questions(category)
    question_bank = [Question(q["question"], q["correct_answer"]) for q in question_data]
    quiz = QuizBrain(question_bank)
    total = len(question_bank)

    def advance() -> None:
        if quiz.still_has_questions():
            text = quiz.next_question()
            display.render_question(text, quiz.score, quiz.question_number - 1, total)
        else:
            display.render_quiz_over(quiz.score, total)

    def on_answer(answer: str) -> None:
        is_correct = quiz.check_answer(answer)
        display.render_feedback(
            is_correct, quiz.score, quiz.question_number, total, advance
        )

    display = Display(
        on_true=lambda: on_answer("True"),
        on_false=lambda: on_answer("False"),
    )

    advance()
    display.root.mainloop()


if __name__ == "__main__":
    main()
