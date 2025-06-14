import pygame
from src.game_manager import GameManager

class MapInputBox:
    def __init__(self, x, y, w, h, font, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = pygame.Color('gray')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.text = text
        self.font = pygame.font.Font(None, 32)
        self.txt_surface = font.render(text, True, self.color)
        self.is_active = True
        self.is_visible = False

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

                    chosen_map = int(result)
                    total_maps = GameManager.get_total_maps()

                    if chosen_map < 1:
                        chosen_map = 1
                    elif chosen_map > total_maps:
                        chosen_map = total_maps

                    GameManager.choose_map(chosen_map - 1)
                    self.turn_off()
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.unicode.isdigit():
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, (0, 0, 0))

        return None

    def render(self, screen):
        if self.is_visible:
            text_rect = self.txt_surface.get_rect(center=self.rect.center)
            screen.blit(self.txt_surface, text_rect)
            pygame.draw.rect(screen, self.color, self.rect, 2)

    def turn_off(self):
        self.is_active = False
        self.is_visible = False

    def get_text(self):
        return self.text
