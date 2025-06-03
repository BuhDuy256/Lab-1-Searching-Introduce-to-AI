from .game_manager import GameManager

class GameObject:
    def __init__(self):
        GameManager.add_game_object(self)
        self.layer = 0 
        # Determine the rendering order, smaller layers are rendered first
        # Layer values should be 5, 10, 15, ...

        self.visible = True # Render if True, otherwise not
        self.active = True # Update if True, otherwise not

    def start(self):
        pass

    def reset(self):
        pass

    def update(self):
        pass

    def render(self, screen):
        pass