# Window
WINDOW_TITLE = "Quizzler"
WINDOW_PADDING_X = 20
WINDOW_PADDING_Y = 20

# Colours
THEME_COLOR = "#375362"
CANVAS_BG = "white"
FEEDBACK_CORRECT_COLOR = "green"
FEEDBACK_WRONG_COLOR = "red"
LABEL_FG = "white"

# Canvas
CANVAS_WIDTH = 300
CANVAS_HEIGHT = 250
CANVAS_TEXT_WIDTH = 280
CANVAS_TEXT_X = 150
CANVAS_TEXT_Y = 125

# Fonts
FONT_SCORE = ("Arial", 12, "bold")
FONT_QUESTION = ("Arial", 20, "italic")

# Timing / delays
FEEDBACK_DELAY_MS = 1000

# Quiz / API
API_URL = "https://opentdb.com/api.php"
QUESTION_AMOUNT = 10
QUESTION_TYPE = "boolean"

# Available categories (0 = any / no filter)
CATEGORIES: dict[str, int] = {
    "Any": 0,
    "General Knowledge": 9,
    "Books": 10,
    "Film": 11,
    "Music": 12,
    "Television": 14,
    "Video Games": 15,
    "Science & Nature": 17,
    "Computers": 18,
    "Mathematics": 19,
    "Mythology": 20,
    "Sports": 21,
    "Geography": 22,
    "History": 23,
    "Animals": 27,
}
