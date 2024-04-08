from Inventory import Inventory
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
        self.inv = Inventory(self)

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
        self.inv.draw()
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
                    if event.key == py.K_b:
                        self.inv.increaseBlue()
                    if event.key == py.K_r:
                        self.inv.increaseRed()
                    if event.key == py.K_w:
                        self.inv.increaseWhite()
                    if event.key == py.K_i:
                        self.inv.select(2)
                    if event.key == py.K_o:
                        self.inv.select(1)
                    if event.key == py.K_p:
                        self.inv.select(0)
                    if event.key == py.K_1:
                        self.inv.selected_card = 0
                    if event.key == py.K_2:
                        self.inv.selected_card = 1
                    if event.key == py.K_3:
                        self.inv.selected_card = 2

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
