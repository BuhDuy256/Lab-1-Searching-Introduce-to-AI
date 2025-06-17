from config import TEXT_COLOR, TILE_SIZE, STATE_RENDERING_AREA_WIDTH, STATE_RENDERING_AREA_HEIGHT
from src.game_manager import GameManager
import pygame
import os

# render các game object dựa vào game state
class Renderer:
    player_sprite = None
    box_sprite = None
    wall_sprite = None
    floor_sprite = None
    goal_sprite = None
    button_sprite = None
    font = None

    @staticmethod
    def load_assets():
        Renderer.player_sprite = pygame.image.load(
            os.path.join("assets", "images", "player.png")
        ).convert_alpha()
        Renderer.box_sprite = pygame.image.load(
            os.path.join("assets", "images", "box.png")
        ).convert_alpha()
        Renderer.wall_sprite = pygame.image.load(
            os.path.join("assets", "images", "wall.png")
        ).convert_alpha()
        Renderer.floor_sprite = pygame.image.load(
            os.path.join("assets", "images", "floor.png")
        ).convert_alpha()
        Renderer.goal_sprite = pygame.image.load(
            os.path.join("assets", "images", "goal.png")
        ).convert_alpha()
        Renderer.font = pygame.font.Font(None, 30)

    @staticmethod
    def render_board(screen, game_state, offset_x=0, offset_y=0):
        pass

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

        height_exceeded = tile_size * rows > STATE_RENDERING_AREA_HEIGHT
        width_exceeded = tile_size * cols > STATE_RENDERING_AREA_WIDTH

        if height_exceeded and width_exceeded:
            if rows >= cols:
                tile_size = int(STATE_RENDERING_AREA_HEIGHT / rows)
            else:
                tile_size = int(STATE_RENDERING_AREA_WIDTH / cols)
        elif height_exceeded:
            tile_size = int(STATE_RENDERING_AREA_HEIGHT / rows)
        elif width_exceeded:
            tile_size = int(STATE_RENDERING_AREA_WIDTH / cols)

        Renderer.player_sprite = pygame.transform.scale(
            Renderer.player_sprite, (tile_size, tile_size)
        )

        for r in range(game_state.map_dims[0]):
            c = 0
            while c < game_state.map_dims[1]:
                # Find the start of a floor (must be after a wall)
                if not game_state.is_wall((r, c)) and (c == 0 or game_state.is_wall((r, c - 1))):
                    start = c
                    # Scan forward until the floor ends
                    while c < game_state.map_dims[1] and not game_state.is_wall((r, c)):
                        c += 1
                    end = c
                    # Optional: only draw if the floor is bounded on both sides
                    if start > 0 and end < game_state.map_dims[1] and game_state.is_wall((r, end)):
                        for floor_c in range(start, end):
                            screen.blit(
                                Renderer.floor_sprite,
                                (floor_c * tile_size, r * tile_size)
                            )
                else:
                    c += 1

        # Draw walls
        for (r, c) in game_state.wall_positions:
            screen.blit(
                Renderer.wall_sprite,
                (c * tile_size, r * tile_size)
            )

        # Draw goals
        for (r, c) in game_state.goal_positions:
            screen.blit(
                Renderer.goal_sprite,
                (c * tile_size, r * tile_size)
            )

        # Draw boxes
        for (r, c) in game_state.box_positions:
            screen.blit(
                Renderer.box_sprite,
                (c * tile_size, r * tile_size)
            )

        # Draw player
        if Renderer.player_sprite:
            screen.blit(
                Renderer.player_sprite,
                (game_state.player_pos[1] * tile_size, game_state.player_pos[0] * tile_size)
            )
