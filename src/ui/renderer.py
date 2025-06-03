from config import TEXT_COLOR

# render các game object dựa vào game state
class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.current_game_state = None

    def render_board(screen, game_state, offset_x=0, offset_y=0):
        pass

    def render_text(screen, text, position, font, color=TEXT_COLOR, center=False):
        pass
    
    def render_player(screen, player, offset_x=0, offset_y=0):
        pass
    
    def render_boxes(screen, boxes, offset_x=0, offset_y=0):
        pass
    
    def render_goals(screen, goals, offset_x=0, offset_y=0):
        pass
    
    def render_floors(screen, floors, offset_x=0, offset_y=0):
        pass
    
    def render_walls(screen, walls, offset_x=0, offset_y=0):
        pass