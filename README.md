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
| In-app category selection (Tkinter) | — | ✓ |
| Keyboard shortcuts (T / F) | — | ✓ |
| Button lock during feedback window | — | ✓ |
| Centralised configuration (`config.py`) | — | ✓ |
| UI / logic fully separated | — | ✓ |
| `fetch_questions()` function (lazy API call) | — | ✓ |

---

## 3. Controls

**Category selector** *(advanced build only)*

| Input | Action |
|-------|--------|
| Click a row | Highlight a category |
| Double-click a row | Select category and start quiz |
| `Enter` | Select highlighted category and start quiz |
| Click "Start Quiz →" | Select highlighted category and start quiz |

**Gameplay**

| Input | Action |
|-------|--------|
| Click ✓ (True button) | Answer True |
| Click ✗ (False button) | Answer False |
| `T` *(advanced build only)* | Answer True via keyboard |
| `F` *(advanced build only)* | Answer False via keyboard |

---

## 4. App flow

### Original

1. `data.py` calls the Open Trivia Database API at import time and decodes HTML entities.
2. 10 True/False questions from the Computers category load into a question bank.
3. The first question appears in the canvas.
4. You click True or False.
5. The canvas flashes **green** (correct) or **red** (wrong); the score label updates immediately.
6. After 1 second the canvas resets to white and the next question loads.
7. Once all 10 questions are answered, "You've reached the end of the quiz." is shown and both buttons are disabled.

### Advanced

1. A category selector screen appears — a styled Listbox with 15 options.
2. Pick a category (click + button, double-click, or Enter).
3. The canvas briefly shows "Loading questions…" while the API call runs.
4. 10 True/False questions for the chosen category load.
5. The first question appears in the canvas.
6. You click True or False (or press `T`/`F`).
7. The canvas flashes **green** (correct) or **red** (wrong); the score label updates immediately.
8. After 1 second the canvas resets to white and the next question loads.
9. Once all 10 questions are answered, "You've reached the end of the quiz." is shown and both buttons are disabled.

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

**In-app category selection**
Before the quiz starts, a Tkinter Listbox lists 15 categories (General Knowledge, Film, Music, History, and more). Choosing "Any" sends no filter, returning a random mix across all categories. The selector and the quiz share the same window — no extra dialog or terminal prompt.

**Keyboard shortcuts**
Press `T` for True and `F` for False. No mouse required once the window has focus.

**Button lock during feedback**
Both answer buttons are disabled the instant you submit an answer and re-enabled only when the next question loads. This prevents accidental double-submissions during the 1-second feedback window.

**Centralised configuration**
All magic numbers — canvas dimensions, colours, fonts, timing, API parameters, and selector styling — live in a single `config.py`. Changing the feedback delay or question count requires editing exactly one line.

**Clean UI / logic separation**
`Display` owns every widget and has no knowledge of quiz rules. `QuizBrain` contains all game logic and has no tkinter imports. `main.py` wires the two together exclusively via callbacks.

**Lazy API call**
The original `data.py` runs the HTTP request at import time. The advanced `data.py` wraps it in `fetch_questions(category)`, so the call only fires once the user has picked a category.

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

### In-app flow — original

```
[App Start → API fetch]
     │
     ▼
┌─────────────────────────┐
│   Question displayed    │◄──────────────────────┐
└─────────────────────────┘                       │
     │                                             │
  Click ✓/✗                                        │
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

### In-app flow — advanced

```
[App Start]
     │
     ▼
┌──────────────────────────────────┐
│   Category Selector Screen       │
│   Listbox (15 options)           │
│   "Start Quiz →" button          │
└──────────────────────────────────┘
     │
  click / double-click / Enter
     │
     ▼
