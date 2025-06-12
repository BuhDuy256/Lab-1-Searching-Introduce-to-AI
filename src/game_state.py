class GameState:
    def __init__(self, player_pos, box_positions, wall_positions, goal_positions,
                 map_dims, parent=None, previous_action=None, cost=0, depth=0):
        self.player_pos = tuple(player_pos)

        self.box_positions = frozenset(map(tuple, box_positions))
        self.wall_positions = wall_positions
        self.goal_positions = goal_positions
        self.map_dims = map_dims # (rows, cols)

        self.parent = parent
        self.previous_action = previous_action # The action that led to this state
        self.cost = cost # Cost from initial state to current state
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
        possible_moves = {
            'UP': (-1, 0), 'DOWN': (1, 0),
            'LEFT': (0, -1), 'RIGHT': (0, 1)
        }

        for action_name, (dr, dc) in possible_moves.items():
            new_player_pos = (self.player_pos[0] + dr, self.player_pos[1] + dc)
            action_cost = 1
            if self.is_wall(new_player_pos):
                continue

            if self.is_box(new_player_pos):
                new_box_pos = (new_player_pos[0] + dr, new_player_pos[1] + dc)
                if self.is_wall(new_box_pos) or self.is_box(new_box_pos):
                    continue
                action_cost += 1
            actions.append((action_name, action_cost))
        return actions

    def apply_action(self, action, action_cost):
        DIRECTIONS = {
            'UP': (-1, 0),
            'DOWN': (1, 0),
            'LEFT': (0, -1),
            'RIGHT': (0, 1)
        }

        dr, dc = DIRECTIONS[action]
        new_player_pos = (self.player_pos[0] + dr, self.player_pos[1] + dc)
        new_box_positions = set(self.box_positions)

        if self.is_box(new_player_pos):
            pushed_box_old_pos = new_player_pos
            new_box_pos = (pushed_box_old_pos[0] + dr, pushed_box_old_pos[1] + dc)

            new_box_positions.remove(pushed_box_old_pos)
            new_box_positions.add(new_box_pos)

        return GameState(
            player_pos=new_player_pos,
            box_positions=frozenset(new_box_positions),
            wall_positions=self.wall_positions,
            goal_positions=self.goal_positions,
            map_dims=self.map_dims,
            parent=self,
            previous_action=action,
            cost=self.cost + action_cost,
            depth=self.depth + 1
        )

    def is_deadlock(self):
        for box_pos in self.box_positions:
            if box_pos in self.goal_positions:
                continue  # not a deadlock if it's already on a goal

            r, c = box_pos

            walls = {
                'up': self.is_wall((r - 1, c)),
                'down': self.is_wall((r + 1, c)),
                'left': self.is_wall((r, c - 1)),
                'right': self.is_wall((r, c + 1)),
            }

            is_corner = (
                    (walls['up'] and walls['left']) or
                    (walls['up'] and walls['right']) or
                    (walls['down'] and walls['left']) or
                    (walls['down'] and walls['right'])
            )

            if is_corner:
                return True

        return False

    def __hash__(self):
        return hash((self.player_pos, self.box_positions))

    def __eq__(self, other):
        if not isinstance(other, GameState):
            return NotImplemented
        return self.player_pos == other.player_pos and \
            self.box_positions == other.box_positions

    def __lt__(self, other): # For priority queue (UCS, A*)
        return self.cost < other.cost

    def get_path(self):
        """Reconstructs the path of actions from the initial state to this state."""
        path = []
        current = self
        while current.parent is not None:
            path.append(current.action)
            current = current.parent
        return path[::-1] # Reverse to get actions from start