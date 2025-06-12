# Screen dimensions
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 640
FPS = 100

# Tile size for rendering the game
TILE_SIZE = 32

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

PLAYER_COLOR = BLUE
BOX_COLOR = GREEN
WALL_COLOR = BLACK
GOAL_COLOR = RED
FLOOR_COLOR = WHITE
TEXT_COLOR = BLACK

# Map characters
PLAYER_CHAR = '@'
PLAYER_ON_GOAL_CHAR = '+'  # Player on a goal
BOX_CHAR = '$'
BOX_ON_GOAL_CHAR = '*'     # Box on a goal
WALL_CHAR = '#'
GOAL_CHAR = '.'
FLOOR_CHAR = ' '

# Paths (adjust as needed)
MAP_DIR = "assets/maps/"
FONT_NAME = None  # Use Pygame default font, or specify e.g. 'arial'
FONT_SIZE_MEDIUM = 30
FONT_SIZE_SMALL = 20

# Animation speed for solution playback (delay in ms between steps)
ANIMATION_DELAY = 200  # milliseconds

# Button
BUTTON_WIDTH = 180
BUTTON_HEIGHT = 40