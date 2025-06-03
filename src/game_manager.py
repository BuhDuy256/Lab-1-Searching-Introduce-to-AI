class GameObject:
    pass

class GameManager:
    game_objects_queue: list[GameObject] = []  # Queue of game objects to be processed

    @classmethod
    def add_game_object(self, game_object: GameObject):
        self.game_objects_queue.append(game_object)