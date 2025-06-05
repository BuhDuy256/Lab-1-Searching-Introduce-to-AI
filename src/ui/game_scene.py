from .renderer import Renderer
from config import WHITE, TILE_SIZE
from src.ui.button import Button
import pygame

class GameScene:
    def __init__(self, screen):
        self.screen = screen

        self.buttons: list[Button] = []

        self.create_buttons()

    def create_buttons(self):
        #example button creation
        button = Button(50, 50, 200, 50, "Start Game", pygame.font.Font(None, 36), action=self.test_action, 
                        hover_color=(200, 200, 200), text_color=(0, 0, 0))
        
        self.buttons.append(button)
        
    def update(self):
        pass

    def render(self, screen):
        self.screen.fill(WHITE)
        for button in self.buttons:
            button.render(screen)

        Renderer.render_game_state(self.screen)

    def test_action(self):
        print("Alo alo")