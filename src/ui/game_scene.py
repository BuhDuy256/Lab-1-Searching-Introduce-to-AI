from .renderer import Renderer
from src.game_object import GameObject
from config import WHITE
from src.ui.button import Button
from src.game_manager import GameManager
import pygame

class GameScene:
    def __init__(self, screen):
        self.screen = screen
        self.renderer = Renderer(screen)

        self.game_objects: list[GameObject] = []  # List of game objects in the scene
        self.buttons: list[Button] = []

        self.create_buttons()


        self.game_objects.extend(GameManager.game_objects_queue)
        GameManager.game_objects_queue.clear()

        for game_object in self.game_objects:
            if isinstance(game_object, Button):
                self.buttons.append(game_object)

    def create_buttons(self):
        #example button creation
        Button(50, 50, 200, 50, "Start Game", pygame.font.Font(None, 36), action=self.test_action, 
                        hover_color=(200, 200, 200), text_color=(0, 0, 0))

    def update(self):
        for game_object in self.game_objects:
            game_object.update()

    def render(self, screen):
        self.screen.fill(WHITE)
        for game_object in self.game_objects:
            game_object.render(screen)

    def test_action(self):
        print("Chó là bạn, không phải tôi")