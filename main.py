from Settings import *
from GameObject import *


class Game:
    def __init__(self):
        self.running = True

        self.ground = [
            StaticObject(self, -200, 400, 900, 50)
        ]

        self.leftPressed = False
        self.rightPressed = False

        self.player = Player(self, 0, 0, 100, 100)
        self.camera = Camera(self, Vector2(0, 0), 2.5, self.player)
        self.clock = py.time.Clock()
        self.deltatime = 0

    def update(self):
        self.camera.update()
        for elt in self.ground:
            elt.update()
        self.player.update()

    def draw(self):
        SCREEN.fill(0)
        for elt in self.ground:
            elt.blit(SCREEN)
        self.player.blit(SCREEN)
        py.display.flip()

    def run(self):
        while self.running:
            self.deltatime = self.clock.get_time() / 1000
            self.clock.tick(60)
            self.update()
            self.draw()

            if self.leftPressed:
                self.player.transform.position.moveX(-10)
            if self.rightPressed:
                self.player.transform.position.moveX(10)
            for event in py.event.get():
                if event.type == py.QUIT:
                    self.running = False
                if event.type == py.KEYUP:
                    if event.key == py.K_q:
                        self.leftPressed = False
                    if event.key == py.K_d:
                        self.rightPressed = False
                if event.type == py.KEYDOWN:
                    if event.key == py.K_q:
                        self.leftPressed = True
                    if event.key == py.K_d:
                        self.rightPressed = True
                    if event.key == py.K_SPACE:
                        self.player.jump()


g = Game()
g.run()
