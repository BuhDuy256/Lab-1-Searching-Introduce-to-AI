from .renderer import Renderer
from config import *
from src.ui.button import Button
import pygame
from  src.game_manager import GameManager
from src.ui.input_box import MapInputBox
import subprocess

def buttons_are_visible(buttons: dict[str, Button], mode=True):
    for button in buttons.values():
        button.is_visible = mode
        button.is_active = mode

class GameScene:
    def __init__(self, screen):
        self.screen = screen

        self.control_buttons: dict[str, Button] = {}
        self.algo_buttons: dict[str, Button] = {}

        self.is_solution_playing = False
        self.is_solution_paused = False
        self.display_algo_buttons = False # For Algorithm Button

        self.map_input_box: MapInputBox = None

        self.create_buttons()

        GameManager.choose_map(3)

    def create_buttons(self):
        font = pygame.font.Font(None, 36)
        self.control_buttons = {}

        x = SCREEN_WIDTH - BUTTON_WIDTH - 20
        y = 20
        spacing = 20

        start_button = Button(x, y, BUTTON_WIDTH, BUTTON_HEIGHT, "START", font,
                              action=self.start_button_action, hover_color=(200, 200, 200), text_color=(0, 0, 0))
        self.control_buttons["START"] = start_button

        pause_button = Button(x, start_button.y + start_button.height + spacing, BUTTON_WIDTH, BUTTON_HEIGHT, "PAUSE",
                              font,
                              action=self.pause_button_action, hover_color=(200, 200, 200), text_color=(0, 0, 0))
        self.control_buttons["PAUSE"] = pause_button

        algorithm_button = Button(x, pause_button.y + pause_button.height + spacing, BUTTON_WIDTH, BUTTON_HEIGHT,
                                  "ALGORITHM", font,
                                  action=self.algorithm_button_action, hover_color=(200, 200, 200),
                                  text_color=(0, 0, 0))
        self.control_buttons["ALGORITHM"] = algorithm_button

        map_button = Button(x, algorithm_button.y + algorithm_button.height + spacing, BUTTON_WIDTH, BUTTON_HEIGHT,
                            "MAP" , font,
                            action=self.map_button_action, hover_color=(200, 200, 200), text_color=(0, 0, 0))
        self.control_buttons["MAP"] = map_button

        algo_x = x - spacing - BUTTON_WIDTH
        algo_y = y

        algo_names = list(GameManager.algorithms.keys())
        y_offset = algo_y

        for name in algo_names:
            button = Button(
                algo_x, y_offset,
                BUTTON_WIDTH, BUTTON_HEIGHT,
                name, font,
                action=lambda n=name: self.select_algorithm(n),
                hover_color=(200, 200, 200),
                text_color=(0, 0, 0)
            )
            self.algo_buttons[name] = button
            y_offset += BUTTON_HEIGHT + spacing

        map_x = x - spacing - BUTTON_WIDTH
        map_y = y

        font = pygame.font.Font(None, 32)
        self.map_input_box = MapInputBox(map_x, map_y, BUTTON_WIDTH, BUTTON_HEIGHT, font)

        buttons_are_visible(self.algo_buttons, False)

    def update(self):
        if GameManager.actions and not self.is_solution_paused:
            try:
                action = next(GameManager.actions)
                GameManager.current_state = GameManager.current_state.apply_action(action, 1)
            except StopIteration:
                GameManager.actions = None

        self.control_buttons["MAP"].set_text("MAP " + str(GameManager.selected_map_idx + 1))

    def render(self, screen):
        self.screen.fill(WHITE)
        for button in self.control_buttons.values():
            button.render(screen)
        for button in self.algo_buttons.values():
            button.render(screen)

        self.map_input_box.render(screen)

        Renderer.render_game_state(self.screen)

    def start_button_action(self):
        # Hide Algo Buttons
        self.display_algo_buttons = False
        buttons_are_visible(self.algo_buttons, self.display_algo_buttons)

        # Hide Map Input Box
        self.map_input_box.turn_off()

        algo_name = self.control_buttons["ALGORITHM"].get_text()

        if algo_name not in GameManager.algorithms:
            import subprocess
            subprocess.Popen([
                "cmd.exe", "/k", f"echo ERROR: Algorithm '{algo_name}' is not available. && pause"
            ])
            return

        GameManager.apply_algorithm(algo_name)

    def pause_button_action(self):
        # Hide Algo Buttons
        self.display_algo_buttons = False
        buttons_are_visible(self.algo_buttons, self.display_algo_buttons)
        # Hide Map Input Box
        self.map_input_box.turn_off()

        self.is_solution_paused = not self.is_solution_paused
        new_label = "PAUSE" if not self.is_solution_paused else "CONTINUE"
        self.control_buttons["PAUSE"].set_text(new_label)

    def algorithm_button_action(self):
        # Hide Map Input Box
        self.map_input_box.turn_off()

        self.display_algo_buttons = not self.display_algo_buttons
        buttons_are_visible(self.algo_buttons, self.display_algo_buttons)

    def map_button_action(self):
        # Hide Algo Buttons
        self.display_algo_buttons = False
        buttons_are_visible(self.algo_buttons, self.display_algo_buttons)

        self.map_input_box.is_visible = not self.map_input_box.is_visible
        self.map_input_box.is_active = not self.map_input_box.is_active

    def select_algorithm(self, name: str):
        self.control_buttons["ALGORITHM"].set_text(name)
        self.display_algo_buttons = False
        buttons_are_visible(self.algo_buttons, False)
