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
        visited = set()
        stack = [(initial_state, [])]  # (state, path_so_far)
        n_explored_nodes = 0

        while stack:
            current_state, path = stack.pop()

            if current_state in visited:
                continue

            visited.add(current_state)
            n_explored_nodes += 1

            if current_state.is_win():
                return path, n_explored_nodes

            for action, action_cost in reversed(current_state.get_possible_actions()):
                next_state = current_state.apply_action(action, action_cost)
                stack.append((next_state, path + [action]))

        return None, n_explored_nodes

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
                    return float('inf')
            return h_value

        frontier = []
        heappush(frontier, (heuristic(initial_state), next(counter), initial_state))
        min_cost = {initial_state: 0}
        n_explored_nodes = 0

        while frontier:
            _, _, current_state = heappop(frontier)
            g = min_cost[current_state]
            n_explored_nodes += 1

            if current_state.is_win():
                return current_state.get_path(), n_explored_nodes

            for action, action_cost in current_state.get_possible_actions():
                next_state = current_state.apply_action(action, action_cost)
                new_cost = g + action_cost

                if new_cost < min_cost.get(next_state, float('inf')):
                    min_cost[next_state] = new_cost
                    f = new_cost + heuristic(next_state)
                    heappush(frontier, (f, next(counter), next_state))

        return None, 0

    @staticmethod
    def iddfs(initial_state: GameState, max_depth: int = 100):
        n_explored_nodes = 0

        for depth_limit in range(max_depth):
            stack = [(initial_state, 0)]  # (state, depth)
            visited = set()

            while stack:
                current_state, depth = stack.pop()

                if current_state in visited:
                    continue
                visited.add(current_state)
                n_explored_nodes += 1

                if current_state.is_win():
                    return current_state.get_path(), n_explored_nodes

                if depth < depth_limit:
                    for action, action_cost in reversed(current_state.get_possible_actions()):
                        next_state = current_state.apply_action(action, action_cost)
                        stack.append((next_state, depth + 1))

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
                if box_position not in distances:
                    return float('inf')
                h_value += distances[box_position]
            return h_value

        threshold = heuristic(initial_state)
        n_explored_nodes = 0

        while True:
            stack = [(initial_state, 0)]  # (state, g)
            visited = set()
            next_threshold = float('inf')

            while stack:
                current_state, g = stack.pop()
                f = g + heuristic(current_state)

                if f > threshold:
                    next_threshold = min(next_threshold, f)
                    continue

                if current_state in visited:
                    continue
                visited.add(current_state)
                n_explored_nodes += 1

                if current_state.is_win():
                    return current_state.get_path(), n_explored_nodes

                for action, action_cost in reversed(current_state.get_possible_actions()):
                    next_state = current_state.apply_action(action, action_cost)
                    if next_state in visited:
                        continue
                    stack.append((next_state, g + action_cost))

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
            nonlocal n_explored_nodes
            visited = set()
            queue = deque()
            queue.append(start_state)
            visited.add(start_state)

            while queue:
                state = queue.popleft()
                n_explored_nodes += 1  # Tăng biến đếm khi duyệt node

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

            better_neighbors = [s for h, s in neighbors if h < current_h]

            if better_neighbors:
                current_state = min(better_neighbors, key=heuristic)
            else:
                next_state = bfs_find_better_state(current_state, current_h)
                if next_state is None:
                    return None, n_explored_nodes
                current_state = next_state
