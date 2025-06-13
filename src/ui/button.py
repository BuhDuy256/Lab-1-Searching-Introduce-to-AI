from config import GRAY, TEXT_COLOR, BLACK
import pygame

class Button:
    def __init__(self, x, y, width, height, text, font, color=GRAY, hover_color=None, text_color=TEXT_COLOR, action=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color if hover_color else color
        self.text_color = text_color
        self.action = action
        self.is_hovered = False

        self.is_active = True
        self.is_visible = True
        
        self.sprite = None

    def set_text(self, text):
        self.text = text

    def get_text(self):
        return self.text

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered and self.is_active: # Left click
                if self.action:
                    self.action() # Execute the button's action
                return True # Indicates button was clicked
        return False
    
    def update(self):
        pass

    def render(self, screen):
        if self.is_visible:
            current_color = self.hover_color if self.is_hovered else self.color
            pygame.draw.rect(screen, current_color, self.rect)
            pygame.draw.rect(screen, BLACK, self.rect, 2) # Border

            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)