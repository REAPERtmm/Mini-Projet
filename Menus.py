from GeoMath import *


class Menu:
    def __init__(self, game, width, height):
        self.game = game
        self.width = width
        self.height = height

    def update(self):
        pass

    def blit(self, screen):
        py.draw.rect(
            screen,
            WHITE,
            (
                WIDTH//2 - self.width//2,
                HEIGHT//2 - self.height//2,
                self.width,
                self.height
            )
        )
