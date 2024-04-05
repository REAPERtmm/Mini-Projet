from GeoMath import *


class Menu:
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.x = x
        self.y = y

    def update(self):
        pass

    def blit(self, screen):
        py.draw.rect(
            screen,
            WHITE,
            (
                self.x,
                self.y,
                self.width,
                self.height
            )
        )

class Label:
    def __init__(self, width, height, size, x, y, text, color):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.font = fontsize(size)
        self.image = self.font.render(text, True, color)

    def update(self):
        pass

    def blit(self, screen):
        py.draw.rect(
            screen,
            WHITE,
            (
                self.x,
                self.y,
                self.width,
                self.height
            )
        )
