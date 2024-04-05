from GeoMath import *


class Menu:
    def __init__(self, game, position: Vector2, size: Vector2, color):
        self.game = game
        self.size = size
        self.position = position
        self.color = color

    def update(self):
        pass

    def blit(self, screen):
        py.draw.rect(
            screen,
            self.color,
            (
                self.position.x(),
                self.position.y(),
                self.size.x(),
                self.size.y()
            )
        )


class Widget:
    def __init__(self, game, position: Vector2, size: Vector2):
        self.game = game
        self.size = size
        self.position = position


    def update(self):
        pass

    def blit(self, screen):
        pass


class Rectangle(Widget):
    def __init__(self, game, position: Vector2, size: Vector2, color):
        super().__init__(game, position, size)
        self.color = color

    def update(self):
        pass

    def blit(self, screen):
        pass


class Label:
    def __init__(self, game, position: Vector2, size: Vector2, text: str, color, text_color):
        self.game = game
        self.position = position
        self.size = size
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = Fonts["arial"].render(self.text, True, text_color)

    def update(self):
        pass

    def blit(self, screen):
        py.draw.rect(
            screen,
            self.color,
            (
                self.position.x(),
                self.position.y(),
                self.size.x(),
                self.size.y()
            )
        )

        screen.blit(self.font, (self.position.x() + self.size.x() // 2 - self.font.get_width() // 2, self.position.y() + self.size.y() // 2 - self.font.get_height() // 2))


class Button(Label):
    def __init__(self, game, position: Vector2, size: Vector2, text: str, color, text_color, callback):
        super().__init__(game, position, size, text, color, text_color)
        self.callback = callback

    def update(self):
        if py.mouse.get_pressed(3)[0]:
            if self.position.x() < py.mouse.get_pos()[0] < self.position.x() + self.size.x() and self.position.y() < py.mouse.get_pos()[1] < self.position.y() + self.size.y():
                self.callback()

    def blit(self, screen):
        super().blit(screen)
