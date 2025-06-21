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

        frontier = []
        heappush(frontier, (heuristic(initial_state), next(counter), initial_state, [], 0))  # (f, id, state, path, g)
        min_cost = {initial_state: 0}
        visited = set()
        n_explored_nodes = 0

        while frontier:
            _, _, current_state, path, g = heappop(frontier)

            if current_state in visited:
                continue
            visited.add(current_state)
            n_explored_nodes += 1

            # Yield thông tin từng bước, bao gồm visited
            yield {
                "current_state": current_state,
                "n_explored": n_explored_nodes,
                "visited": visited.copy(),
                "path_so_far": path.copy()
            }

            if current_state.is_win():
                yield {
                    "solution": path,
                    "done": True
                }
                return

            for action, action_cost in current_state.get_possible_actions():
                next_state = current_state.apply_action(action, action_cost)
                new_cost = g + action_cost

                if new_cost < min_cost.get(next_state, float('inf')):
                    min_cost[next_state] = new_cost
                    f = new_cost + heuristic(next_state)
                    heappush(frontier, (f, next(counter), next_state, path + [(action, action_cost)], new_cost))

        # Không tìm thấy lời giải
        yield {
            "solution": None,
            "done": True
        }

    @staticmethod
    def iddfs_generator(initial_state: GameState, max_depth: int = 50):
        n_explored_nodes = 0

        for depth_limit in range(max_depth):
            stack = [(initial_state, 0, [])]  # (state, depth, path_so_far)
            visited = set()

            while stack:
                current_state, depth, path = stack.pop()

                if current_state in visited:
                    continue
                visited.add(current_state)
                n_explored_nodes += 1

                yield {
                    "current_state": current_state,
                    "n_explored": n_explored_nodes,
                    "visited": visited,
                    "path_so_far": path.copy()
                }

                if current_state.is_win():
                    yield {
                        "solution": path,
                        "done": True
                    }
                    return

                if depth < depth_limit:
                    for action, action_cost in reversed(current_state.get_possible_actions()):
                        next_state = current_state.apply_action(action, action_cost)
                        stack.append((next_state, depth + 1, path + [(action, action_cost)]))

        yield {
            "solution": None,
            "done": True
        }

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
            stack = [(initial_state, 0, [])]  # (state, g, path_so_far)
            visited = set()
            next_threshold = float('inf')

            while stack:
                current_state, g, path = stack.pop()
                f = g + heuristic(current_state)

                if f > threshold:
                    next_threshold = min(next_threshold, f)
                    continue

                if current_state in visited:
                    continue
                visited.add(current_state)
                n_explored_nodes += 1

                # Yield thông tin tại mỗi bước
                yield {
                    "current_state": current_state,
                    "n_explored": n_explored_nodes,
                    "visited": visited.copy(),
                    "path_so_far": path.copy()
                }

                if current_state.is_win():
                    yield {
                        "solution": path,
                        "done": True
                    }
                    return

                for action, action_cost in reversed(current_state.get_possible_actions()):
                    next_state = current_state.apply_action(action, action_cost)
                    if next_state in visited:
                        continue
                    new_path = path + [(action, action_cost)]
                    stack.append((next_state, g + action_cost, new_path))

            if next_threshold == float('inf'):
                yield {
                    "solution": None,
                    "done": True
                }
                return

            threshold = next_threshold

    @staticmethod
    def enforced_hill_climbing_generator(initial_state: GameState):
        from collections import deque

        distances = initial_state.get_mahattan_distances_from_goal_to_all_nodes()

        def heuristic(state: GameState):
            h_value = 0
            for box_position in state.box_positions:
                if box_position not in distances:
                    return float('inf')
                h_value += distances[box_position]
            return h_value

        def bfs_find_better_state(start_state, current_h, visited_global, path):
            nonlocal n_explored_nodes
            visited = set()
            queue = deque()
            queue.append((start_state, []))  # (state, path_extension)
            visited.add(start_state)

            while queue:
                state, ext_path = queue.popleft()
                n_explored_nodes += 1  # ✅ Tăng node đã duyệt

                for action, action_cost in state.get_possible_actions():
                    next_state = state.apply_action(action, action_cost)
                    if next_state in visited:
                        continue
                    h = heuristic(next_state)
                    new_path = ext_path + [(action, action_cost)]

                    if h < current_h:
                        return next_state, new_path

                    queue.append((next_state, new_path))
                    visited.add(next_state)

            return None, None

        current_state = initial_state
        path = []
        visited = set()
        n_explored_nodes = 0

        while True:
            current_h = heuristic(current_state)
            visited.add(current_state)
            n_explored_nodes += 1

            yield {
                "current_state": current_state,
                "n_explored": n_explored_nodes,
                "visited": visited.copy(),
                "path_so_far": path.copy()
            }

            if current_state.is_win():
                yield {
                    "solution": path,
                    "done": True
                }
                return

            neighbors = []
            for action, action_cost in current_state.get_possible_actions():
                next_state = current_state.apply_action(action, action_cost)
                neighbors.append((heuristic(next_state), next_state, (action, action_cost)))

            better_neighbors = [(h, s, a) for h, s, a in neighbors if h < current_h]

            if better_neighbors:
                _, next_state, action = min(better_neighbors, key=lambda x: x[0])
                current_state = next_state
                path.append(action)
            else:
                next_state, path_extension = bfs_find_better_state(current_state, current_h, visited, path)
                if next_state is None:
                    yield {
                        "solution": None,
                        "done": True
                    }
                    return
                current_state = next_state
                path += path_extension