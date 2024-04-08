from Settings import *
from GameObject import *
from Inventory import Inventory
from Map import *
from Menus import *
from parallax import *


class Game:
    def __init__(self):
        self.running = True
        self.spawnpoint: Vector2 = None
        self.map: Map = None

        self.ground = []
        self.interactible = [StaticObject(self, -Trevor.get_width(), 0, 1000, 1000, "Trevor", Trevor)]

        self.inv = Inventory(self)
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

        self.player = Player(self, 0, 0, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.loadMap()

        self.leftPressed = False
        self.rightPressed = False
        self.up = False
        self.down = False
        self.tabPressed = False

        self.camera = Camera(self, Vector2(0, 0), 5, self.player)
        self.clock = py.time.Clock()
        self.deltatime = 0
        self.ParaX = Parallax(self)

    def loadMap(self):
        self.map = createMapStartingWith(self, 10, 0)

        firstground = 0
        for tile in self.map.map[0].t_left:
            if tile != 0:
                break
            firstground += RESOLUTION
        self.spawnpoint = Vector2(0, firstground - PLAYER_HEIGHT)

        self.player.transform.position = self.spawnpoint.copy()

    def update(self):
        self.ground = self.map.get_physique_on_screen(self.camera)
        self.interactible[0].transform.position.moveX(self.deltatime * 10)
        for elt in self.ground:
            elt.update()
        self.player.update()
        if self.player.transform.position.y() > TILETOTALSIZE + 50:
            self.player.transform.position = self.spawnpoint.copy()
        self.camera.update()
        """self.buttonTest.update()"""

    def draw(self):
        self.ParaX.draw_bg(SCREEN)
        for elt in self.interactible:
            elt.blit(SCREEN)
        self.map.blit(SCREEN, self.camera)
        self.player.blit(SCREEN)
        py.draw.rect(SCREEN, (50, 25, 5), (0, TILETOTALSIZE - self.camera.position.y(), WIDTH, HEIGHT))
        Xpos = self.interactible[0].transform.position.x() - self.camera.position.x() + self.interactible[0].transform.size.x()
        print(Xpos)
        py.draw.line(SCREEN, (255, 0, 0), (Xpos, 0), (Xpos, TILETOTALSIZE))
        # self.ParaX.draw_ground(SCREEN)
        if self.tabPressed:
            self.MainMenu.blit(SCREEN)
        self.inv.draw()
        py.display.flip()

    def run(self):
        while self.running:
            SCREEN.fill(SKY)
            self.deltatime = self.clock.get_time() / 1000
            self.clock.tick(60)
            self.update()
            self.draw()
            if not self.tabPressed:
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
                    if event.key == py.K_RSHIFT:
                        self.player.dash()
                    if event.key == py.K_TAB:
                        if self.tabPressed:
                            self.tabPressed = False
                        else:
                            self.tabPressed = True

g = Game()
g.run()

