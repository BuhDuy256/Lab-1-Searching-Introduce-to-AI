from .renderer import Renderer
from src.game_object import GameObject
from config import WHITE, TILE_SIZE
from src.ui.button import Button
from src.game_manager import GameManager
import pygame
from src.player import Player  # Assuming Player is defined in src/player.py

class GameScene:
    def __init__(self, screen):
        self.screen = screen
        self.renderer = Renderer(screen)

        self.game_objects: list[GameObject] = []  # List of game objects in the scene
        self.buttons: list[Button] = []
        
        self.player: Player = None

        self.create_buttons()
        self.create_player()

    def create_buttons(self):
        #example button creation
        button = Button(50, 50, 200, 50, "Start Game", pygame.font.Font(None, 36), action=self.test_action, 
                        hover_color=(200, 200, 200), text_color=(0, 0, 0))
        
        self.buttons.append(button)
        self.game_objects.append(button)  # Add button to game objects for rendering
        
    def create_player(self):
        player_sprite = pygame.image.load("assets\images\player.png").convert_alpha()
        self.player = Player(100, 100, sprite = player_sprite)
        self.game_objects.append(self.player)
        
    def update(self):
        for game_object in self.game_objects:
            if game_object.active:
                game_object.update()
                
        self.sync_game_objects_from_game_state()

    def render(self, screen):
        self.screen.fill(WHITE)
        for game_object in self.game_objects:
            if game_object.visible: 
                game_object.render(screen)

    def test_action(self):
        print("Alo alo")
        
    def sync_game_objects_from_game_state(self):
        game_state = GameManager.current_state
        self.player.set_position(game_state.player_pos[0] * TILE_SIZE, game_state.player_pos[1] * TILE_SIZE)