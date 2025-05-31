from config import TEXT_COLOR

# để tính sau
class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.current_game_state = None

    def render_board(screen, game_state, offset_x=0, offset_y=0):
        pass

    def render_text(screen, text, position, font, color=TEXT_COLOR, center=False):
        pass