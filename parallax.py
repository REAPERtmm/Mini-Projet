from Settings import *

class Parallax:
    def __init__(self, game):
        self.game = game

    def draw_bg(self, screen):
        speed = .2
        for i in range(1, 5):
            for j in range(3):
                screen.blit(Bg[i], ((-self.game.camera.position.x() * speed) % (WIDTH * 1.5) - (j-1) * (WIDTH * 1.5), -self.game.camera.position.y() - 50))
            speed += .2


"""    def draw_ground(self, screen):
        for j in range(3):
            screen.blit(Ground, (0 - (j-1) * WIDTH, HEIGHT * 9/10))"""

