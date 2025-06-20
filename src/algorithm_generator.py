import time

from src.game_state import GameState
from queue import Queue
from heapq import heappush, heappop
import heapq
from itertools import count
import sys

class AlgorithmGenerator:
    @staticmethod
    def dfs_generator(initial_state: GameState):
        stack = [(initial_state, [])]  # (state, path_so_far)
        visited = set()
        n_explored_nodes = 0

        while stack:
            current_state, path = stack.pop()

            if current_state in visited:
                continue
            visited.add(current_state)
            n_explored_nodes += 1

            # 👇 Yield thông tin hiện tại cho render
            yield {
                "current_state": current_state,
                "n_explored": n_explored_nodes,
                "visited": visited.copy(),
                "path_so_far": path.copy()
            }

            if current_state.is_win():
                yield {"solution": path, "done": True}
                return

            for action, action_cost in reversed(current_state.get_possible_actions()):
                next_state = current_state.apply_action(action, action_cost)
                stack.append((next_state, path + [(action, action_cost)]))

        # Nếu hết mà không có lời giải
        yield {"solution": None, "done": True}

    @staticmethod
    def bfs_generator(initial_state: GameState):
        q = Queue()
        visited = set()
        n_explored_nodes = 0

        q.put((initial_state, []))
        visited.add(initial_state)

        while not q.empty():
            current_state, path = q.get()
            n_explored_nodes += 1

            yield {
                "current_state": current_state,
                "n_explored": n_explored_nodes,
                "visited": visited.copy(),
                "path_so_far": path.copy()
            }

            if current_state.is_win():
                yield {"solution": path, "done": True}
                return

            for action, action_cost in current_state.get_possible_actions():
                next_state = current_state.apply_action(action, action_cost)
                if next_state not in visited:
                    visited.add(next_state)
                    q.put((next_state, path + [(action, action_cost)]))

        yield {"solution": None, "done": True}

    @staticmethod
    def ucs_generator(initial_state: GameState):
        from itertools import count
        counter = count()
        frontier = []
        heappush(frontier, (initial_state.cost, next(counter), initial_state, []))
        visited = set()
        min_cost = {initial_state: initial_state.cost}
        n_explored_nodes = 0

        while frontier:
            cost, _, current_state, path = heappop(frontier)

            if current_state in visited:
                continue
            visited.add(current_state)
            n_explored_nodes += 1

            yield {
                "current_state": current_state,
                "n_explored": n_explored_nodes,
                "visited": visited.copy(),
                "path_so_far": path.copy()
            }

            if current_state.is_win():
                yield {"solution": path, "done": True}
                return

            for action, action_cost in current_state.get_possible_actions():
                next_state = current_state.apply_action(action, action_cost)
                total_cost = next_state.cost

                if next_state not in min_cost or total_cost < min_cost[next_state]:
                    min_cost[next_state] = total_cost
                    heappush(frontier, (total_cost, next(counter), next_state, path + [(action, action_cost)]))

        yield {"solution": None, "done": True}

    @staticmethod
    def a_star_generator(initial_state: GameState):
        distances = initial_state.get_mahattan_distances_from_goal_to_all_nodes()

        def heuristic(state: GameState):
            return sum(distances.get(box, float('inf')) for box in state.box_positions)

        counter = count()
        frontier = []
        heappush(frontier, (heuristic(initial_state) + initial_state.cost, next(counter), initial_state, []))
        visited = set()
        min_cost = {initial_state: initial_state.cost}
        n_explored_nodes = 0

        while frontier:
            _, _, current_state, path = heappop(frontier)

            if current_state in visited:
                continue
            visited.add(current_state)
            n_explored_nodes += 1

            yield {
                "current_state": current_state,
                "n_explored": n_explored_nodes,
                "visited": visited.copy(),
                "path_so_far": path.copy()
            }

            if current_state.is_win():
                yield {"solution": path, "done": True}
                return

            for action, action_cost in current_state.get_possible_actions():
                next_state = current_state.apply_action(action, action_cost)
                total_cost = next_state.cost

                if next_state not in min_cost or total_cost < min_cost[next_state]:
                    min_cost[next_state] = total_cost
                    estimated_cost = total_cost + heuristic(next_state)
                    heappush(frontier, (estimated_cost, next(counter), next_state, path + [(action, action_cost)]))

        yield {"solution": None, "done": True}

    @staticmethod
    def iddfs_generator(initial_state: GameState):
        def dls(current_state, depth, path, visited):
            nonlocal n_explored_nodes

            if current_state in visited or depth < 0:
                return None

            visited.add(current_state)
            n_explored_nodes += 1

            yield {
                "current_state": current_state,
                "n_explored": n_explored_nodes,
                "visited": visited.copy(),
                "path_so_far": path.copy()
            }

            if current_state.is_win():
                yield {"solution": path, "done": True}
                return

            for action, action_cost in current_state.get_possible_actions():
                next_state = current_state.apply_action(action, action_cost)
                yield from dls(next_state, depth - 1, path + [(action, action_cost)], visited)

            visited.remove(current_state)

        max_depth = 50
        n_explored_nodes = 0

        for depth_limit in range(max_depth):
            visited = set()
            result = yield from dls(initial_state, depth_limit, [], visited)
            if result is not None:
                return

        yield {"solution": None, "done": True}

    @staticmethod
    def beam_generator(initial_state: GameState):
        beam_width = 5
        distances = initial_state.get_mahattan_distances_from_goal_to_all_nodes()

        def heuristic(state):
            return sum(distances.get(box, float('inf')) for box in state.box_positions)

        from itertools import count
        counter = count()
        frontier = [(heuristic(initial_state), next(counter), initial_state, [])]
        n_explored_nodes = 0
        visited = set()

        while frontier:
            next_frontier = []

            for _, _, current_state, path in frontier:
                if current_state in visited:
                    continue
                visited.add(current_state)
                n_explored_nodes += 1

                yield {
                    "current_state": current_state,
                    "n_explored": n_explored_nodes,
                    "visited": visited.copy(),
                    "path_so_far": path.copy()
                }

                if current_state.is_win():
                    yield {"solution": path, "done": True}
                    return

                for action, action_cost in current_state.get_possible_actions():
                    next_state = current_state.apply_action(action, action_cost)
                    if next_state in visited:
                        continue
                    next_path = path + [(action, action_cost)]
                    next_frontier.append((heuristic(next_state), next(counter), next_state, next_path))

            frontier = sorted(next_frontier)[:beam_width]

        yield {"solution": None, "done": True}

    @staticmethod
    def ida_star_generator(initial_state: GameState):
        distances = initial_state.get_mahattan_distances_from_goal_to_all_nodes()

        def heuristic(state):
            return sum(distances.get(box, float('inf')) for box in state.box_positions)

        def backtrack(state, g, threshold, path, visited):
            nonlocal n_explored_nodes, next_threshold

            f = g + heuristic(state)
            if f > threshold:
                next_threshold = min(next_threshold, f)
                return None

            visited.add(state)
            n_explored_nodes += 1

            yield {
                "current_state": state,
                "n_explored": n_explored_nodes,
                "visited": visited.copy(),
                "path_so_far": path.copy()
            }

            if state.is_win():
                yield {"solution": path, "done": True}
                return

            for action, action_cost in state.get_possible_actions():
                next_state = state.apply_action(action, action_cost)
                if next_state in visited:
                    continue
                yield from backtrack(next_state, g + action_cost, threshold, path + [(action, action_cost)], visited)

            visited.remove(state)

        threshold = heuristic(initial_state)
        n_explored_nodes = 0

        while True:
            visited = set()
            next_threshold = float('inf')
            result = yield from backtrack(initial_state, 0, threshold, [], visited)
            if result is not None:
                return
            if next_threshold == float('inf'):
                yield {"solution": None, "done": True}
                return
            threshold = next_threshold

    @staticmethod
    def enforced_hill_climbing_generator(initial_state: GameState):
        from collections import deque

        distances = initial_state.get_mahattan_distances_from_goal_to_all_nodes()

        def heuristic(state):
            return sum(distances.get(box, float('inf')) for box in state.box_positions)

        def bfs_find_better_state(start_state, current_h):
            visited = set()
            queue = deque([(start_state, [])])
            visited.add(start_state)

            while queue:
                state, path = queue.popleft()

                for action, action_cost in state.get_possible_actions():
                    next_state = state.apply_action(action, action_cost)
                    if next_state in visited:
                        continue
                    h = heuristic(next_state)
                    if h < current_h:
                        return next_state, path + [(action, action_cost)]
                    visited.add(next_state)
                    queue.append((next_state, path + [(action, action_cost)]))

            return None, []

        current_state = initial_state
        path = []
        n_explored_nodes = 0

        while True:
            current_h = heuristic(current_state)
            n_explored_nodes += 1

            yield {
                "current_state": current_state,
                "n_explored": n_explored_nodes,
                "visited": set(),  # EHC không dùng visited toàn cục
                "path_so_far": path.copy()
            }

            if current_state.is_win():
                yield {"solution": path, "done": True}
                return

            neighbors = []
            for action, action_cost in current_state.get_possible_actions():
                next_state = current_state.apply_action(action, action_cost)
                neighbors.append((heuristic(next_state), action, action_cost, next_state))

            better_neighbors = [(h, a, c, s) for h, a, c, s in neighbors if h < current_h]

            if better_neighbors:
                _, action, action_cost, best_state = min(better_neighbors, key=lambda x: x[0])
                path.append((action, action_cost))
                current_state = best_state
            else:
                next_state, extra_path = bfs_find_better_state(current_state, current_h)
                if next_state is None:
                    yield {"solution": None, "done": True}
                    return
                current_state = next_state
                path.extend(extra_path)
