import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from data import fetch_questions
from display import Display
from question_model import Question
from quiz_brain import QuizBrain


def main() -> None:
    question_data = fetch_questions()
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
