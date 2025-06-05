from .game_object import GameObject
import pygame
from config import TILE_SIZE

class Player(GameObject):
    def __init__(self, x, y, width, height, sprite=None):
        super().__init__(x, y, width, height, sprite)
        self.layer = 15
        
    def __init__(self, x, y, sprite=None):
        super().__init__(x, y, TILE_SIZE, TILE_SIZE, sprite)
        self.layer = 15