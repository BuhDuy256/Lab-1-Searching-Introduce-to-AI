from src.game import Game
import sys
import os

if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()
    game = Game()
    game.run()