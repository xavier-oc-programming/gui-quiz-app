# Course Notes

## Exercise Description

Build a True/False trivia quiz application that:

1. Fetches questions live from the [Open Trivia Database API](https://opentdb.com/) using `requests`.
2. Parses the JSON response and decodes any HTML entities found in the question text.
3. Models the data with a `Question` class (text + correct answer) and a `QuizBrain` class that manages state.
4. Presents questions one at a time inside a Tkinter GUI window.
5. Lets the user answer by clicking a True or False image button.
6. Gives instant colour feedback (green = correct, red = wrong) before loading the next question.
7. Tracks and displays the running score until all questions have been answered.

## Concepts Covered

### API & Data

- Sending a parameterised GET request with `requests.get(url, params={})`
- Reading and navigating a JSON response with `.json()`
- Handling HTTP errors with `.raise_for_status()`
- Decoding HTML character entities with Python's built-in `html.unescape()`

### Object-Oriented Programming

- **`Question`** — a simple data class storing `text` and `answer`
- **`QuizBrain`** — manages `question_number`, `score`, the question list, and the current question; exposes `still_has_questions()`, `next_question()`, and `check_answer()`
- **`QuizInterface`** — owns the Tk window and all widgets; calls into `QuizBrain` directly

### Tkinter GUI

- Creating and configuring a `Tk()` root window (`title`, `config`, `padx`, `pady`, `bg`)
- `Label` — score display, styled with `fg`, `bg`, `font`
- `Canvas` — question text drawn with `create_text`; background colour changed at runtime with `.config(bg=...)`
- `PhotoImage` — loading `.png` images for buttons
- `Button` — image-only buttons bound to commands; `config(state="disabled")` to lock them
- Grid layout: `grid(row=, column=, columnspan=, sticky=, pady=)`
- Delayed callback with `window.after(ms, callback)` to pause before advancing

### Python Patterns

- Module-level execution in `data.py` (runs at import time)
- Keeping `PhotoImage` references as instance attributes to prevent garbage collection
- Using `int | None` union type hint (Python 3.10+)
