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

        self.main_menu = Menu(self, 500, 500)

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

    def draw(self):
        self.map.blit(SCREEN, self.camera)

        if self.tabPressed:
            self.main_menu.blit(SCREEN)

        for i in range(len(self.InvContents)):
            if self.InvContents[i] == 'Dash':
                SCREEN.blit(py.image.load("Resources/Godspeed_Soul_Card.webp"), (WIDTH-(200+(100*i)), HEIGHT-250))
            if self.InvContents[i] == 'Jump+':
                SCREEN.blit(py.image.load("Resources/Elevate_Soul_Card.webp"), (WIDTH-(200+(100*i)), HEIGHT-250))
            if self.InvContents[i] == 'Bomb':
                SCREEN.blit(py.image.load("Resources/Purify_Soul_Card.webp"), (WIDTH-(200+(100*i)), HEIGHT-250))

        py.display.flip()

    def inv(self):
        self.BlueFlow = 0
        self.WhiteFlow = 0
        self.RedFlow = 0
        self.InvContents = []
        self.CardScale = [0, 0, 0]

    def run(self):
        self.inv()
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
                    if event.key == py.K_b:
                        self.BlueFlow += 1
                        print(self.BlueFlow, self.RedFlow, self.WhiteFlow, self.InvContents, self.CardScale)
                    if event.key == py.K_r:
                        self.RedFlow += 1
                        print(self.BlueFlow, self.RedFlow, self.WhiteFlow, self.InvContents, self.CardScale)
                    if event.key == py.K_w:
                        self.WhiteFlow += 1
                        print(self.BlueFlow, self.RedFlow, self.WhiteFlow, self.InvContents, self.CardScale)
                    if event.key == py.K_i:
                        if len(self.InvContents) >= 3:
                            self.InvContents.pop(0)
                        self.InvContents.append("Dash")
                        print(self.BlueFlow, self.RedFlow, self.WhiteFlow, self.InvContents, self.CardScale)
                    if event.key == py.K_o:
                        if len(self.InvContents) >= 3:
                            self.InvContents.pop(0)
                        self.InvContents.append("Jump+")
                        print(self.BlueFlow, self.RedFlow, self.WhiteFlow, self.InvContents, self.CardScale)
                    if event.key == py.K_p:
                        if len(self.InvContents) >= 3:
                            self.InvContents.pop(0)
                        self.InvContents.append("Bomb")
                        print(self.BlueFlow, self.RedFlow, self.WhiteFlow, self.InvContents, self.CardScale)
                    if event.key == py.K_1:
                        pass
                    if event.key == py.K_2:
                        pass
                    if event.key == py.K_3:
                        pass

                if event.type == py.KEYDOWN:
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
