from Settings import *


class Parallax:
    def __init__(self, game, offsetY):
        self.game = game
        self.offsetY = offsetY
        self.current = "Plaine"

    def set_current(self, new_current):
        self.current = new_current

    def draw_bg(self, screen):
        depth = len(Bg[self.current])
        speed = .5
        for i in range(0, depth):
            for j in range(2):
                screen.blit(
                    Bg[self.current][i],
                    (
                        (-self.game.camera.position.x() * speed) % PARALLAX_WIDTH - j * PARALLAX_WIDTH,
                        TILETOTALSIZE - PARALLAX_HEIGHT - self.game.camera.position.y() + self.offsetY
                    )
                )
            speed += 1 / (depth * 2)


"""    def draw_ground(self, screen):
        for j in range(3):
            screen.blit(Ground, (0 - (j-1) * WIDTH, HEIGHT * 9/10))"""

