import time

from src.game_state import GameState
from queue import Queue
from heapq import heappush, heappop
import heapq
from itertools import count
import sys

class Algorithms:
    @staticmethod
    def dfs(initial_state: GameState):
        def _dfs(current_state: GameState, visited: set):
            if current_state in visited:
                return None

            if current_state.is_win():
                return current_state.get_path()

            visited.add(current_state)

            for action, action_cost in current_state.get_possible_actions():
                next_state = current_state.apply_action(action, action_cost)
                result = _dfs(next_state, visited=visited)
                if result is not None:
                    return result

            visited.remove(current_state)

            return None

        return _dfs(initial_state, set())

    @staticmethod
    def bfs(initial_state: GameState):
        q = Queue()
        visited = set()

        q.put(initial_state)
        visited.add(initial_state)

        while not q.empty():
            current_state = q.get()

            if current_state.is_win():
                return current_state.get_path()

            for action, action_cost in current_state.get_possible_actions():
                next_state = current_state.apply_action(action, action_cost)

                if next_state in visited:
                    continue

                q.put(next_state)
                visited.add(next_state)

        return None

    @staticmethod
    def ucs(initial_state: GameState):
        counter = count() # Handle case if 2 state have the same cost, it will compare id next
        frontier = []
        heapq.heappush(frontier, (initial_state.cost, next(counter), initial_state))
        visited = set()
        min_cost = {initial_state: initial_state.cost}

        while frontier:
            _, _, current_state = heapq.heappop(frontier)

            if current_state in visited:
                continue
            visited.add(current_state)

            if current_state.is_win():
                return current_state.get_path()

            for action, action_cost in current_state.get_possible_actions():
                next_state = current_state.apply_action(action, action_cost)
                total_cost = next_state.cost

                if next_state not in min_cost or total_cost < min_cost[next_state]:
                    min_cost[next_state] = total_cost
                    heapq.heappush(frontier, (total_cost, next(counter), next_state))

        return None

    @staticmethod
    def a_star(initial_state: GameState):
        distances = initial_state.get_mahattan_distances_from_goal_to_all_nodes()
        counter = count()

        def heuristic(state: GameState):
            h_value = 0
            for box_position in state.box_positions:
                if box_position in distances:
                    h_value += distances[box_position]
                else:
                    float('inf')

            return h_value

        start = time.time()

        frontier = []
        heappush(frontier, (heuristic(initial_state) + initial_state.cost, next(counter), initial_state))
        visited = set()
        min_cost = {initial_state: initial_state.cost}

        while frontier:
            _, _, current_state = heappop(frontier)

            if current_state in visited:
                continue
            visited.add(current_state)

            if current_state.is_win():
                return current_state.get_path()

            for action, action_cost in current_state.get_possible_actions():
                next_state = current_state.apply_action(action, action_cost)
                total_cost = next_state.cost

                if next_state not in min_cost or total_cost < min_cost[next_state]:
                    min_cost[next_state] = total_cost
                    estimated_cost = total_cost + heuristic(next_state)
                    heappush(frontier, (estimated_cost, next(counter), next_state))

        return None

    @staticmethod
    def iddfs(initial_state: GameState):
        def dls(current_state: GameState, depth: int, visited: set):
            if current_state in visited:
                return None
            if depth < 0:
                return None

            if current_state.is_win():
                return current_state.get_path()

            visited.add(current_state)

            for action, action_cost in current_state.get_possible_actions():
                next_state = current_state.apply_action(action, action_cost)
                result = dls(next_state, depth - 1, visited)
                if result is not None:
                    return result

            visited.remove(current_state)
            return None

        max_depth = sys.maxsize
        for depth_limit in range(max_depth):
            result = dls(initial_state, depth_limit, set())
            if result is not None:
                return result

        return None

    @staticmethod
    def bi_directional(initial_state: GameState):
       pass

    @staticmethod
    def beam(initial_state: GameState, beam_width=5):
        from heapq import heappush, heappop
        from itertools import count

        distances = initial_state.get_mahattan_distances_from_goal_to_all_nodes()
        counter = count()

        def heuristic(state: GameState):
            h_value = 0
            for box_position in state.box_positions:
                if box_position in distances:
                    h_value += distances[box_position]
                else:
                    return float('inf')
            return h_value

        frontier = [initial_state]
        visited = set()
        min_cost = {initial_state: 0}

        while frontier:
            candidates = []

            for state in frontier:
                if state.is_win():
                    return state.get_path()

                for action, action_cost in state.get_possible_actions():
                    next_state = state.apply_action(action, action_cost)

                    if next_state in visited:
                        continue

                    total_cost = next_state.cost
                    h = heuristic(next_state)

                    if h == float('inf'):
                        continue

                    if next_state not in min_cost or total_cost < min_cost[next_state]:
                        min_cost[next_state] = total_cost
                        heappush(candidates, (h, next(counter), next_state))

            frontier = [heappop(candidates)[2] for _ in range(min(beam_width, len(candidates)))]
            visited.update(frontier)

        return None

    @staticmethod
    def ida_star(initial_state: GameState):
        distances = initial_state.get_mahattan_distances_from_goal_to_all_nodes()

        def heuristic(state: GameState):
            h_value = 0
            for box_position in state.box_positions:
                if box_position in distances:
                    h_value += distances[box_position]
                else:
                    return float('inf')
            return h_value

        def search(state: GameState, g: int, threshold: int, visited: set):
            f = g + heuristic(state)
            if f > threshold:
                return f

            if state.is_win():
                return state.get_path()

            visited.add(state)
            min_threshold = float('inf')

            for action, action_cost in state.get_possible_actions():
                next_state = state.apply_action(action, action_cost)
                if next_state in visited:
                    continue

                result = search(next_state, g + action_cost, threshold, visited)
                if isinstance(result, list):
                    return result
                if isinstance(result, (int, float)):
                    min_threshold = min(min_threshold, result)

            visited.remove(state)
            return min_threshold

        threshold = heuristic(initial_state)
        visited = set()

        while True:
            result = search(initial_state, 0, threshold, visited)
            if isinstance(result, list):
                return result  # Found solution
            if result == float('inf'):
                return None  # No solution
            threshold = result  # Increase threshold and retry