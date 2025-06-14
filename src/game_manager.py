from config import MAP_DIR
import os
from src.game_state import GameState
from src.map_loader import load_map
from src.algorithms import Algorithms
import time
import re

# handle game logic and algorithms for solving Sokoban puzzles
class GameManager:
    algorithms = {
        # "DFS": lambda state: Algorithms.dfs(state),
        "BFS": lambda state: Algorithms.bfs(state),
        "UCS": lambda state: Algorithms.ucs(state),
        "A-Star": lambda state: Algorithms.a_star(state),
        # "IDDFS": lambda state: Algorithms.iddfs(state),
        # "BI-DIRECTIONAL": lambda state: Algorithms.bi_directional(state),
        # "BEAM": lambda state: Algorithms.beam(state),
        # "IDA-Star": lambda state: Algorithms.ida_star(state),
    }
    available_algo_names = list(algorithms.keys())
    selected_map_idx = 0
    selected_algo_idx = 0

    # is_solving = False
    actions = []

    maps = []
    current_state: GameState = None
    initial_state: GameState = None

    @classmethod
    def load_map_files(cls):
        try:
            all_files = os.listdir(MAP_DIR)
            cls.maps = sorted(
                [f for f in all_files if re.match(r'^level\d+\.txt$', f)],
                key=lambda name: int(re.findall(r'\d+', name)[0])
            )
        except FileNotFoundError:
            print(f"Error: Map directory '{MAP_DIR}' not found.")
            cls.maps = []

    @classmethod
    def get_total_maps(cls):
        try:
            all_files = os.listdir(MAP_DIR)
            valid_maps = [f for f in all_files if re.match(r'^level\d+\.txt$', f)]
            return len(valid_maps)
        except FileNotFoundError:
            print(f"Error: Map directory '{MAP_DIR}' not found.")
            return 0

    @staticmethod
    def hello():
        print("Hello from GameManager!")
        
    @staticmethod
    def choose_map(index):
        GameManager.selected_map_idx = index
        GameManager.initial_state = load_map(os.path.join(MAP_DIR, GameManager.maps[index]))
        GameManager.current_state = GameManager.initial_state

    @staticmethod
    def apply_algorithm(algo_name):
        if algo_name not in GameManager.available_algo_names:
            raise ValueError(f"Algorithm '{algo_name}' is not defined.")
        GameManager.current_state = GameManager.initial_state
        temp_state = GameManager.initial_state

        start = time.time()
        solution = GameManager.algorithms[algo_name](temp_state)
        end = time.time()
        print(f"Algorithm '{algo_name}' took {int((end - start) * 1000)} ms.")
        if solution is None:
            GameManager.actions = None
            # GameManager.is_solving = False
            print("No solution found.")
        else:
            GameManager.actions = iter(solution)
            # GameManager.is_solving = True

# Call this early in your main game setup to initialize maps
GameManager.load_map_files()