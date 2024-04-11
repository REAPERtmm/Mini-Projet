from Settings import *


img = py.Surface((WIDTH, HEIGHT)).convert_alpha()
img.fill((0, 0, 0))


class GameOver:
    def __init__(self, speed):
        self.speed = speed
        self.xf = False
        self.opacity = 0
        self.img = img
        self.is_game_over = False
        self.reset = False

    def fade(self, dt):
        if self.reset:
            self.reset = False
        if self.xf:
            self.opacity += dt * self.speed
            print("fade in progress")
            if self.opacity > 255:
                self.reset = True
                self.xf = False
        else:
            self.opacity -= dt * self.speed
            if self.opacity < 0:
                self.is_game_over = False

        self.Alpha()

    def game_over(self):
        self.is_game_over = True
        self.opacity = 0
        self.xf = True
        print("Game Over")

    def Affichage(self, screen):
        if self.is_game_over:
            screen.blit(self.img, (0, 0))

    def Alpha(self):
        self.img.set_alpha(self.opacity)