from config import TEXT_COLOR
from src.game_manager import GameManager
import pygame
from config import TILE_SIZE
import os

# render các game object dựa vào game state
class Renderer:
    player_sprite = None  # Will load after pygame is initialized

    @staticmethod
    def load_assets():
        Renderer.player_sprite = pygame.image.load(
            os.path.join("assets", "images", "player.png")
        ).convert_alpha()
        Renderer.player_sprite = pygame.transform.scale(Renderer.player_sprite, (TILE_SIZE, TILE_SIZE))

    @staticmethod
    def render_board(screen, game_state, offset_x=0, offset_y=0):
        pass

    @staticmethod
    def render_text(screen, text, position, font, color=TEXT_COLOR, center=False):
        pass

    @staticmethod
    def render_game_state(screen):
        game_state = GameManager.current_state
        if game_state is None:
            return

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
                            rect = pygame.Rect(floor_c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                            pygame.draw.rect(screen, (200, 200, 200), rect)
                else:
                    c += 1


        # Draw walls
        for (r, c) in game_state.wall_positions:
            rect = pygame.Rect(c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, (139, 69, 19), rect)

        # Draw goals
        for (r, c) in game_state.goal_positions:
            rect = pygame.Rect(c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, (0, 255, 0), rect)

        # Draw boxes
        for (r, c) in game_state.box_positions:
            rect = pygame.Rect(c * TILE_SIZE + 5, r * TILE_SIZE + 5, TILE_SIZE - 10, TILE_SIZE - 10)
            pygame.draw.rect(screen, (255, 165, 0), rect)

        # Draw player
        if Renderer.player_sprite:
            screen.blit(Renderer.player_sprite, (game_state.player_pos[1] * TILE_SIZE, game_state.player_pos[0] * TILE_SIZE))
