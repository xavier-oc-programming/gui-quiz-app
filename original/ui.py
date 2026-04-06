# ui.py
from tkinter import *
from pathlib import Path
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"
_IMAGES = Path(__file__).parent.parent / "images"


class QuizInterface:
    def __init__(self, quiz_brain: QuizBrain):
        self.quiz = quiz_brain

        # --- Window ---
        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        # --- Status label (top-right) ---
        self.score_label = Label(text="", fg="white", bg=THEME_COLOR, font=("Arial", 12, "bold"))
        self.score_label.grid(row=0, column=1, sticky="e")

        # --- Question canvas ---
        self.canvas = Canvas(width=300, height=250, bg="white", highlightthickness=0)
        self.question_text = self.canvas.create_text(
            150, 125, width=280, text="", fill=THEME_COLOR, font=("Arial", 20, "italic")
        )
        self.canvas.grid(row=1, column=0, columnspan=2, pady=50)

        # --- Buttons (keep refs to images) ---
        self.true_img = PhotoImage(file=str(_IMAGES / "true.png"))
        self.true_button = Button(image=self.true_img, highlightthickness=0, bd=0, command=self.true_pressed)
        self.true_button.grid(row=2, column=0)

        self.false_img = PhotoImage(file=str(_IMAGES / "false.png"))
        self.false_button = Button(image=self.false_img, highlightthickness=0, bd=0, command=self.false_pressed)
        self.false_button.grid(row=2, column=1)

        # Initial status (0 answered)
        self.update_status(answered=0)

        # Load first question
        self.get_next_question()

        self.window.mainloop()

    # ---------- Helpers ----------
    def update_status(self, answered: int | None = None):
        """
        Show: 'Score: X/Y — N Questions Left !'
        answered = questions already answered.
        """
        total = len(self.quiz.question_list)
        if answered is None:
            answered = max(self.quiz.question_number - 1, 0)

        remaining = total - answered
        word = "Question" if remaining == 1 else "Questions"
        self.score_label.config(
            text=f"Score: {self.quiz.score}/{answered} — {remaining} {word} Left !"
        )

    # ---------- UI flow ----------
    def get_next_question(self):
        self.canvas.config(bg="white")
        if self.quiz.still_has_questions():
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text)
        else:
            total = len(self.quiz.question_list)
            self.update_status(answered=total)
            self.canvas.itemconfig(self.question_text, text="You've reached the end of the quiz.")
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")

    def true_pressed(self):
        self.give_feedback(self.quiz.check_answer("True"))

    def false_pressed(self):
        self.give_feedback(self.quiz.check_answer("False"))

    def give_feedback(self, is_right: bool):
        self.canvas.config(bg="green" if is_right else "red")
        # Update once per answer (prevents +2/-1 glitch)
        self.update_status(answered=self.quiz.question_number)
        self.window.after(1000, self.get_next_question)
