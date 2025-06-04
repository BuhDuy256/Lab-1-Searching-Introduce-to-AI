from config import MAP_DIR
import os
from src.game_state import GameState
from src.map_loader import load_map

# handle game logic and algorithms for solving Sokoban puzzles
class GameManager:
    algorithms = {
        # "BFS": solve_bfs,
        # "DFS": solve_dfs,
        # "UCS": solve_ucs,
        # "A* (Simple)": lambda s: solve_a_star(s, simple_heuristic),
        # "A* (Advanced)": lambda s: solve_a_star(s, advanced_heuristic_astar),
    }
    available_algo_names = list(algorithms.keys())
    selected_map_idx = 0
    selected_algo_idx = 0
    is_solving = False
    maps = []
    current_state: GameState = None
    initial_state: GameState = None

    @classmethod
    def load_map_files(cls):
        try:
            cls.maps = sorted([f for f in os.listdir(MAP_DIR) if f.endswith(".txt")])
        except FileNotFoundError:
            print(f"Error: Map directory '{MAP_DIR}' not found.")
            cls.maps = []

    @staticmethod
    def hello():
        print("Hello from GameManager!")
        
    @staticmethod
    def choose_map(index):
        GameManager.initial_state = load_map(os.path.join(MAP_DIR, GameManager.maps[index]))
        GameManager.current_state = GameManager.initial_state
        

# Call this early in your main game setup to initialize maps
GameManager.load_map_files()