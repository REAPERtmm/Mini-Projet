import pygame

from Settings import *
from GameObject import *
from Map import *
from Menus import *

class Game:
    def __init__(self):
        self.running = True

        self.ground = [
            StaticObject(self, -200, 200, 400, 100, "Ground"),
            StaticObject(self, 200, 100, 100, 200, "Wall"),
            StaticObject(self, 150, 0, 100, 50, "Platform"),
        ]

        self.map = Map(10, 1, 50, *[loadTile(path) for path in TILES])

        self.MainMenu = Menu(self,
                             Vector2(WIDTH//2 - 500//2, HEIGHT//2 - 500//2),
                             Vector2(500, 500),
                             WHITE)

        """self.labelTest = Label(self,
                               Vector2(WIDTH//2 - 500//2, HEIGHT//2 - 500//2),
                               Vector2(100, 100),
                               "YOOOO", BLACK, WHITE)"""

        """self.buttonTest = Button(self,
                                 Vector2(WIDTH // 2 - 100 // 2, HEIGHT // 2 - 100 // 2),
                                 Vector2(100, 100),
                                 "YOOOO", WHITE, BLACK,
                                 self.openmenu)"""

        self.leftPressed = False
        self.rightPressed = False
        self.up = False
        self.down = False
        self.tabPressed = False

        self.player = Player(self, 0, 0, 50, 75)
        self.camera = Camera(self, Vector2(0, 0), 5, self.player)
        self.clock = py.time.Clock()
        self.deltatime = 0

    def update(self):
        self.camera.update()
        """self.buttonTest.update()"""

    def draw(self):
        self.map.blit(SCREEN, self.camera)

        if self.tabPressed:
            self.MainMenu.blit(SCREEN)

        """self.buttonTest.blit(SCREEN)"""
        """self.labelTest.blit(SCREEN)"""

        py.display.flip()


    def run(self):
        while self.running:
            SCREEN.fill(SKY)
            self.deltatime = self.clock.get_time() / 1000
            self.clock.tick(60)
            self.update()
            self.draw()

            if self.leftPressed:
                self.player.transform.position.moveX(-10)
            if self.rightPressed:
                self.player.transform.position.moveX(10)
            if self.up:
                self.player.transform.position.moveY(-10)
            if self.down:
                self.player.transform.position.moveY(10)
            for event in py.event.get():
                if event.type == py.QUIT:
                    self.running = False
                if event.type == py.KEYUP:
                    if event.key == py.K_q:
                        self.leftPressed = False
                    if event.key == py.K_d:
                        self.rightPressed = False
                    if event.key == py.K_z:
                        self.up = False
                    if event.key == py.K_s:
                        self.down = False
                if event.type == py.KEYDOWN:
                    if not self.tabPressed:
                        if event.key == py.K_q:
                            self.leftPressed = True
                        if event.key == py.K_d:
                            self.rightPressed = True
                        if event.key == py.K_z:
                            self.up = True
                        if event.key == py.K_s:
                            self.down = True
                        if event.key == py.K_SPACE:
                            self.player.jump()
                    if event.key == py.K_TAB:
                        if self.tabPressed:
                            self.tabPressed = False
                        else:
                            self.tabPressed = True


g = Game()
g.run()
