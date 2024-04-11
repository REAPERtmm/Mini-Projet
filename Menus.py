from GeoMath import *


class Menu:
    def __init__(self, game, position: Vector2, image, *widget):
        self.game = game
        self.position = position
        self.image = image
        self.widget = list(widget)

    def update(self):
        for w in self.widget:
            w.update()

    def blit(self, screen):
        screen.blit(self.image, (self.position.x(), self.position.y()))

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
    def __init__(self, game, position: Vector2, size: Vector2, image):
        super().__init__(game, position, size)
        self.image = image

    def update(self):
        pass

    def blit(self, screen):
        screen.blit(self.image, (self.position.x(), self.position.y()))


class Label(Widget):
    def __init__(self, game, position: Vector2, size: Vector2, text: str, image, text_color, font_name: str):
        super().__init__(game, position, size)
        self.text = text
        self.image = image
        self.text_color = text_color
        self.font = Fonts[font_name].render(self.text, True, text_color)

    def update(self):
        pass

    def blit(self, screen):
        screen.blit(self.image, (self.position.x(), self.position.y()))

        screen.blit(self.font, (self.position.x() + self.size.x() // 2 - self.font.get_width() // 2, self.position.y() + self.size.y() // 2 - self.font.get_height() // 2))


class Button(Label):
    def __init__(self, game, position: Vector2, size: Vector2, text: str, image, text_color, font_name, callback):
        super().__init__(game, position, size, text, image, text_color, font_name)
        self.callback = callback
        self.is_click = False

    def update(self):
        if py.mouse.get_pressed(3)[0] and self.position.x() < py.mouse.get_pos()[0] < self.position.x() + self.size.x() and self.position.y() < py.mouse.get_pos()[1] < self.position.y() + self.size.y():
            self.is_click = True
            if self.game.mouse_down:
                self.callback()
                self.game.mouse_down = False
        else:
            self.is_click = False

    def blit(self, screen):
        super().blit(screen)

        if self.is_click:
            image = py.Surface(self.size.tuple())
            image.fill(0)
            image.set_alpha(100)
            screen.blit(image, self.position.tuple())


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
