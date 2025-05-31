import copy

class GameState:
    def __init__(self, player_pos, box_positions, wall_positions, goal_positions,
                 map_dims, parent=None, action=None, cost=0, depth=0):
        self.player_pos = tuple(player_pos)
        # Use frozenset for box_positions to make the state hashable and order-independent
        self.box_positions = frozenset(map(tuple, box_positions))
        self.wall_positions = wall_positions # Should be a set for efficient lookup
        self.goal_positions = goal_positions # Should be a set
        self.map_dims = map_dims # (rows, cols)

        self.parent = parent
        self.action = action # The action that led to this state
        self.cost = cost     # Cost from initial state to this state (g-value)
        self.depth = depth   # Depth of this node in the search tree

    def is_wall(self, pos):
        return pos in self.wall_positions

    def is_box(self, pos):
        return pos in self.box_positions

    def is_goal(self, pos):
        return pos in self.goal_positions

    def is_win(self):
        if not self.box_positions: # No boxes means no win (or trivial map)
            return False
        return all(box_pos in self.goal_positions for box_pos in self.box_positions)

    def get_possible_actions(self):
        actions = []
        # (dr, dc, action_name)
        # dr = delta_row, dc = delta_col
        possible_moves = {
            'UP': (-1, 0), 'DOWN': (1, 0),
            'LEFT': (0, -1), 'RIGHT': (0, 1)
        }

        for action_name, (dr, dc) in possible_moves.items():
            new_player_pos = (self.player_pos[0] + dr, self.player_pos[1] + dc)

            if self.is_wall(new_player_pos):
                continue

            if self.is_box(new_player_pos):
                # Attempting to push a box
                new_box_pos = (new_player_pos[0] + dr, new_player_pos[1] + dc)
                if self.is_wall(new_box_pos) or self.is_box(new_box_pos):
                    # Box push blocked by wall or another box
                    continue
            actions.append(action_name)
        return actions

    def apply_action(self, action):
        dr, dc = 0, 0
        if action == 'UP': dr = -1
        elif action == 'DOWN': dr = 1
        elif action == 'LEFT': dc = -1
        elif action == 'RIGHT': dc = 1

        new_player_pos = (self.player_pos[0] + dr, self.player_pos[1] + dc)
        new_box_positions = set(self.box_positions) # Make it mutable for this operation

        if self.is_box(new_player_pos):
            # Player is pushing a box
            pushed_box_old_pos = new_player_pos
            new_box_pos_for_pushed = (pushed_box_old_pos[0] + dr, pushed_box_old_pos[1] + dc)

            new_box_positions.remove(pushed_box_old_pos)
            new_box_positions.add(new_box_pos_for_pushed)

        # Create new state
        return GameState(
            player_pos=new_player_pos,
            box_positions=frozenset(new_box_positions), # Convert back to frozenset
            wall_positions=self.wall_positions,
            goal_positions=self.goal_positions,
            map_dims=self.map_dims,
            parent=self,
            action=action,
            cost=self.cost + 1, # Assuming cost of 1 per action
            depth=self.depth + 1
        )

    def is_deadlock(self):
        # Basic deadlock: a box is in a corner and not on a goal
        for box_pos in self.box_positions:
            if box_pos in self.goal_positions:
                continue # Box is on a goal, not a deadlock

            r, c = box_pos
            # Check corners (X is box, # is wall)
            # #X
            # ##
            is_corner_up_left = (self.is_wall((r-1, c)) and self.is_wall((r, c-1)))
            # X#
            # ##
            is_corner_up_right = (self.is_wall((r-1, c)) and self.is_wall((r, c+1)))
            # ##
            # #X
            is_corner_down_left = (self.is_wall((r+1, c)) and self.is_wall((r, c-1)))
            # ##
            # X#
            is_corner_down_right = (self.is_wall((r+1, c)) and self.is_wall((r, c+1)))
            
            if is_corner_up_left or is_corner_up_right or is_corner_down_left or is_corner_down_right:
                return True # Box in a non-goal corner is a deadlock
            
            # More advanced: Box against a wall with no goals along that wall segment
            # This is more complex to implement correctly. For now, stick to corners.

        return False


    def __hash__(self):
        # Hash based on player position and frozenset of box positions
        return hash((self.player_pos, self.box_positions))

    def __eq__(self, other):
        if not isinstance(other, GameState):
            return NotImplemented
        return self.player_pos == other.player_pos and \
               self.box_positions == other.box_positions

    def __lt__(self, other): # For priority queue (UCS, A*)
        # Default comparison for A* should be f_score, for UCS it's cost.
        # The priority queue will store tuples like (priority_value, state),
        # so this method might not be directly used by heapq if you store tuples.
        # If storing states directly, it would be:
        # return self.cost < other.cost # For UCS
        # Or for A*: return (self.cost + heuristic(self)) < (other.cost + heuristic(other))
        # It's safer to manage priority explicitly when adding to heapq.
        return self.cost < other.cost # Placeholder

    def get_path(self):
        """Reconstructs the path of actions from the initial state to this state."""
        path = []
        current = self
        while current.parent is not None:
            path.append(current.action)
            current = current.parent
        return path[::-1] # Reverse to get actions from start