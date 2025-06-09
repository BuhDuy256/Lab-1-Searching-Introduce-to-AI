from src.game_state import GameState

def dfs(state: GameState):
    def solve_dfs(curr_state: GameState, visited=None):
        if visited is None:
            visited = set()

        if curr_state in visited:
            return None

        if curr_state.is_deadlock():
            return None

        if curr_state.is_win():
            return curr_state.get_path()

        visited.add(curr_state)

        for action in curr_state.get_possible_actions():
            next_state = curr_state.apply_action(action)
            result = solve_dfs(next_state, visited)
            if result is not None:
                return result

        return None

    return solve_dfs(state)