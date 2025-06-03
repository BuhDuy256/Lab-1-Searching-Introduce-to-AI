from .game_object import GameObject
import pygame

class Player(GameObject):
    def __init__(self, x, y, width, height, sprite=None):
        super().__init__(x, y, width, height, sprite)
        self.layer = 15