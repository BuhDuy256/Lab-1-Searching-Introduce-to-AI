from config import TEXT_COLOR, TILE_SIZE, STATE_RENDERING_AREA_WIDTH, STATE_RENDERING_AREA_HEIGHT
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
            os.path.join("assets", "images", "floor.png")
        ).convert_alpha()
        Renderer.original_goal_sprite = pygame.image.load(
            os.path.join("assets", "images", "goal.png")
        ).convert_alpha()

        Renderer.font = pygame.font.Font(None, 30)

    @staticmethod
    def render_text(screen, text, x, y, center=False):
        text_surface = Renderer.font.render(text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect()

        if center:
            text_rect.center = (x, y)
        else:
            text_rect.topleft = (x, y)

        screen.blit(text_surface, text_rect)

    @staticmethod
    def render_game_state(screen):
        game_state = GameManager.current_state
        if game_state is None:
            return

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

        for (r, c) in game_state.goal_positions:
            screen.blit(Renderer.goal_sprite, (c * tile_size, r * tile_size))

        for (r, c) in game_state.box_positions:
            screen.blit(Renderer.box_sprite, (c * tile_size, r * tile_size))

        pr, pc = game_state.player_pos
        screen.blit(Renderer.player_sprite, (pc * tile_size, pr * tile_size))
