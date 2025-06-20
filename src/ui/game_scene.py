from .renderer import Renderer
from config import *
from src.ui.button import Button
import pygame
from src.game_manager import GameManager
from src.ui.map_input_box import MapInputBox
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

        self.is_paused = False
        self.display_algo_buttons = False  # For Algorithm Button

        self.map_input_box: MapInputBox = None

        self.is_solution_running = False
        self.is_search_visualizing = False

        self.create_GUI()
        GameManager.choose_map(0)

    def create_GUI(self):
        font = pygame.font.Font(None, FONT_SIZE_MEDIUM)
        self.control_buttons = {}

        x = SCREEN_WIDTH - BUTTON_WIDTH - 20
        y = 20
        spacing = 20

        map_button = Button(x, y, BUTTON_WIDTH, BUTTON_HEIGHT, "MAP", font,
                            action=self.map_button_action, hover_color=(200, 200, 200), text_color=(0, 0, 0))
        self.control_buttons["MAP"] = map_button

        algorithm_button = Button(x, map_button.y + map_button.height + spacing, BUTTON_WIDTH, BUTTON_HEIGHT,
                                  "ALGORITHM", font,
                                  action=self.algorithm_button_action, hover_color=(200, 200, 200),
                                  text_color=(0, 0, 0))
        self.control_buttons["ALGORITHM"] = algorithm_button

        solution_button = Button(x, algorithm_button.y + algorithm_button.height + spacing, BUTTON_WIDTH, BUTTON_HEIGHT,
                                 "SOLUTION", font,
                                 action=self.solution_button_action, hover_color=(200, 200, 200), text_color=(0, 0, 0))
        self.control_buttons["SOLUTION"] = solution_button

        visualize_button = Button(
            x, solution_button.y + solution_button.height + spacing,
            BUTTON_WIDTH, BUTTON_HEIGHT,
            "VISUALIZE", font,
            action=self.visualize_button_action,
            hover_color=(200, 200, 200),
            text_color=(0, 0, 0)
        )
        self.control_buttons["VISUALIZE"] = visualize_button

        pause_button = Button(
            x, visualize_button.y + visualize_button.height + spacing,
            BUTTON_WIDTH, BUTTON_HEIGHT,
            "PAUSE", font,
            action=self.pause_button_action,
            hover_color=(200, 200, 200),
            text_color=(0, 0, 0)
        )
        self.control_buttons["PAUSE"] = pause_button

        algo_x = x - spacing - BUTTON_WIDTH
        algo_y = algorithm_button.y

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
        map_y = map_button.y

        self.map_input_box = MapInputBox(map_x, map_y, BUTTON_WIDTH, BUTTON_HEIGHT, font)

        buttons_are_visible(self.algo_buttons, False)

    def update(self):
        GameManager.update_algorithm()

        if self.is_search_visualizing and not self.is_paused and GameManager.search_generator:
            GameManager.visualize_frame_counter += 1
            if GameManager.visualize_frame_counter >= GameManager.visualize_frames_per_action:
                GameManager.visualize_frame_counter = 0
                try:
                    result = next(GameManager.search_generator)

                    if "done" in result and result["done"]:
                        self.is_search_visualizing = False
                        GameManager.status_message = (
                            "No solution found." if result["solution"] is None else "Solution found."
                        )
                        return

                    GameManager.current_state = result["current_state"]
                    GameManager.n_explored_nodes = result["n_explored"]
                    GameManager.solution_rendering_step = len(result["path_so_far"])
                except StopIteration:
                    self.is_search_visualizing = False
                    GameManager.status_message = "Visualization ended."

        elif self.is_solution_running and not self.is_paused and GameManager.actions:
            GameManager.solution_frame_counter += 1
            if GameManager.solution_frame_counter >= GameManager.solution_frames_per_action:
                GameManager.solution_frame_counter = 0
                try:
                    GameManager.current_action = next(GameManager.actions)
                    action, action_cost = GameManager.current_action
                    GameManager.current_state = GameManager.current_state.apply_action(action, action_cost)
                    GameManager.solution_rendering_step += 1
                except StopIteration:
                    GameManager.actions = None
                    GameManager.current_action = None

        self.control_buttons["MAP"].set_text("MAP " + str(GameManager.selected_map_idx + 1))
        self.control_buttons["PAUSE"].set_text("CONTINUE" if self.is_paused else "PAUSE")

    def render(self, screen):
        self.screen.fill(WHITE)
        for button in self.control_buttons.values():
            button.render(screen)
        for button in self.algo_buttons.values():
            button.render(screen)

        self.map_input_box.render(screen)
        Renderer.render_game_state(self.screen)

        label_x = 20
        value_x = 220
        spacing = 40
        y = SCREEN_HEIGHT - spacing * 4 - 20

        Renderer.render_text(screen, "Step:", label_x, y)
        Renderer.render_text(screen, str(GameManager.solution_rendering_step), value_x, y)

        Renderer.render_text(screen, "Total Cost:", label_x, y + spacing)
        Renderer.render_text(screen, str(GameManager.current_state.cost), value_x, y + spacing)

        Renderer.render_text(screen, "Explored Nodes:", label_x, y + spacing * 2)
        Renderer.render_text(screen, str(GameManager.n_explored_nodes), value_x, y + spacing * 2)

        Renderer.render_text(screen, "Solving Time:", label_x, y + spacing * 3)
        Renderer.render_text(screen, str(GameManager.solving_time) + " ms", value_x, y + spacing * 3)

        Renderer.render_text(screen, GameManager.status_message, 20, SCREEN_HEIGHT - 20)

        # --- Render possible actions during visualization ---
        if self.is_search_visualizing and GameManager.current_state:
            # "+" shape order: UP, RIGHT, LEFT, DOWN
            actions = ["UP", "RIGHT", "LEFT", "DOWN"]
            possible_actions = set(a for a, _ in GameManager.current_state.get_possible_actions())
            action_font = pygame.font.Font(None, 36)
            action_box_w, action_box_h = 100, 40

            # Dynamically position "+" shape to the right of the map
            cols = GameManager.current_state.map_dims[1]
            map_right = cols * TILE_SIZE
            print(f"Map right edge at: {cols} pixels")
            center_x = map_right + action_box_w + 60  # 60 pixels padding to the right of the map
            center_y = SCREEN_HEIGHT // 2

            positions = {
                "UP":    (center_x, center_y - action_box_h - 10),
                "DOWN":  (center_x, center_y + action_box_h + 10),
                "LEFT":  (center_x - action_box_w - 10, center_y),
                "RIGHT": (center_x + action_box_w + 10, center_y),
            }

            for action in actions:
                pos_x, pos_y = positions[action]
                rect = pygame.Rect(
                    pos_x - action_box_w // 2,
                    pos_y - action_box_h // 2,
                    action_box_w,
                    action_box_h
                )
                border_color = (0, 200, 0) if action in possible_actions else (180, 180, 180)
                pygame.draw.rect(screen, (255, 255, 255), rect)
                pygame.draw.rect(screen, border_color, rect, 3)
                text_surface = action_font.render(action, True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=rect.center)
                screen.blit(text_surface, text_rect)

    def solution_button_action(self):
        self.is_solution_running = True
        self.is_search_visualizing = False

        self.display_algo_buttons = False
        buttons_are_visible(self.algo_buttons, self.display_algo_buttons)
        self.map_input_box.turn_off()
        self.is_paused = False

        algo_name = self.control_buttons["ALGORITHM"].get_text()
        algo_name = self.control_buttons["ALGORITHM"].get_text()
        if algo_name not in GameManager.algorithms:
            GameManager.status_message = f"ERROR: Algorithm '{algo_name}' is not available."
            return

        GameManager.start_algorithm(algo_name)

    def visualize_button_action(self):
        self.is_solution_running = False
        self.is_search_visualizing = True

        self.display_algo_buttons = False
        buttons_are_visible(self.algo_buttons, self.display_algo_buttons)
        self.map_input_box.turn_off()
        self.is_paused = False

        algo_name = self.control_buttons["ALGORITHM"].get_text()
        if algo_name not in GameManager.algorithm_generators:
            GameManager.status_message = f"Algorithm '{algo_name}' does not support visualization."
            self.is_search_visualizing = False
            return

        GameManager.start_visualization(algo_name)

    def pause_button_action(self):
        self.display_algo_buttons = False
        buttons_are_visible(self.algo_buttons, self.display_algo_buttons)
        self.map_input_box.turn_off()
        self.is_paused = not self.is_paused

    def algorithm_button_action(self):
        self.map_input_box.turn_off()
        self.display_algo_buttons = not self.display_algo_buttons
        buttons_are_visible(self.algo_buttons, self.display_algo_buttons)

    def map_button_action(self):
        self.display_algo_buttons = False
        buttons_are_visible(self.algo_buttons, self.display_algo_buttons)
        self.map_input_box.is_visible = not self.map_input_box.is_visible
        self.map_input_box.is_active = not self.map_input_box.is_active

    def select_algorithm(self, name: str):
        self.control_buttons["ALGORITHM"].set_text(name)
        self.display_algo_buttons = False
        buttons_are_visible(self.algo_buttons, False)
