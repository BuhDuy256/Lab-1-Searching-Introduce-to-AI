from .game_object import GameObject

class Wall(GameObject):
    def __init__(self, x, y, width, height, sprite=None):
        super().__init__(x, y, width, height, sprite)
        self.active = False  # Walls are not updated
        
        self.layer = 5