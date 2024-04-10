from Inventory import *
from Map import *
from Menus import *
from parallax import *
from Events import *


def checkpoints(self):
    print("Nouveau Checkpoint")


# Fonction pour démarrer les checkpoints
def start_checkpoint(self):
    print("Checkpoint")


# Fonction pour gérer le game over
def game_over(self):
    print("Game Over! Score:")


class Game:
    def __init__(self):
        self.running = True
        self.spawnpoint: Vector2 = None
        self.map: Map = None

        self.ground = []
        self.interactible = [StaticObject(self, -Trevor.get_width(), 0, 1000, 1000, "Trevor", Trevor)]

        self.inv = Inventory(self)
        fill_inventory(self.inv, "Dash", "Jump+", "Bomb")

        self.MainMenu = Menu(
            self,
            Vector2(WIDTH//2 - 500//2, HEIGHT//2 - 500//2),
            Vector2(500, 500),
            WHITE,
            Label(
                self,
                Vector2(WIDTH//2 - 300//2, HEIGHT//2 - 400//2),
                Vector2(300, 50),
                "PAUSE",
                BLACK,
                WHITE,
                "Grand arial"
            ),
            Frame(
                self,
                Vector2(WIDTH//2 - 300//2, HEIGHT//2 - 200//2),
                Button(
                    self,
                    Vector2(0, 0),
                    Vector2(300, 50),
                    "Jouer",
                    RED,
                    BLACK,
                    "Grand arial",
                    self.btn_play
                ),
                Button(
                    self,
                    Vector2(0, 0),
                    Vector2(300, 50),
                    "Paramètres",
                    GREEN,
                    BLACK,
                    "Grand arial",
                    lambda: print("test")
                ),
                Button(
                    self,
                    Vector2(0, 0),
                    Vector2(300, 50),
                    "Quitter",
                    BLUE,
                    BLACK,
                    "Grand arial",
                    lambda: print("test")
                ),
                wrap=1,
                gap_x=50,
                gap_y=50
            )
        )

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

        # Créer les événements pour le checkpoint et le game over
        self.checkpoint_event = Event(start_checkpoint)
        self.game_over_event = Event(game_over)
        
    def loadMap(self):
        self.map = createMapStartingWith(self, 10, 0)

        firstground = 0
        for tile in self.map.map[0].t_left:
            if tile != 0:
                break
            firstground += RESOLUTION
        self.spawnpoint = Vector2(0, firstground - PLAYER_HEIGHT)

        self.player.transform.position = self.spawnpoint.copy()

    def btn_play(self):
        self.tabPressed = False

    def update(self):
        self.ground = self.map.get_physique_on_screen(self.camera)
        # self.interactible[0].transform.position.moveX(self.deltatime * 10)
        for elt in self.ground:
            elt.update()
        self.player.update()
        if self.player.transform.position.y() > TILETOTALSIZE + 50:
            self.player.transform.position = self.spawnpoint.copy()
        self.camera.update()
        if self.tabPressed:
            self.MainMenu.update()

    def draw(self):
        self.ParaX.draw_bg(SCREEN)
        for elt in self.interactible:
            elt.blit(SCREEN)
        self.map.blit(SCREEN, self.camera)
        self.player.blit(SCREEN)
        py.draw.rect(SCREEN, (50, 25, 5), (0, TILETOTALSIZE - self.camera.position.y(), WIDTH, HEIGHT))
        Xpos = self.interactible[0].transform.position.x() - self.camera.position.x() + self.interactible[0].transform.size.x()
        py.draw.line(SCREEN, (255, 0, 0), (Xpos, 0), (Xpos, TILETOTALSIZE))
        # self.ParaX.draw_ground(SCREEN)
        if self.tabPressed:
            self.MainMenu.blit(SCREEN)
        self.inv.draw()
        SCREEN.blit(Fonts["arial"].render(f"fps : {self.clock.get_fps()}", True, GREEN, BLACK), (10, 10))

        py.display.flip()

    def run(self):
        while self.running:
            SCREEN.fill(SKY)
            self.deltatime = self.clock.get_time() / 1000
            self.clock.tick(200)
            self.update()
            self.inv.update()
            self.draw()
            if not self.tabPressed:
                if self.leftPressed:
                    self.player.velocity.x(-500 * self.deltatime)
                elif self.rightPressed:
                    self.player.velocity.x(500 * self.deltatime)
                else:
                    self.player.velocity.x(0)
            for event in py.event.get():
                if event.type == py.QUIT:
                    self.running = False
                if event.type == py.KEYUP:
                    if event.key == py.K_q:
                        self.leftPressed = False
                    if event.key == py.K_d:
                        self.rightPressed = False
                    if event.key == py.K_r:
                        self.inv.increaseRed()
                    if event.key == py.K_1:
                        self.inv.select("Bomb")
                    if event.key == py.K_2:
                        self.inv.select("Jump+")
                    if event.key == py.K_3:
                        self.inv.select("Dash")

                if event.type == py.KEYDOWN:
                    if event.key == py.K_q:
                        self.leftPressed = True
                    if event.key == py.K_d:
                        self.rightPressed = True
                    if event.key == py.K_SPACE:
                        self.player.jump()
                    if event.key == py.K_LSHIFT:
                        self.player.dash()
                    if event.key == py.K_TAB:
                        if self.tabPressed:
                            self.tabPressed = False
                        else:
                            self.tabPressed = True


g = Game()
g.run()