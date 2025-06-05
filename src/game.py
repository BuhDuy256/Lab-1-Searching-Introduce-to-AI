import os
import pygame
from config import *
from src.time_manager import Time
from src.ui.game_scene import GameScene
from src.game_manager import GameManager
from src.ui.renderer import Renderer

# aka scene_manager
class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init() # Initialize font module
        Time.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Sokoban AI Solver")

        Renderer.load_assets()

        self.current_scene = GameScene(self.screen)
        
        self.running = True
            
    def reset(self):
        pass

    def run(self):
        GameManager.choose_map(0)
        while self.running:
            self.handle_events()

            self.update()
            self.render()
        
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Pass event to buttons if not currently solving/animating heavily
            if not GameManager.is_solving:
                for button in self.current_scene.buttons:
                    if button.handle_event(event):
                        break  # Stop after the first button handles the event

    def update(self):
        # Game logic updates that happen continuously (not much in this type of game)
        Time.update()
        self.current_scene.update()

    def render(self):
        self.current_scene.render(self.screen)
        pygame.display.flip()