from .game_object import GameObject

class Floor(GameObject):
    def __init__(self, x, y, width, height, sprite=None):
        super().__init__(x, y, width, height, sprite)
        self.active = False  # Floors are not updated
        self.layer = 5