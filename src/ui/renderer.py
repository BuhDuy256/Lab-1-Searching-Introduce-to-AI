from config import TEXT_COLOR, TILE_SIZE, STATE_RENDERING_AREA_WIDTH, STATE_RENDERING_AREA_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, BLACK
from src.game_manager import GameManager
import pygame
import os

# Render các game object dựa vào game state
class Renderer:
    # Sprite gốc (không bị scale)
    original_player_sprite = None
    original_box_sprite = None
    original_wall_sprite = None
    original_floor_sprite = None
    original_goal_sprite = None

    # Sprite đã scale phù hợp
    player_sprite = None
    box_sprite = None
    wall_sprite = None
    floor_sprite = None
    goal_sprite = None
    goal_pressed_sprite = None
    background_sprite = None 
    button_sprite = None
    button_hovered_sprite = None
    map_input_box_sprite = None
    map_input_box_active_sprite = None

    font = None

    @staticmethod
    def load_assets():
        # Load sprite gốc
        Renderer.original_player_sprite = pygame.image.load(
            os.path.join("assets", "images", "player.png")
        ).convert_alpha()
        Renderer.original_box_sprite = pygame.image.load(
            os.path.join("assets", "images", "box.png")
        ).convert_alpha()
        Renderer.original_wall_sprite = pygame.image.load(
            os.path.join("assets", "images", "wall.png")
        ).convert_alpha()
        Renderer.original_floor_sprite = pygame.image.load(
            os.path.join("assets", "images", "floor2.png")
        ).convert_alpha()
        Renderer.original_goal_sprite = pygame.image.load(
            os.path.join("assets", "images", "goal.png")
        ).convert_alpha()
        Renderer.goal_pressed_sprite = pygame.image.load(
            os.path.join("assets", "images", "goal_pressed.png")
        ).convert_alpha()
        # Load and scale background
        background_img = pygame.image.load(
            os.path.join("assets", "images", "background.png")
        ).convert()
        Renderer.background_sprite = pygame.transform.scale(
            background_img, (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        Renderer.button_sprite = pygame.image.load(
            os.path.join("assets", "images", "button.png")
        ).convert_alpha()
        Renderer.button_hovered_sprite = pygame.image.load(
            os.path.join("assets", "images", "button_hovered.png")
        ).convert_alpha()
        Renderer.map_input_box_sprite = pygame.image.load(
            os.path.join("assets", "images", "map_input_box.png")
        ).convert_alpha()
        Renderer.map_input_box_active_sprite = pygame.image.load(
            os.path.join("assets", "images", "map_input_box_active.png")
        ).convert_alpha()
        Renderer.font = pygame.font.Font(None, 30)

    @staticmethod
    def render_text(screen, text, x, y, center=False):
        # Render text with a white border
        font = Renderer.font
        # Render border by drawing text in white at offsets
        border_color = (255, 255, 255)
        text_color = TEXT_COLOR
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect()

        if center:
            text_rect.center = (x, y)
        else:
            text_rect.topleft = (x, y)

        # Draw border by rendering text in white at 1px offsets
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                border_surface = font.render(text, True, border_color)
                border_rect = border_surface.get_rect()
                if center:
                    border_rect.center = (x + dx, y + dy)
                else:
                    border_rect.topleft = (x + dx, y + dy)
                screen.blit(border_surface, border_rect)

        # Draw main text
        screen.blit(text_surface, text_rect)

    @staticmethod
    def render_game_state(screen):
        game_state = GameManager.current_state
        if game_state is None:
            return

        # Draw scaled background
        if Renderer.background_sprite:
            screen.blit(Renderer.background_sprite, (0, 0))

        tile_size = TILE_SIZE
        rows, cols = game_state.map_dims

        # Tính tile_size phù hợp với khu vực hiển thị
        if tile_size * rows > STATE_RENDERING_AREA_HEIGHT or tile_size * cols > STATE_RENDERING_AREA_WIDTH:
            tile_size = min(
                STATE_RENDERING_AREA_HEIGHT // rows,
                STATE_RENDERING_AREA_WIDTH // cols
            )

        # Scale sprite theo tile_size
        Renderer.player_sprite = pygame.transform.scale(Renderer.original_player_sprite, (tile_size, tile_size))
        Renderer.box_sprite = pygame.transform.scale(Renderer.original_box_sprite, (tile_size, tile_size))
        Renderer.wall_sprite = pygame.transform.scale(Renderer.original_wall_sprite, (tile_size, tile_size))
        Renderer.floor_sprite = pygame.transform.scale(Renderer.original_floor_sprite, (tile_size, tile_size))
        Renderer.goal_sprite = pygame.transform.scale(Renderer.original_goal_sprite, (tile_size, tile_size))
        Renderer.goal_pressed_sprite = pygame.transform.scale(Renderer.goal_pressed_sprite, (tile_size, tile_size))

        # Vẽ sàn theo từng đoạn (có tường bao quanh)
        for r in range(rows):
            c = 0
            while c < cols:
                if not game_state.is_wall((r, c)) and (c == 0 or game_state.is_wall((r, c - 1))):
                    start = c
                    while c < cols and not game_state.is_wall((r, c)):
                        c += 1
                    end = c
                    if start > 0 and end < cols and game_state.is_wall((r, end)):
                        for floor_c in range(start, end):
                            screen.blit(Renderer.floor_sprite, (floor_c * tile_size, r * tile_size))
                else:
                    c += 1

        # Vẽ các đối tượng
        for (r, c) in game_state.wall_positions:
            screen.blit(Renderer.wall_sprite, (c * tile_size, r * tile_size))

        # Draw goals: pressed if box on goal, else normal
        for (r, c) in game_state.goal_positions:
            if (r, c) in game_state.box_positions:
                screen.blit(Renderer.goal_pressed_sprite, (c * tile_size, r * tile_size))
            else:
                screen.blit(Renderer.goal_sprite, (c * tile_size, r * tile_size))

        for (r, c) in game_state.box_positions:
            screen.blit(Renderer.box_sprite, (c * tile_size, r * tile_size))

        pr, pc = game_state.player_pos
        screen.blit(Renderer.player_sprite, (pc * tile_size, pr * tile_size))

    @staticmethod
    def render_button(screen, button):
        if button.is_visible:
            x_offset, y_offset = 0, 3
            # Choose sprite based on hovered state
            if getattr(button, "is_hovered", False):
                sprite = Renderer.button_hovered_sprite
            else:
                sprite = Renderer.button_sprite
                x_offset, y_offset = 0, -3

            # Draw the button sprite, scaled to button.rect size
            if sprite:
                scaled_sprite = pygame.transform.scale(sprite, (button.rect.width, button.rect.height))
                screen.blit(scaled_sprite, button.rect.topleft)
            else:
                # Fallback: draw colored rect if sprite not loaded
                current_color = button.hover_color if button.is_hovered else button.color
                pygame.draw.rect(screen, current_color, button.rect)
                pygame.draw.rect(screen, BLACK, button.rect, 2) # Border

            # Draw button text centered
            text_surface = button.font.render(button.text, True, button.text_color)
            text_rect = text_surface.get_rect(center=(
                button.rect.centerx + x_offset,
                button.rect.centery + y_offset
            ))
            screen.blit(text_surface, text_rect)
            
    @staticmethod
    def render_map_input_box(screen, input_box):
        if input_box.is_visible:
            # Choose sprite based on active state
            if getattr(input_box, "is_active", False):
                sprite = Renderer.map_input_box_active_sprite
                x_offset, y_offset = 0, 3
            else:
                sprite = Renderer.map_input_box_sprite
                x_offset, y_offset = 0, -3

            # Draw the input box sprite, scaled to input_box.rect size
            if sprite:
                scaled_sprite = pygame.transform.scale(sprite, (input_box.rect.width, input_box.rect.height))
                screen.blit(scaled_sprite, input_box.rect.topleft)
            else:
                # Fallback: draw colored rect if sprite not loaded
                pygame.draw.rect(screen, input_box.color, input_box.rect, 2)

            # Draw the text or placeholder centered with offset
            if input_box.text:
                text_surface = input_box.font.render(input_box.text, True, (0, 0, 0))
            else:
                text_surface = input_box.font.render(input_box.placeholder, True, input_box.placeholder_color)

            text_rect = text_surface.get_rect(center=(
                input_box.rect.centerx + x_offset,
                input_box.rect.centery + y_offset
            ))
            screen.blit(text_surface, text_rect)