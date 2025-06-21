import pygame
from src.game_manager import GameManager

class MapInputBox:
    def __init__(self, x, y, w, h, font, text='', placeholder='Enter map...'):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = pygame.Color('gray')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.text = text
        self.font = font
        self.txt_surface = font.render(text, True, (0, 0, 0))
        self.is_active = True
        self.is_visible = False

        # Placeholder-related
        self.placeholder = placeholder
        self.placeholder_color = pygame.Color('gray70')

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.is_active = self.rect.collidepoint(event.pos)
            self.color = self.color_active if self.is_active else self.color_inactive

        if event.type == pygame.KEYDOWN:
            if self.is_active:
                if event.key == pygame.K_RETURN:
                    result = self.text
                    self.text = ""
                    self.txt_surface = self.font.render(self.text, True, (0, 0, 0))

                    try:
                        chosen_map = int(result)
                        total_maps = GameManager.get_total_maps()

                        if chosen_map < 1:
                            chosen_map = 1
                        elif chosen_map > total_maps:
                            chosen_map = total_maps

                        GameManager.choose_map(chosen_map - 1)
                        GameManager.actions = None
                        GameManager.n_explored_nodes = 0
                        GameManager.solving_time = 0
                        GameManager.solution_rendering_step = 0
                        GameManager.search_generator = None
                        GameManager.solution_frame_counter = 0
                        GameManager.visualize_frame_counter = 0
                    except ValueError:
                        pass  # Ignore invalid (non-numeric) input

                    self.turn_off()

                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.unicode.isdigit():
                    self.text += event.unicode

                self.txt_surface = self.font.render(self.text, True, (0, 0, 0))

        return None

    def turn_off(self):
        self.is_active = False
        self.is_visible = False

    def get_text(self):
        return self.text
