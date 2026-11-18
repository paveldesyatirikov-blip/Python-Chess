WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colors (RGB)
LIGHT_SQUARE = (238, 238, 210)
DARK_SQUARE = (118, 150, 86)
HIGHLIGHT = (186, 202, 68)
SELECTED_COLOR = (246, 246, 105)
CHECK_COLOR = (235, 64, 52)
BG_MENU = (40, 44, 52)
TEXT_COLOR = (255, 255, 255)
BTN_COLOR = (118, 150, 86)
BTN_HOVER = (140, 175, 100)

# Piece values for AI evaluation
PIECE_VALUES = {
    'pawn': 10,
    'knight': 30,
    'bishop': 30,
    'rook': 50,
    'queen': 90,
    'king': 900
}