from .game_manager import GameManager
import pygame

class GameObject:
    # mấy cái sprite load sẵn trong file config.py hoặc rảnh thì tạo file riêng để load asset
    def __init__(self, x, y, width, height, sprite = None):
        self.layer = 0 
        # Determine the rendering order, smaller layers are rendered first
        # Layer values should be 5, 10, 15, ...

        self.visible = True # Render if True, otherwise not
        self.active = True # Update if True, otherwise not
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.sprite = sprite
        
        if sprite is not None:
            self.sprite = pygame.transform.scale(self.sprite, (self.width, self.height))
            
    def set_position(self, x, y):
        self.x = x
        self.y = y

    def start(self):
        pass

    def reset(self):
        pass

    def update(self):
        pass

    def render(self, screen):
        if self.sprite:
            screen.blit(self.sprite, (self.x, self.y))