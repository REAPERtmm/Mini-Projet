from GeoMath import *


class Menu:
    def __init__(self, game, size, key):
        self.game = game
        self.size = size
        self.key = key

    def update(self):
        pass

    def blit(self, screen):
        py.draw.rect(
            screen,
            WHITE,
            (
                0,
                0,
                WIDTH,
                HEIGHT
            )
        )
