import time

from src.game_state import GameState
from queue import Queue
from heapq import heappush, heappop
import heapq
from itertools import count
from collections import deque
import sys

class Heuristics:
    @staticmethod
    def heuristic1(state: GameState, distances):
        h_value = 0
        for box_position in state.box_positions:
            if box_position in distances:
                h_value += distances[box_position]
            else:
                h_value += float('inf')
        return h_value

    @staticmethod
    def heuristic2(state, distances):
        h_value = 0

        # --- Part 1: Sum of box-to-goal distances (precomputed distances dict) ---
        for box_pos in state.box_positions:
            if box_pos in distances:
                h_value += distances[box_pos]
            else:
                h_value += float('inf')  # Penalize unreachable positions

        # --- Part 2: Sum of distances from player to all boxes (greedy + early stop) ---
        remaining_boxes = set(state.box_positions)
        visited = set()
        heap = []
        heappush(heap, (0, state.player_pos))  # (distance, position)

        while heap and remaining_boxes:
            dist, pos = heappop(heap)
            if pos in visited:
                continue
            visited.add(pos)

            if pos in remaining_boxes:
                h_value += dist  # Player to box distance
                remaining_boxes.remove(pos)
                if not remaining_boxes:
                    break  # Stop early once all boxes reached

            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = pos[0] + dr, pos[1] + dc
                next_pos = (nr, nc)
                if next_pos not in visited and not state.is_wall(next_pos):
                    heappush(heap, (dist + 1, next_pos))

        return h_value

    @staticmethod
    def heuristic3(state: GameState, distances, player_weight=0.5):
        h_value = 0

        # --- Check deadlocks ---
        for box in state.box_positions:
            if state.is_deadlock_at(box) and box not in state.goal_positions:
                return float('inf')

        # --- Part 1: Greedy box-goal matching (no goal used twice) ---
        unmatched_goals = set(state.goal_positions)
        box_goal_costs = []

        for box in state.box_positions:
            if box not in distances:
                return float('inf')  # Unreachable box

            goal_dists = [(distances[goal], goal) for goal in unmatched_goals if goal in distances]
            if not goal_dists:
                return float('inf')  # No reachable goal left

            dist, matched_goal = min(goal_dists)
            h_value += dist
            unmatched_goals.remove(matched_goal)

        # --- Part 2 (optional): Player to nearest box (weighted) ---
        remaining_boxes = set(state.box_positions)
        visited = set()
        heap = []
        heappush(heap, (0, state.player_pos))

        while heap and remaining_boxes:
            dist, pos = heappop(heap)
            if pos in visited:
                continue
            visited.add(pos)

            if pos in remaining_boxes:
                h_value += dist * player_weight
                remaining_boxes.remove(pos)
                if not remaining_boxes:
                    break

            for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                nr, nc = pos[0] + dr, pos[1] + dc
                next_pos = (nr, nc)
                if next_pos not in visited and not state.is_wall(next_pos):
                    heappush(heap, (dist + 1, next_pos))

        return h_value

