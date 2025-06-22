from config import MAP_DIR, PROBLEM_SOLVING_TIME
import os
from src.game_state import GameState
from src.map_loader import load_map
from src.algorithms import Algorithms
import time
import re
from multiprocessing import Process, Queue
import pygame
from src.algorithm_generator import AlgorithmGenerator

# === Thêm vào đầu file game_manager.py hoặc một file riêng ===

def run_algorithm(algo_func, state, output_queue):
    solution, n_explored_node, solving_time = algo_func(state)
    output_queue.put((solution, n_explored_node, solving_time))

# handle game logic and algorithms for solving Sokoban puzzles
class GameManager:
    solution_frame_counter = 0
    solution_frames_per_action = 20
    visualize_frame_counter = 0
    visualize_frames_per_action = 20

    algorithms = {
        "DFS": Algorithms.dfs,
        "BFS": Algorithms.bfs,
        "UCS": Algorithms.ucs,
        "A*": Algorithms.a_star,
        "IDDFS": Algorithms.iddfs,
        # "BI-DIRECTIONAL": Algorithms.bi_directional,
        "BEAM": Algorithms.beam,
        "IDA*": Algorithms.ida_star,
        "EHC": Algorithms.enforced_hill_climbing,
    }

    algorithm_generators = {
        "DFS": AlgorithmGenerator.dfs_generator,
        "BFS": AlgorithmGenerator.bfs_generator,
        "UCS": AlgorithmGenerator.ucs_generator,
        "A*": AlgorithmGenerator.a_star_generator,
        "IDDFS": AlgorithmGenerator.iddfs_generator,
        # "BI-DIRECTIONAL": AlgorithmGenerator.bi_directional_generator,  # nếu có
        "BEAM": AlgorithmGenerator.beam_generator,
        "IDA*": AlgorithmGenerator.ida_star_generator,
        "EHC": AlgorithmGenerator.enforced_hill_climbing_generator,
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

    status_message = ""

    _algo_process = None
    _algo_output_queue = None
    _start_time = None

    search_generator = None

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
    def start_algorithm(algo_name):
        if algo_name not in GameManager.available_algo_names:
            raise ValueError(f"Algorithm '{algo_name}' is not defined.")

        GameManager.actions = None
        GameManager.solution_rendering_step = 0
        GameManager.n_explored_nodes = 0
        GameManager.solving_time = 0

        GameManager.current_state = GameManager.initial_state
        temp_state = GameManager.initial_state

        GameManager.status_message = "Solving..."
        GameManager._start_time = time.time()
        GameManager._algo_output_queue = Queue()
        GameManager._algo_process = Process(
            target=run_algorithm,
            args=(GameManager.algorithms[algo_name], temp_state, GameManager._algo_output_queue)
        )
        GameManager._algo_process.start()

    @staticmethod
    def update_algorithm():
        if GameManager._algo_process is None:
            return

        current_time = time.time()
        if current_time - GameManager._start_time >= PROBLEM_SOLVING_TIME:
            if GameManager._algo_process.is_alive():
                GameManager._algo_process.terminate()
            GameManager.status_message = f"Timeout. No solution found after {PROBLEM_SOLVING_TIME} s."
            GameManager.actions = None
            GameManager._algo_process = None
            return

        if not GameManager._algo_output_queue.empty():
            solution, n_explored_node, solving_time = GameManager._algo_output_queue.get()
            solving_time = int((current_time - GameManager._start_time) * 1000) # Comment this line if you want to use the solving_time from the algorithm
            GameManager.solving_time = solving_time
            GameManager.n_explored_nodes = n_explored_node

            if solution is None:
                GameManager.status_message = "No solution found."
                GameManager.actions = None
            else:
                GameManager.status_message = f""
                GameManager.actions = iter(solution)

            GameManager._algo_process = None

    @staticmethod
    def start_visualization(algo_name):
        if algo_name not in GameManager.algorithm_generators:
            raise ValueError(f"Algorithm '{algo_name}' does not support visualization.")

        GameManager.search_generator = GameManager.algorithm_generators[algo_name](GameManager.initial_state)
        GameManager.solution_rendering_step = 0
        GameManager.n_explored_nodes = 0
        GameManager.solving_time = 0
        GameManager.status_message = "Visualizing..."
        GameManager.current_state = GameManager.initial_state
        GameManager.actions = None

# Call this early in your main game setup to initialize maps
GameManager.load_map_files()