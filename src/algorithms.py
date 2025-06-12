from src.game_state import GameState

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

            return None

        return _dfs(initial_state, set())
