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
            for c in range(game_state.map_dims[1]):
                x, y = c * TILE_SIZE, r * TILE_SIZE
                rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, (50, 50, 50), rect, 1)  # Draw grid lines

        # Draw walls
        for (r, c) in game_state.wall_positions:
            rect = pygame.Rect(c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, (100, 100, 100), rect)

        # Draw goals
        for (r, c) in game_state.goal_positions:
            rect = pygame.Rect(c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, (0, 255, 0), rect)

        # Draw boxes
        for (r, c) in game_state.box_positions:
            rect = pygame.Rect(c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, (255, 165, 0), rect)

        # Draw player
        if Renderer.player_sprite:
            screen.blit(Renderer.player_sprite, (game_state.player_pos[1] * TILE_SIZE, game_state.player_pos[0] * TILE_SIZE))
