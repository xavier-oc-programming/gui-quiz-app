import sys
import tkinter as tk
from pathlib import Path
from typing import Callable

from config import (
    CANVAS_BG,
    CANVAS_HEIGHT,
    CANVAS_TEXT_WIDTH,
    CANVAS_TEXT_X,
    CANVAS_TEXT_Y,
    CANVAS_WIDTH,
    CATEGORIES,
    FEEDBACK_CORRECT_COLOR,
    FEEDBACK_DELAY_MS,
    FEEDBACK_WRONG_COLOR,
    FONT_QUESTION,
    FONT_SCORE,
    LABEL_FG,
    SELECTOR_BTN_FONT,
    SELECTOR_BTN_TEXT,
    SELECTOR_LISTBOX_FONT,
    SELECTOR_LISTBOX_HEIGHT,
    SELECTOR_LISTBOX_WIDTH,
    SELECTOR_TITLE,
    SELECTOR_TITLE_FONT,
    THEME_COLOR,
    WINDOW_PADDING_X,
    WINDOW_PADDING_Y,
    WINDOW_TITLE,
)

_IMAGES = Path(__file__).parent.parent / "images"


class Display:
    def __init__(self, on_category_select: Callable[[int], None]) -> None:
        self._on_category_select = on_category_select
        self._on_true: Callable[[], None] = lambda: None
        self._on_false: Callable[[], None] = lambda: None

        self.root = tk.Tk()
        self.root.title(WINDOW_TITLE)
        self.root.config(padx=WINDOW_PADDING_X, pady=WINDOW_PADDING_Y, bg=THEME_COLOR)

        self._build_selector()
        self._build_quiz_widgets()
        self.root.focus_set()

    # ---------- Category selector ----------

    def _build_selector(self) -> None:
        self._selector_frame = tk.Frame(self.root, bg=THEME_COLOR)
        self._selector_frame.grid(row=0, column=0, columnspan=2)

        tk.Label(
            self._selector_frame,
            text=SELECTOR_TITLE,
            fg=LABEL_FG,
            bg=THEME_COLOR,
            font=SELECTOR_TITLE_FONT,
        ).pack(pady=(0, 10))

        list_frame = tk.Frame(self._selector_frame, bg=THEME_COLOR)
        list_frame.pack()

        scrollbar = tk.Scrollbar(list_frame, orient="vertical")
        self._listbox = tk.Listbox(
            list_frame,
            height=SELECTOR_LISTBOX_HEIGHT,
            width=SELECTOR_LISTBOX_WIDTH,
            font=SELECTOR_LISTBOX_FONT,
            yscrollcommand=scrollbar.set,
            selectmode="single",
            activestyle="none",
            bg="white",
            fg=THEME_COLOR,
            selectbackground=THEME_COLOR,
            selectforeground="white",
            borderwidth=0,
            highlightthickness=1,
            highlightcolor=THEME_COLOR,
        )
        scrollbar.config(command=self._listbox.yview)
        self._listbox.pack(side="left")
        scrollbar.pack(side="left", fill="y")

        for name in CATEGORIES:
            self._listbox.insert("end", name)
        self._listbox.select_set(0)

        tk.Button(
            self._selector_frame,
            text=SELECTOR_BTN_TEXT,
            font=SELECTOR_BTN_FONT,
            bg="white",
            fg=THEME_COLOR,
            relief="flat",
            padx=10,
            pady=5,
            command=self._handle_category_select,
        ).pack(pady=(10, 0))

        self._listbox.bind("<Double-Button-1>", lambda _: self._handle_category_select())
        self.root.bind("<Return>", lambda _: self._handle_category_select())

    def _handle_category_select(self) -> None:
        selection = self._listbox.curselection()
        if not selection:
            return
        name = self._listbox.get(selection[0])
        category_id = CATEGORIES[name]
        self._selector_frame.grid_remove()
        self._show_loading(category_id)

    def _show_loading(self, category_id: int) -> None:
        self._score_label.grid(row=0, column=1, sticky="e")
        self._canvas.grid(row=1, column=0, columnspan=2, pady=50)
        self._true_button.grid(row=2, column=0)
        self._false_button.grid(row=2, column=1)
        self._set_buttons("disabled")
        self._canvas.itemconfig(self._question_text, text="Loading questions…")
        self.root.after(50, lambda: self._on_category_select(category_id))

    # ---------- Quiz widgets ----------

    def _build_quiz_widgets(self) -> None:
        self._score_label = tk.Label(
            self.root, text="", fg=LABEL_FG, bg=THEME_COLOR, font=FONT_SCORE
        )

        self._canvas = tk.Canvas(
            self.root,
            width=CANVAS_WIDTH,
            height=CANVAS_HEIGHT,
            bg=CANVAS_BG,
            highlightthickness=0,
        )
        self._question_text = self._canvas.create_text(
            CANVAS_TEXT_X,
            CANVAS_TEXT_Y,
            width=CANVAS_TEXT_WIDTH,
            text="",
            fill=THEME_COLOR,
            font=FONT_QUESTION,
        )

        self._true_img = tk.PhotoImage(file=str(_IMAGES / "true.png"))
        self._true_button = tk.Button(
            self.root,
            image=self._true_img,
            highlightthickness=0,
            bd=0,
            command=self._handle_true,
        )

        self._false_img = tk.PhotoImage(file=str(_IMAGES / "false.png"))
        self._false_button = tk.Button(
            self.root,
            image=self._false_img,
            highlightthickness=0,
            bd=0,
            command=self._handle_false,
        )

    def start_quiz(
        self,
        on_true: Callable[[], None],
        on_false: Callable[[], None],
    ) -> None:
        self._on_true = on_true
        self._on_false = on_false
        self.root.unbind("<Return>")
        self.root.bind("<Key-t>", lambda _: self._handle_true())
        self.root.bind("<Key-f>", lambda _: self._handle_false())
        self.root.focus_set()

    # ---------- Internal handlers ----------

    def _handle_true(self) -> None:
        self._set_buttons("disabled")
        self._on_true()

    def _handle_false(self) -> None:
        self._set_buttons("disabled")
        self._on_false()

    def _set_buttons(self, state: str) -> None:
        self._true_button.config(state=state)
        self._false_button.config(state=state)

    def _update_score_label(self, score: int, answered: int, total: int) -> None:
        remaining = total - answered
        word = "Question" if remaining == 1 else "Questions"
        self._score_label.config(
            text=f"Score: {score}/{answered} — {remaining} {word} Left !"
        )

    # ---------- Public render methods ----------

    def render_question(self, text: str, score: int, answered: int, total: int) -> None:
        self._canvas.config(bg=CANVAS_BG)
        self._canvas.itemconfig(self._question_text, text=text)
        self._update_score_label(score, answered, total)
        self._set_buttons("normal")

    def render_feedback(
        self,
        is_correct: bool,
        score: int,
        answered: int,
        total: int,
        on_done: Callable[[], None],
    ) -> None:
        color = FEEDBACK_CORRECT_COLOR if is_correct else FEEDBACK_WRONG_COLOR
        self._canvas.config(bg=color)
        self._update_score_label(score, answered, total)
        self.root.after(FEEDBACK_DELAY_MS, on_done)

    def render_quiz_over(self, score: int, total: int) -> None:
        self._canvas.config(bg=CANVAS_BG)
        self._canvas.itemconfig(
            self._question_text, text="You've reached the end of the quiz."
        )
        self._update_score_label(score, total, total)
        self._set_buttons("disabled")

    def close(self) -> None:
        sys.exit(0)
