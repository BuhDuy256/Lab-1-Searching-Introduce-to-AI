from .renderer import Renderer
from config import *
from src.ui.button import Button
import pygame
from  src.game_manager import GameManager

class GameScene:
    def __init__(self, screen):
        self.screen = screen

        self.buttons: dict[str, Button] = {}

        self.create_buttons()

        GameManager.choose_map(0)

    def create_buttons(self):
        font = pygame.font.Font(None, 36)
        self.buttons = {}

        x = SCREEN_WIDTH - BUTTON_WIDTH - 20
        y = 20
        spacing = 20

        start_button = Button(x, y, BUTTON_WIDTH, BUTTON_HEIGHT, "START", font,
                              action=self.test_action, hover_color=(200, 200, 200), text_color=(0, 0, 0))
        self.buttons["START"] = start_button

        pause_button = Button(x, start_button.y + start_button.height + spacing, BUTTON_WIDTH, BUTTON_HEIGHT, "PAUSE",
                              font,
                              action=self.test_action, hover_color=(200, 200, 200), text_color=(0, 0, 0))
        self.buttons["PAUSE"] = pause_button

        reset_button = Button(x, pause_button.y + pause_button.height + spacing, BUTTON_WIDTH, BUTTON_HEIGHT, "RESET",
                              font,
                              action=self.test_action, hover_color=(200, 200, 200), text_color=(0, 0, 0))
        self.buttons["RESET"] = reset_button

        algorithm_button = Button(x, reset_button.y + reset_button.height + spacing, BUTTON_WIDTH, BUTTON_HEIGHT,
                                  "ALGORITHM", font,
                                  action=self.test_action, hover_color=(200, 200, 200), text_color=(0, 0, 0))
        self.buttons["ALGORITHM"] = algorithm_button

        map_button = Button(x, algorithm_button.y + algorithm_button.height + spacing, BUTTON_WIDTH, BUTTON_HEIGHT,
                            "MAP", font,
                            action=self.test_action, hover_color=(200, 200, 200), text_color=(0, 0, 0))
        self.buttons["MAP"] = map_button

        algo_x = x - spacing - BUTTON_WIDTH
        algo_y = y

        dfs_button = Button(algo_x, algo_y, BUTTON_WIDTH, BUTTON_HEIGHT, "DFS", font,
                            action=self.test_action, hover_color=(200, 200, 200), text_color=(0, 0, 0))
        self.buttons["DFS"] = dfs_button

        bfs_button = Button(algo_x, dfs_button.y + dfs_button.height + spacing, BUTTON_WIDTH, BUTTON_HEIGHT, "BFS",
                            font,
                            action=self.test_action, hover_color=(200, 200, 200), text_color=(0, 0, 0))
        self.buttons["BFS"] = bfs_button

        ucs_button = Button(algo_x, bfs_button.y + bfs_button.height + spacing, BUTTON_WIDTH, BUTTON_HEIGHT, "UCS",
                            font,
                            action=self.test_action, hover_color=(200, 200, 200), text_color=(0, 0, 0))
        self.buttons["UCS"] = ucs_button

        a_star_button = Button(algo_x, ucs_button.y + ucs_button.height + spacing, BUTTON_WIDTH, BUTTON_HEIGHT, "A*",
                               font,
                               action=self.test_action, hover_color=(200, 200, 200), text_color=(0, 0, 0))
        self.buttons["A*"] = a_star_button

        iddfs_button = Button(algo_x, a_star_button.y + a_star_button.height + spacing, BUTTON_WIDTH, BUTTON_HEIGHT,
                              "IDDFS", font,
                              action=self.test_action, hover_color=(200, 200, 200), text_color=(0, 0, 0))
        self.buttons["IDDFS"] = iddfs_button

        bi_directional_button = Button(algo_x, iddfs_button.y + iddfs_button.height + spacing, BUTTON_WIDTH,
                                       BUTTON_HEIGHT, "BIDIR", font,
                                       action=self.test_action, hover_color=(200, 200, 200), text_color=(0, 0, 0))
        self.buttons["BIDIR"] = bi_directional_button

        ida_star_button = Button(algo_x, bi_directional_button.y + bi_directional_button.height + spacing, BUTTON_WIDTH,
                                 BUTTON_HEIGHT, "IDA*", font,
                                 action=self.test_action, hover_color=(200, 200, 200), text_color=(0, 0, 0))
        self.buttons["IDA*"] = ida_star_button

    def update(self):
        if GameManager.actions:
            try:
                action = next(GameManager.actions)
                GameManager.current_state = GameManager.current_state.apply_action(action)
            except StopIteration:
                GameManager.actions = None

    def render(self, screen):
        self.screen.fill(WHITE)
        for button in self.buttons.values():
            button.render(screen)

        Renderer.render_game_state(self.screen)

    def test_action(self):
        pass