[Canvas: "Loading questions…"]
     │
  API fetch (after 50 ms render delay)
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
    ├── data.py                 # fetch_questions(category) — lazy API call, no tkinter
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
| `fetch_questions(category=0)` | `list[dict]` | Calls the Open Trivia DB API for the given category ID (0 = any) and returns decoded `{question, correct_answer}` dicts |

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
| `__init__(on_category_select)` | — | Builds the Tk window; shows the category selector screen |
| `start_quiz(on_true, on_false)` | `None` | Stores answer callbacks; binds `T`/`F` keys; called by `main.py` after questions are fetched |
| `render_question(text, score, answered, total)` | `None` | Resets canvas to white, shows new question text, updates score label, re-enables buttons |
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
| `SELECTOR_TITLE` | `"Choose a Category"` | Heading text on the category selector screen |
| `SELECTOR_TITLE_FONT` | `("Arial", 14, "bold")` | Font for the selector heading |
| `SELECTOR_LISTBOX_HEIGHT` | `10` | Number of visible rows in the category Listbox |
| `SELECTOR_LISTBOX_WIDTH` | `24` | Character width of the category Listbox |
| `SELECTOR_LISTBOX_FONT` | `("Arial", 12)` | Font for Listbox rows |
| `SELECTOR_BTN_TEXT` | `"Start Quiz  →"` | Label on the start button |
| `SELECTOR_BTN_FONT` | `("Arial", 12, "bold")` | Font for the start button |
| `CATEGORIES` | *(dict, 15 entries)* | Ordered mapping of display name → Open Trivia DB category ID; `0` = any |
| `API_URL` | `"https://opentdb.com/api.php"` | Open Trivia Database endpoint |
| `QUESTION_AMOUNT` | `10` | Number of questions fetched per session |
| `QUESTION_TYPE` | `"boolean"` | Open Trivia DB question type (`"boolean"` = True/False) |

---

## 10. Display layout

### Category selector screen *(advanced build only)*

```
┌──────────────────────────────────────────┐
│  (bg=#375362, padx=20, pady=20)           │
│                                           │
│         "Choose a Category"               │
│         (Arial 14 bold, white)            │
│                                           │
│  ┌────────────────────────┬─┐             │
│  │ Any                    │▲│             │
│  │ General Knowledge      │ │             │
│  │ Books                  │ │  Listbox    │
│  │ Film                   │ │  10 rows    │
│  │ Music                  │ │  visible,   │
│  │ Television             │ │  scrollable │
│  │ Video Games            │ │             │
│  │ Science & Nature       │ │             │
│  │ Computers              │▼│             │
│  └────────────────────────┴─┘             │
│                                           │
│         [ Start Quiz  → ]                 │
│         (white btn, theme text)           │
│                                           │
└──────────────────────────────────────────┘
```

### Quiz screen

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
Every number, colour string, and API parameter has a name and lives in one file. Changing the feedback delay, question count, or selector height requires editing exactly one constant.

**`on_category_select` callback drives the two-phase startup**
`Display.__init__` receives a single `on_category_select` callback instead of quiz callbacks. Once the user picks a category, that callback runs in `main.py`, fetches questions, builds the `QuizBrain`, then calls `display.start_quiz(on_true, on_false)`. This keeps `Display` unaware of quiz logic at both startup and runtime.

**`root.after(50, ...)` for the loading state**
After the selector is hidden, the quiz widgets are gridded with "Loading questions…" on the canvas. The actual API call is then scheduled with a 50 ms delay so tkinter has one render cycle to paint the loading text before the blocking network request freezes the event loop. The result: the user sees visible feedback instantly.

**Category selector in the same window, not a separate dialog**
Using `Toplevel` for category selection would create a second window and complicate focus management. Instead, the selector frame and quiz widgets share the same root window — the frame is removed from the grid when the quiz starts, and the quiz widgets are gridded in its place. No extra window is ever opened.

**`fetch_questions()` function vs module-level execution**
The original `data.py` fires the API request at import time, which means it runs even during tooling, testing, or accidental imports. Wrapping it in `fetch_questions(category)` makes the call explicit, lazy, and tied to the user's category choice.

**Button lock during feedback**
Both buttons are disabled the moment an answer is submitted and re-enabled only inside `render_question()`. Without this, clicking rapidly during the 1-second feedback window would call `check_answer()` twice on the same question, corrupting the score.

**`sys.path.insert` pattern**
`advanced/main.py` inserts its own directory at the front of `sys.path` so sibling imports (`from display import Display`) resolve correctly whether the file is run directly or via `menu.py` with a different working directory.

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
- Multi-phase UI startup (selector screen → quiz screen in one window)
- `Listbox` with scrollbar and keyboard navigation
- Blocking network calls inside a tkinter event loop and how to give visual feedback first
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
