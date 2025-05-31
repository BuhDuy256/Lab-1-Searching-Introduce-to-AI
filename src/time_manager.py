from config import FPS

class Time:
    clock = None
    delta_time = 0.0

    @staticmethod
    def init():
        import pygame
        Time.clock = pygame.time.Clock()

    @staticmethod
    def update():
        Time.delta_time = Time.clock.tick(FPS) / 1000.0  # 60 FPS