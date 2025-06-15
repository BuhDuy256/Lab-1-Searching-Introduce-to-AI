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

        max_depth = 50
        n_explored_nodes = 0

        for depth_limit in range(max_depth):
            visited = set()
            result = dls(initial_state, depth_limit, visited)
            if result is not None:
                return result, n_explored_nodes

        return None, n_explored_nodes

    # Very difficult to solve Sokuban Problem
    # @staticmethod
    # def bi_directional(initial_state: GameState):
    #    pass

    @staticmethod
    def beam(initial_state: GameState):
        beam_width = 5
        from itertools import count

        distances = initial_state.get_mahattan_distances_from_goal_to_all_nodes()

        def heuristic(state: GameState):
            h_value = 0
            for box_position in state.box_positions:
                if box_position in distances:
                    h_value += distances[box_position]
                else:
                    h_value += float('inf')
            return h_value

        counter = count()
        frontier = [(heuristic(initial_state), next(counter), initial_state)]
        n_explored_nodes = 0
        visited = set()

        while frontier:
            next_frontier = []

            for _, _, current_state in frontier:
                if current_state in visited:
                    continue
                visited.add(current_state)
                n_explored_nodes += 1

                if current_state.is_win():
                    return current_state.get_path(), n_explored_nodes

                for action, action_cost in current_state.get_possible_actions():
                    next_state = current_state.apply_action(action, action_cost)
                    if next_state in visited:
                        continue
                    next_frontier.append((heuristic(next_state), next(counter), next_state))

            frontier = sorted(next_frontier)[:beam_width]

        return None, n_explored_nodes

    @staticmethod
    def ida_star(initial_state: GameState):
        distances = initial_state.get_mahattan_distances_from_goal_to_all_nodes()

        def heuristic(state: GameState):
            h_value = 0
            for box_position in state.box_positions:
                if box_position in distances:
                    h_value += distances[box_position]
                else:
                    h_value += float('inf')
            return h_value

        def backtrack(state: GameState, g: int, threshold: float, visited: set):
            nonlocal n_explored_nodes, next_threshold

            f = g + heuristic(state)
            if f > threshold:
                next_threshold = min(next_threshold, f)
                return None

            n_explored_nodes += 1
            if state.is_win():
                return state.get_path()

            visited.add(state)

            for action, action_cost in state.get_possible_actions():
                next_state = state.apply_action(action, action_cost)
                if next_state in visited:
                    continue
                result = backtrack(next_state, g + action_cost, threshold, visited)
                if result is not None:
                    return result

            visited.remove(state)
            return None

        threshold = heuristic(initial_state)
        n_explored_nodes = 0

        while True:
            visited = set()
            next_threshold = float('inf')
            result = backtrack(initial_state, 0, threshold, visited)
            if result is not None:
                return result, n_explored_nodes
            if next_threshold == float('inf'):
                return None, n_explored_nodes
            threshold = next_threshold

    @staticmethod
    def enforced_hill_climbing(initial_state: GameState):
        from collections import deque

        distances = initial_state.get_mahattan_distances_from_goal_to_all_nodes()

        def heuristic(state: GameState):
            h_value = 0
            for box_position in state.box_positions:
                if box_position in distances:
                    h_value += distances[box_position]
                else:
                    h_value += float('inf')
            return h_value

        def bfs_find_better_state(start_state, current_h):
            visited = set()
            queue = deque()
            queue.append(start_state)
            visited.add(start_state)

            while queue:
                state = queue.popleft()

                for action, action_cost in state.get_possible_actions():
                    next_state = state.apply_action(action, action_cost)
                    if next_state in visited:
                        continue

                    h = heuristic(next_state)
                    if h < current_h:
                        return next_state
                    queue.append(next_state)
                    visited.add(next_state)

            return None  # Không tìm thấy state tốt hơn

        current_state = initial_state
        n_explored_nodes = 0

        while True:
            current_h = heuristic(current_state)
            n_explored_nodes += 1

            if current_state.is_win():
                return current_state.get_path(), n_explored_nodes

            neighbors = []
            for action, action_cost in current_state.get_possible_actions():
                next_state = current_state.apply_action(action, action_cost)
                neighbors.append((heuristic(next_state), next_state))

            # Tìm neighbor tốt hơn hiện tại
            better_neighbors = [s for h, s in neighbors if h < current_h]

            if better_neighbors:
                current_state = min(better_neighbors, key=heuristic)
            else:
                # Thực hiện BFS để tìm state tốt hơn
                next_state = bfs_find_better_state(current_state, current_h)
                if next_state is None:
                    return None, n_explored_nodes  # Không còn state tốt hơn
                current_state = next_state