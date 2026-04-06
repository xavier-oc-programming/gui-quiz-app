# Quizzler

A True/False trivia quiz that fetches questions live from the Open Trivia Database API and displays them in a Tkinter GUI.

---

## Table of Contents

1. [Quick start](#1-quick-start)
2. [Builds comparison](#2-builds-comparison)
3. [Controls](#3-controls)
4. [App flow](#4-app-flow)
5. [Features](#5-features)
6. [Navigation flow](#6-navigation-flow)
7. [Architecture](#7-architecture)
8. [Module reference](#8-module-reference)
9. [Configuration reference](#9-configuration-reference)
10. [Display layout](#10-display-layout)
11. [Design decisions](#11-design-decisions)
12. [Course context](#12-course-context)
13. [Dependencies](#13-dependencies)

---

## 1. Quick start

```bash
pip install requests          # only external dependency

python menu.py                # launch the terminal menu, then select 1 or 2

python original/main.py       # run the original build directly
python advanced/main.py       # run the advanced build directly
```

---

## 2. Builds comparison

| Feature | Original | Advanced |
|---------|:--------:|:--------:|
| Live API question fetching | ✓ | ✓ |
| True/False button controls | ✓ | ✓ |
| Score and questions-remaining display | ✓ | ✓ |
| Colour feedback (green / red) | ✓ | ✓ |
| Keyboard shortcuts (T / F) | — | ✓ |
| Button lock during feedback window | — | ✓ |
| Centralised configuration (`config.py`) | — | ✓ |
| UI / logic fully separated | — | ✓ |
| `fetch_questions()` function (lazy API call) | — | ✓ |

---

## 3. Controls

**Gameplay**

| Input | Action |
|-------|--------|
| Click ✓ (True button) | Answer True |
| Click ✗ (False button) | Answer False |
| `T` *(advanced build only)* | Answer True via keyboard |
| `F` *(advanced build only)* | Answer False via keyboard |

---

## 4. App flow

1. `data.py` / `fetch_questions()` sends a GET request to the Open Trivia Database and decodes HTML entities in the returned text.
2. 10 True/False questions are loaded into a question bank.
3. The first question appears in the canvas.
4. You click True or False (or press `T`/`F` in the advanced build).
5. The canvas flashes **green** (correct) or **red** (wrong); the score label updates immediately.
6. After 1 second the canvas resets to white and the next question loads.
7. Once all 10 questions are answered, "You've reached the end of the quiz." is shown and both buttons are disabled.

---

## 5. Features

### Both builds

**Live API questions**
Questions are fetched fresh from the Open Trivia Database on every launch, so each session uses a different set.

**Colour feedback**
The canvas background turns green for a correct answer and red for a wrong one, giving instant visual reinforcement before the next question loads.

**Live score display**
The label shows `Score: X/Y — N Questions Left !` — X is the number of correct answers, Y is the number of questions answered so far, and N counts down with each question.

### Advanced build only

**Keyboard shortcuts**
Press `T` for True and `F` for False. No mouse required once the window has focus.

**Button lock during feedback**
Both answer buttons are disabled the instant you submit an answer and re-enabled only when the next question loads. This prevents accidental double-submissions during the 1-second feedback window.

**Centralised configuration**
All magic numbers — canvas dimensions, colours, fonts, timing, and API parameters — live in a single `config.py`. Changing the feedback delay or question count requires editing exactly one line.

**Clean UI / logic separation**
`Display` owns every widget and has no knowledge of quiz rules. `QuizBrain` contains all game logic and has no tkinter imports. `main.py` wires the two together exclusively via callbacks.

**Lazy API call**
The original `data.py` runs the HTTP request at import time. The advanced `data.py` wraps it in `fetch_questions()`, so the call only fires when `main()` explicitly invokes it.

---

## 6. Navigation flow

### Terminal menu tree

```
python menu.py
│
├── 1  ──────────────►  original/main.py  (original build)
├── 2  ──────────────►  advanced/main.py  (advanced build)
└── q  ──────────────►  exit
```

### In-app flow

```
[App Start]
     │
     ▼
[API Fetch → 10 questions loaded]
     │
     ▼
┌─────────────────────────┐
│   Question displayed    │◄──────────────────────┐
└─────────────────────────┘                       │
     │                                             │
  Click ✓/✗  (or press T/F)                        │
     │                                             │
     ▼                                             │
[Feedback: canvas green or red, score updates]     │
     │                                             │
  after 1 second                                   │
     │                                             │
     ├── questions remain ──────────────────────────┘
     │
     └── no questions left
               │
               ▼
     [Quiz Over: buttons disabled]
```

---

## 7. Architecture

```
gui-quiz-app/
│
├── menu.py                     # Terminal launcher: print logo, run selected build
├── art.py                      # LOGO constant — ASCII art printed by menu.py
├── requirements.txt            # pip-installable dependencies (requests)
├── .gitignore
├── README.md
│
├── images/
│   ├── true.png                # ✓ button image (shared by both builds)
│   └── false.png               # ✗ button image (shared by both builds)
│
├── docs/
│   └── COURSE_NOTES.md         # Original exercise description and concepts covered
│
├── original/                   # Verbatim course files (path fix in ui.py only)
│   ├── main.py                 # Wires QuizBrain → QuizInterface
│   ├── data.py                 # Module-level API fetch; exports question_data
│   ├── question_model.py       # Question(text, answer) data class
│   ├── quiz_brain.py           # QuizBrain: state + logic
│   └── ui.py                   # QuizInterface: Tk window, widgets, event loop
│
└── advanced/                   # Refactored build — MVC separation
    ├── main.py                 # Orchestrator: wires QuizBrain ↔ Display via callbacks
    ├── config.py               # All constants — zero magic numbers elsewhere
    ├── question_model.py       # Question dataclass — pure logic, no tkinter
    ├── quiz_brain.py           # QuizBrain — pure logic, no tkinter
    ├── data.py                 # fetch_questions() — lazy API call, no tkinter
    └── display.py              # Display class — all tkinter, no quiz logic
```

---

## 8. Module reference

### `original/question_model.py` — class `Question`

| Method | Returns | Description |
|--------|---------|-------------|
| `__init__(text, answer)` | — | Stores question text and correct answer as instance attributes |

### `original/quiz_brain.py` — class `QuizBrain`

| Method | Returns | Description |
|--------|---------|-------------|
| `__init__(q_list)` | — | Initialises `question_number=0`, `score=0`, stores the question list |
| `still_has_questions()` | `bool` | `True` while `question_number < len(question_list)` |
| `next_question()` | `str` | Advances to the next question, increments counter, returns question text |
| `check_answer(user_answer)` | `bool` | Case-insensitive comparison; increments `score` if correct |

### `original/ui.py` — class `QuizInterface`

| Method | Returns | Description |
|--------|---------|-------------|
| `__init__(quiz_brain)` | — | Builds the Tk window, loads the first question, enters `mainloop()` |
| `update_status(answered)` | `None` | Refreshes the score label with current score, answered count, and remaining count |
| `get_next_question()` | `None` | Resets canvas to white; shows next question or end message |
| `true_pressed()` | `None` | Submits "True" to `check_answer`, triggers feedback |
| `false_pressed()` | `None` | Submits "False" to `check_answer`, triggers feedback |
| `give_feedback(is_right)` | `None` | Flashes canvas, updates score label, schedules next question after 1 s |

### `advanced/data.py`

| Function | Returns | Description |
|----------|---------|-------------|
| `fetch_questions()` | `list[dict]` | Calls the Open Trivia DB API and returns a list of `{question, correct_answer}` dicts with HTML entities decoded |

### `advanced/quiz_brain.py` — class `QuizBrain`

| Method | Returns | Description |
|--------|---------|-------------|
| `__init__(q_list)` | — | Initialises `question_number=0`, `score=0`, stores the question list |
| `still_has_questions()` | `bool` | `True` while `question_number < len(question_list)` |
| `next_question()` | `str` | Advances to the next question, increments counter, returns question text |
| `check_answer(user_answer)` | `bool` | Case-insensitive comparison; increments `score` if correct |

### `advanced/display.py` — class `Display`

| Method | Returns | Description |
|--------|---------|-------------|
| `__init__(on_true, on_false)` | — | Builds the Tk window and all widgets; binds `T`/`F` keys; stores callbacks |
| `render_question(text, score, answered, total)` | `None` | Resets canvas to white, shows new question, updates score label, re-enables buttons |
| `render_feedback(is_correct, score, answered, total, on_done)` | `None` | Flashes canvas green/red, updates score label, schedules `on_done` after `FEEDBACK_DELAY_MS` |
| `render_quiz_over(score, total)` | `None` | Shows end message, updates final score label, disables both buttons |
| `close()` | `None` | Calls `sys.exit(0)` |

---

## 9. Configuration reference

All constants live in [advanced/config.py](advanced/config.py).

| Constant | Default | Description |
|----------|---------|-------------|
| `WINDOW_TITLE` | `"Quizzler"` | Tk window title bar text |
| `WINDOW_PADDING_X` | `20` | Horizontal window padding (px) |
| `WINDOW_PADDING_Y` | `20` | Vertical window padding (px) |
| `THEME_COLOR` | `"#375362"` | Background colour for window and score label |
| `CANVAS_BG` | `"white"` | Default canvas background |
| `FEEDBACK_CORRECT_COLOR` | `"green"` | Canvas colour shown after a correct answer |
| `FEEDBACK_WRONG_COLOR` | `"red"` | Canvas colour shown after a wrong answer |
| `LABEL_FG` | `"white"` | Score label text colour |
| `CANVAS_WIDTH` | `300` | Canvas width (px) |
| `CANVAS_HEIGHT` | `250` | Canvas height (px) |
| `CANVAS_TEXT_WIDTH` | `280` | Maximum wrap width for question text (px) |
| `CANVAS_TEXT_X` | `150` | Question text anchor x (centre of canvas) |
| `CANVAS_TEXT_Y` | `125` | Question text anchor y (centre of canvas) |
| `FONT_SCORE` | `("Arial", 12, "bold")` | Score label font |
| `FONT_QUESTION` | `("Arial", 20, "italic")` | Question text font |
| `FEEDBACK_DELAY_MS` | `1000` | How long feedback colour is shown before advancing (ms) |
| `API_URL` | `"https://opentdb.com/api.php"` | Open Trivia Database endpoint |
| `QUESTION_AMOUNT` | `10` | Number of questions fetched per session |
| `QUESTION_TYPE` | `"boolean"` | Open Trivia DB question type (`"boolean"` = True/False) |
| `QUESTION_CATEGORY` | `18` | Open Trivia DB category ID (18 = Computers) |

---

## 10. Display layout

```
┌──────────────────────────────────────────┐
│  (bg=#375362, padx=20, pady=20)           │
│                                           │
│  row 0 ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄  │
│  [col 0: empty]   [col 1: Score label ▶] │
│                   "Score: 0/0 — 10        │
│                    Questions Left !"      │
│                                           │
│  row 1 ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄  │
│  (columnspan=2, pady=50)                  │
│  ┌────────────────────────────────┐       │
│  │       Canvas 300 × 250 px      │       │
│  │       (bg=white by default)    │       │
│  │                                │       │
│  │   Question text                │       │
│  │   (Arial 20 italic, centred    │       │
│  │    at x=150, y=125,            │       │
│  │    wrap width=280)             │       │
│  │                                │       │
│  └────────────────────────────────┘       │
│                                           │
│  row 2 ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄  │
│  [col 0: ✓ true.png]  [col 1: ✗ false.png]│
│                                           │
└──────────────────────────────────────────┘
  Approximate rendered size: ~340 × 420 px
```

---

## 11. Design decisions

**`display.py` owns all UI (testability, swappability)**
Isolating every widget inside `Display` means quiz logic can be tested without ever spinning up a Tk window. If the GUI toolkit changes, only `display.py` needs to be rewritten — nothing in `quiz_brain.py` or `data.py` is affected.

**`config.py` — zero magic numbers**
Every number, colour string, and API parameter has a name and lives in one file. Changing the feedback delay, question count, or category requires editing exactly one constant.

**Callbacks injected via `__init__`**
`Display` receives `on_true` and `on_false` at construction time and never imports `QuizBrain`. It knows nothing about what the callbacks do — it just calls them when a button is pressed. This fully decouples the display layer from the quiz logic.

**`fetch_questions()` function vs module-level execution**
The original `data.py` fires the API request at import time, which means it runs even during tooling, testing, or accidental imports. Wrapping it in `fetch_questions()` makes the call explicit, lazy, and easy to mock in tests.

**Button lock during feedback**
Both buttons are disabled the moment an answer is submitted and re-enabled only inside `render_question()`. Without this, clicking rapidly during the 1-second feedback window would call `check_answer()` twice on the same question, corrupting the score.

**`sys.path.insert` pattern**
`advanced/main.py` inserts its own directory at the front of `sys.path` so sibling imports (`from display import Display`) resolve correctly whether the file is run directly (`python advanced/main.py`) or launched via `menu.py` with a different working directory.

**`subprocess.run` + `cwd=`**
`menu.py` sets `cwd=str(path.parent)` when launching each build so the child process's working directory matches the source file's location, keeping any remaining relative-path assumptions intact.

**`while True` in `menu.py` vs recursion**
Calling the menu function recursively would grow the call stack indefinitely over many launches. A plain `while True` loop has zero stack cost regardless of how many builds are launched.

**Console cleared before every menu render**
`os.system("cls"/"clear")` runs at the top of each loop iteration so the menu always appears on a clean terminal, especially after a build exits and control returns.

**`sys.exit(0)` vs `root.destroy()` alone**
Calling `root.destroy()` alone can leave `mainloop()` spinning or raise tkinter cleanup errors on some platforms. `sys.exit(0)` exits cleanly at the OS process level.

---

## 12. Course context

Built as a programming exercise covering:

- Fetching and parsing JSON from a REST API with `requests`
- Decoding HTML character entities with Python's built-in `html` module
- Designing a True/False quiz with OOP state management (`Question`, `QuizBrain`)
- Building a Tkinter GUI with `Canvas`, `PhotoImage`, `Button`, and `Label`
- Grid layout management in tkinter
- Delayed callbacks with `root.after()`

The advanced build extends into:

- Model-View separation (pure-logic modules vs. UI module)
- Dependency injection via constructor callbacks
- Centralised configuration
- Defensive UI patterns (button locking, keyboard shortcuts)
- Lazy vs. eager execution at module import time

See [docs/COURSE_NOTES.md](docs/COURSE_NOTES.md) for the full concept breakdown.

---

## 13. Dependencies

| Module | Used in | Purpose |
|--------|---------|---------|
| `tkinter` | `original/ui.py`, `advanced/display.py` | GUI framework |
| `requests` | `original/data.py`, `advanced/data.py` | HTTP GET to Open Trivia Database |
| `html` | `original/data.py`, `advanced/data.py` | Decode HTML entities in question text |
| `pathlib.Path` | `original/ui.py`, `advanced/display.py`, `advanced/main.py`, `menu.py` | Resolve file paths relative to each source file |
| `subprocess` | `menu.py` | Launch the selected build as a child process |
| `sys` | `menu.py`, `advanced/main.py`, `advanced/display.py` | Executable path, `sys.path` insertion, `sys.exit()` |
| `os` | `menu.py` | `os.system()` to clear the terminal before each menu render |
| `typing.Callable` | `advanced/display.py` | Type hints for callback parameters |
