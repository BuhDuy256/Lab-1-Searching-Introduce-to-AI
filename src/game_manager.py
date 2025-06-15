from config import MAP_DIR
import os
from src.game_state import GameState
from src.map_loader import load_map
from src.algorithms import Algorithms
import time
import re
from multiprocessing import Process, Queue
import pygame

# === Thêm vào đầu file game_manager.py hoặc một file riêng ===

def run_algorithm(algo_func, state, output_queue):
    solution, n_explored_node = algo_func(state)
    output_queue.put((solution, n_explored_node))

# handle game logic and algorithms for solving Sokoban puzzles
class GameManager:
    frame_counter = 0
    frames_per_action = 10
    current_action = None

    algorithms = {
        "DFS": Algorithms.dfs,
        "BFS": Algorithms.bfs,
        "UCS": Algorithms.ucs,
        "A-Star": Algorithms.a_star,
        "IDDFS": Algorithms.iddfs,
    }
    available_algo_names = list(algorithms.keys())
    selected_map_idx = 0
    selected_algo_idx = 0

    # When an algorithm is applied
    actions = []
    solution_rendering_step = 0
    n_explored_nodes = 0
    solving_time = 0

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

        # Block Handle Event
        pygame.event.set_blocked(None)

        output_queue = Queue()
        process = Process(target=run_algorithm, args=(GameManager.algorithms[algo_name], temp_state, output_queue))

        start = time.time()
        process.start()
        process.join(5)  # wait max 5 seconds
        end = time.time()

        solving_time = int((end - start) * 1000)

        # Unblock Handle Event
        pygame.event.set_allowed(None)

        if process.is_alive():
            process.terminate()
            process.join()
            print(f"Algorithm '{algo_name}' took {solving_time} ms.")
            print("⏰ Timeout: No solution found in 5 seconds.")
            GameManager.actions = None
            GameManager.n_explored_nodes = 0
            GameManager.solving_time = solving_time
            return

        if not output_queue.empty():
            solution, n_explored_node = output_queue.get()
        else:
            solution, n_explored_node = None, 0

        print(f"Algorithm '{algo_name}' took {solving_time} ms.")
        GameManager.n_explored_nodes = n_explored_node
        GameManager.solving_time = solving_time

        if solution is None:
            print("No solution found.")
            GameManager.actions = None
        else:
            GameManager.actions = iter(solution)

# Call this early in your main game setup to initialize maps
GameManager.load_map_files()