class Algorithms:
    @staticmethod
    def dfs(initial_state: GameState):
        start_time = time.time()

        visited = set()
        stack = [initial_state]
        n_explored_nodes = 0

        while stack:
            current_state = stack.pop()

            if current_state in visited:
                continue

            visited.add(current_state)
            n_explored_nodes += 1

            if current_state.is_win():
                solving_time = time.time() - start_time
                return current_state.get_path(), n_explored_nodes, solving_time

            for action, action_cost in reversed(current_state.get_possible_actions()):
                next_state = current_state.apply_action(action, action_cost)
                stack.append(next_state)

        solving_time = time.time() - start_time
        return None, n_explored_nodes, solving_time

    @staticmethod
    def bfs(initial_state: GameState):
        start_time = time.time()

        q = Queue()
        visited = set()
        n_explored_nodes = 0

        q.put(initial_state)
        visited.add(initial_state)

        while not q.empty():
            current_state = q.get()
            n_explored_nodes += 1

            if current_state.is_win():
                solving_time = time.time() - start_time
                return current_state.get_path(), n_explored_nodes, solving_time

            for action, action_cost in current_state.get_possible_actions():
                next_state = current_state.apply_action(action, action_cost)

                if next_state in visited:
                    continue

                q.put(next_state)
                visited.add(next_state)

        solving_time = time.time() - start_time
        return None, n_explored_nodes, solving_time

    @staticmethod
    def ucs(initial_state: GameState):
        start_time = time.time()

        counter = count()  # Handle case if 2 states have the same cost, it will compare id next
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
                solving_time = time.time() - start_time
                return current_state.get_path(), n_explored_nodes, solving_time

            for action, action_cost in current_state.get_possible_actions():
                next_state = current_state.apply_action(action, action_cost)
                total_cost = next_state.cost

                if next_state not in min_cost or total_cost < min_cost[next_state]:
                    min_cost[next_state] = total_cost
                    heapq.heappush(frontier, (total_cost, next(counter), next_state))

        solving_time = time.time() - start_time
        return None, n_explored_nodes, solving_time

    @staticmethod
    def a_star(initial_state: GameState):
        start_time = time.time()

        distances = initial_state.get_mahattan_distances_from_goal_to_all_nodes()
        counter = count()

        frontier = []
        heappush(frontier, (Heuristics.heuristic1(initial_state, distances), next(counter), initial_state))
        min_cost = {initial_state: 0}
        n_explored_nodes = 0

        while frontier:
            _, _, current_state = heappop(frontier)
            g = min_cost[current_state]
            n_explored_nodes += 1

            if current_state.is_win():
                solving_time = time.time() - start_time
                return current_state.get_path(), n_explored_nodes, solving_time

            for action, action_cost in current_state.get_possible_actions():
                next_state = current_state.apply_action(action, action_cost)
                new_cost = g + action_cost

                if new_cost < min_cost.get(next_state, float('inf')):
                    min_cost[next_state] = new_cost
                    f = new_cost + Heuristics.heuristic1(next_state, distances)
                    heappush(frontier, (f, next(counter), next_state))

        solving_time = time.time() - start_time
        return None, n_explored_nodes, solving_time

    import time

    @staticmethod
    def iddfs(initial_state: GameState, max_depth: int = 100):
        start_time = time.time()
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
                    solving_time = time.time() - start_time
                    return current_state.get_path(), n_explored_nodes, solving_time

                if depth < depth_limit:
                    for action, action_cost in reversed(current_state.get_possible_actions()):
                        next_state = current_state.apply_action(action, action_cost)
                        stack.append((next_state, depth + 1))

        solving_time = time.time() - start_time
        return None, n_explored_nodes, solving_time

    # Very difficult to solve Sokuban Problem
    # @staticmethod
    # def bi_directional(initial_state: GameState):
    #    pass

    @staticmethod
    def beam(initial_state: GameState):
        start_time = time.time()

        beam_width = 100
        distances = initial_state.get_mahattan_distances_from_goal_to_all_nodes()

        counter = count()
        frontier = [(Heuristics.heuristic1(initial_state, distances), next(counter), initial_state)]
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
                    solving_time = time.time() - start_time
                    return current_state.get_path(), n_explored_nodes, solving_time

                for action, action_cost in current_state.get_possible_actions():
                    next_state = current_state.apply_action(action, action_cost)
                    if next_state in visited:
                        continue
                    next_frontier.append((
                        Heuristics.heuristic1(next_state, distances),
                        next(counter),
                        next_state
                    ))

            frontier = sorted(next_frontier)[:beam_width]

        solving_time = time.time() - start_time
        return None, n_explored_nodes, solving_time

    @staticmethod
    def ida_star(initial_state: GameState):
        start_time = time.time()

        distances = initial_state.get_mahattan_distances_from_goal_to_all_nodes()

        threshold = Heuristics.heuristic1(initial_state, distances)
        n_explored_nodes = 0

        while True:
            stack = [(initial_state, 0)]  # (state, g)
            visited = set()
            next_threshold = float('inf')

            while stack:
                current_state, g = stack.pop()
                f = g + Heuristics.heuristic1(current_state, distances)

                if f > threshold:
                    next_threshold = min(next_threshold, f)
                    continue

                if current_state in visited:
                    continue
                visited.add(current_state)
                n_explored_nodes += 1

                if current_state.is_win():
                    solving_time = time.time() - start_time
                    return current_state.get_path(), n_explored_nodes, solving_time

                for action, action_cost in reversed(current_state.get_possible_actions()):
                    next_state = current_state.apply_action(action, action_cost)
                    if next_state in visited:
                        continue
                    stack.append((next_state, g + action_cost))

            if next_threshold == float('inf'):
                solving_time = time.time() - start_time
                return None, n_explored_nodes, solving_time

            threshold = next_threshold

    @staticmethod
    def enforced_hill_climbing(initial_state: GameState):
        start_time = time.time()

        distances = initial_state.get_mahattan_distances_from_goal_to_all_nodes()

        def bfs_find_better_state(start_state, current_h):
            nonlocal n_explored_nodes
            visited = set()
            queue = deque()
            queue.append(start_state)
            visited.add(start_state)

            while queue:
                state = queue.popleft()
                n_explored_nodes += 1

                for action, action_cost in state.get_possible_actions():
                    next_state = state.apply_action(action, action_cost)
                    if next_state in visited:
                        continue

                    h = Heuristics.heuristic1(next_state, distances)
                    if h < current_h:
                        return next_state
                    queue.append(next_state)
                    visited.add(next_state)

            return None

        current_state = initial_state
        n_explored_nodes = 0

        while True:
            current_h = Heuristics.heuristic1(current_state, distances)
            n_explored_nodes += 1

            if current_state.is_win():
                solving_time = time.time() - start_time
                return current_state.get_path(), n_explored_nodes, solving_time

            neighbors = []
            for action, action_cost in current_state.get_possible_actions():
                next_state = current_state.apply_action(action, action_cost)
                neighbors.append((Heuristics.heuristic1(next_state, distances), next_state))

            better_neighbors = [s for h, s in neighbors if h < current_h]

            if better_neighbors:
                current_state = min(better_neighbors, key=lambda s: Heuristics.heuristic1(s, distances))
            else:
                next_state = bfs_find_better_state(current_state, current_h)
                if next_state is None:
                    solving_time = time.time() - start_time
                    return None, n_explored_nodes, solving_time
                current_state = next_state