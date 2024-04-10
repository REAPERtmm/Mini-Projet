from Settings import *

bg_game_over = py.image.load("C:/Users/gravit/Documents/GitHub/Mini-Projet/Resources/Game_over.png").convert_alpha()

img = py.Surface((WIDTH, HEIGHT))
img.fill((0,0,0))

class GameOver:
    def __init__(self):
        self.xf = False
        self.opacity = 0
        self.img = img
        self.is_game_over = False
        self.screen =py.display.set_mode((WIDTH, HEIGHT))

    def fade(self):
        if self.xf:
            self.opacity += 1
            print("fade in progress")
            if self.opacity > 2000:
                self.xf = False

        else:
            self.opacity -= 1

        self.Alpha()

    def game_over(self):
        self.is_game_over = True
        print("Game Over")

    def Affichage(self):
        if self.is_game_over:
            self.screen.fill((0,0,0))

    def Alpha(self):
        self.img.set_alpha(self.opacity)