# code nguyên bản của AI chưa chỉnh sửa

from .game_state import GameState
from config import PLAYER_CHAR, PLAYER_ON_GOAL_CHAR, BOX_CHAR, BOX_ON_GOAL_CHAR, \
                   WALL_CHAR, GOAL_CHAR, FLOOR_CHAR

def load_map(filepath):
    player_pos = None
    box_positions = set()
    wall_positions = set()
    goal_positions = set()
    
    max_cols = 0
    try:
        with open(filepath, 'r') as f:
            for r, line in enumerate(f):
                line = line.rstrip('\n') # Remove newline character
                max_cols = max(max_cols, len(line))
                for c, char in enumerate(line):
                    pos = (r, c)
                    if char == WALL_CHAR:
                        wall_positions.add(pos)
                    elif char == PLAYER_CHAR:
                        player_pos = pos
                    elif char == BOX_CHAR:
                        box_positions.add(pos)
                    elif char == GOAL_CHAR:
                        goal_positions.add(pos)
                    elif char == PLAYER_ON_GOAL_CHAR:
                        player_pos = pos
                        goal_positions.add(pos)
                    elif char == BOX_ON_GOAL_CHAR:
                        box_positions.add(pos)
                        goal_positions.add(pos)
                    # FLOOR_CHAR is implicit
    except FileNotFoundError:
        print(f"Error: Map file not found at {filepath}")
        return None
    
    if player_pos is None:
        print(f"Error: Player not found in map {filepath}")
        return None

    map_dims = (r + 1, max_cols) # r will be the last row index

    return GameState(player_pos, list(box_positions), wall_positions, goal_positions, map_dims)