from src.game_object import GameObject

# background sử dụng hiệu ứng parallax, dùng 3 sprite tương đương với 3 layer của background
class Background(GameObject):
    def __init__(self, x, y, width, height, sprite=None):
        super().__init__(x, y, width, height, sprite)
        self.layer = 0  # Background layer