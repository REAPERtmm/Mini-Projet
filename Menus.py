from GeoMath import *


class Menu:
    def __init__(self, game, position: Vector2, size: Vector2, color, *widget):
        self.game = game
        self.size = size
        self.position = position
        self.color = color
        self.widget = list(widget)

    def update(self):
        for w in self.widget:
            w.update()

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

        for widget in self.widget:
            widget.blit(screen)


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


class Label(Widget):
    def __init__(self, game, position: Vector2, size: Vector2, text: str, color, text_color, font_name: str):
        super().__init__(game, position, size)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = Fonts[font_name].render(self.text, True, text_color)

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
    def __init__(self, game, position: Vector2, size: Vector2, text: str, color, text_color, font_name, callback):
        super().__init__(game, position, size, text, color, text_color, font_name)
        self.callback = callback

    def update(self):
        #ajouter keydown
        if py.mouse.get_pressed(3)[0]:
            if self.position.x() < py.mouse.get_pos()[0] < self.position.x() + self.size.x() and self.position.y() < py.mouse.get_pos()[1] < self.position.y() + self.size.y():
                self.callback()

    def blit(self, screen):
        super().blit(screen)


class Frame(Widget):
    def __init__(self, game, position: Vector2, *widget, wrap=0, gap_x=0, gap_y=0):
        super().__init__(game, position, Vector2(0, 0))
        self.widget = list(widget)
        self.wrap = wrap
        self.gap_x = gap_x
        self.gap_y = gap_y

    def update(self):
        for w in self.widget:
            w.update()

    def blit(self, screen):
        x_align = self.position.x()
        y_align = self.position.y()
        max_height = 0
        for i in range(len(self.widget)):
            if self.widget[i].size.y() > max_height:
                max_height = self.widget[i].size.y()

            self.widget[i].position.y(y_align)
            self.widget[i].position.x(x_align)
            x_align += self.widget[i].size.x() + self.gap_x

            if self.wrap > 0 and i % self.wrap == self.wrap - 1:
                x_align = self.position.x()
                y_align += max_height + self.gap_y

            self.widget[i].blit(screen)
