from src.game_object import GameObject

class GameManager:
    game_objects_queue: list[GameObject] = []  # Queue of game objects to be processed