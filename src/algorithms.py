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
            nonlocal n_explored_nodes
            if current_state in visited:
                return None

            n_explored_nodes += 1

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

        n_explored_nodes = 0

        return _dfs(initial_state, set()), n_explored_nodes

    @staticmethod
    def bfs(initial_state: GameState):
        q = Queue()
        visited = set()
        n_explored_nodes = 0

        q.put(initial_state)
        visited.add(initial_state)

        while not q.empty():
            current_state = q.get()
            n_explored_nodes += 1

            if current_state.is_win():
                return current_state.get_path(), n_explored_nodes

            for action, action_cost in current_state.get_possible_actions():
                next_state = current_state.apply_action(action, action_cost)

                if next_state in visited:
                    continue

                q.put(next_state)
                visited.add(next_state)

        return None, 0

    @staticmethod
    def ucs(initial_state: GameState):
        counter = count() # Handle case if 2 state have the same cost, it will compare id next
        frontier = []
        heapq.heappush(frontier, (initial_state.cost, next(counter), initial_state))
        visited = set()
        min_cost = {initial_state: initial_state.cost}
        n_explored_nodes = 0

        while frontier:
            _, _, current_state = heapq.heappop(frontier)

            if current_state in visited:
                continue
            visited.add(current_state)
            n_explored_nodes += 1

            if current_state.is_win():
                return current_state.get_path(), n_explored_nodes

            for action, action_cost in current_state.get_possible_actions():
                next_state = current_state.apply_action(action, action_cost)
                total_cost = next_state.cost

                if next_state not in min_cost or total_cost < min_cost[next_state]:
                    min_cost[next_state] = total_cost
                    heapq.heappush(frontier, (total_cost, next(counter), next_state))

        return None, 0

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
        n_explored_nodes = 0

        while frontier:
            _, _, current_state = heappop(frontier)

            if current_state in visited:
                continue
            visited.add(current_state)
            n_explored_nodes += 1

            if current_state.is_win():
                return current_state.get_path(), n_explored_nodes

            for action, action_cost in current_state.get_possible_actions():
                next_state = current_state.apply_action(action, action_cost)
                total_cost = next_state.cost

                if next_state not in min_cost or total_cost < min_cost[next_state]:
                    min_cost[next_state] = total_cost
                    estimated_cost = total_cost + heuristic(next_state)
                    heappush(frontier, (estimated_cost, next(counter), next_state))

        return None, 0

    @staticmethod
    def iddfs(initial_state: GameState):
        import sys

        def dls(current_state: GameState, depth: int, visited: set):
            nonlocal n_explored_nodes
            if current_state in visited:
                return None
            if depth < 0:
                return None

            n_explored_nodes += 1

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
        n_explored_nodes = 0

        for depth_limit in range(max_depth):
            visited = set()
            result = dls(initial_state, depth_limit, visited)
            if result is not None:
                return result, n_explored_nodes

        return None, n_explored_nodes

    @staticmethod
    def bi_directional(initial_state: GameState):
       pass

    @staticmethod
    def beam(initial_state: GameState, beam_width=5):
        pass

    @staticmethod
    def ida_star(initial_state: GameState):
        pass