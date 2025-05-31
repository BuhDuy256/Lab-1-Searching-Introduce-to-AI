import pygame
from config import *
from src.game_object import GameObject
from src.game_manager import GameManager

class Button(GameObject):
    def __init__(self, x, y, width, height, text, font, color=GRAY, hover_color=None, text_color=TEXT_COLOR, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color if hover_color else color
        self.text_color = text_color
        self.action = action # Function to call when clicked
        self.is_hovered = False

        GameManager().game_objects_queue.append(self)  # Add to the game objects queue

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered: # Left click
                if self.action:
                    self.action() # Execute the button's action
                return True # Indicates button was clicked
        return False
    
    def update(self):
        pass

    def render(self, screen):
        current_color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, current_color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2) # Border

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)