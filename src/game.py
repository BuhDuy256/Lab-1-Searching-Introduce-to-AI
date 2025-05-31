import os
import pygame
from config import *
from src.time_manager import Time
from src.ui.game_scene import GameScene

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init() # Initialize font module
        Time.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Sokoban AI Solver")

        self.current_scene = GameScene(self.screen)

        self.maps = self.load_map_files()
        self.algorithms = {
            # "BFS": solve_bfs,
            # "DFS": solve_dfs,
            # "UCS": solve_ucs,
            # "A* (Simple)": lambda s: solve_a_star(s, simple_heuristic),
            # "A* (Advanced)": lambda s: solve_a_star(s, advanced_heuristic_astar),
        }
        self.available_algo_names = list(self.algorithms.keys())

        self.selected_map_idx = 0
        self.selected_algo_idx = 0

        self.is_solving = False
        
        self.running = True

    def load_map_files(self):
        try:
            return sorted([f for f in os.listdir(MAP_DIR) if f.endswith(".txt")])
        except FileNotFoundError:
            print(f"Error: Map directory '{MAP_DIR}' not found.")
            return []
            
    def reset(self):
        pass

    def run(self):
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
            if not self.is_solving:
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