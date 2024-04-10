from Inventory import *
from Map import *
from Menus import *
from parallax import *
from Events import *

TRANSPARENT_COLOR = (255, 255, 255, 0)


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
        self.load_shop_image()

        self.ground = []
        self.interactible = [StaticObject(self, -Trevor.get_width(), 0, 1000, 1000, "Trevor", Trevor)]

        self.inv = Inventory(self)
        fill_inventory(self.inv, "Dash", "Jump+", "Bomb")
        self.MainMenu = Menu(
            self,
            Vector2(WIDTH//2 - 500//2, HEIGHT//2 - 500//2),
            Vector2(500, 500),
            WHITE,
            Frame(
                self,
                Vector2(WIDTH//2 - 500//2, HEIGHT//2 - 500//2),
                Button(
                    self,
                    Vector2(WIDTH//2 - 500//2, HEIGHT//2 - 500//2),
                    Vector2(75, 75),
                    "YOOO",
                    RED,
                    BLACK,
                    lambda: print("test")
                ),
                Button(
                    self,
                    Vector2(0, 0),
                    Vector2(50, 50),
                    "YOOO",
                    GREEN,
                    BLACK,
                    lambda: print("test")
                ),
                Button(
                    self,
                    Vector2(0, 0),
                    Vector2(50, 50),
                    "YOOO",
                    BLUE,
                    BLACK,
                    lambda: print("test")
                ),
                wrap=2,
                gap_x=5,
                gap_y=5
            )
        )
        self.Shop = Menu(
            self,
            Vector2(0,0),
            Vector2(WIDTH//10, HEIGHT//10),
            TRANSPARENT_COLOR,
            Frame(
                self,
                Vector2(WIDTH//16, HEIGHT//8),
                Button(
                    self,
                    Vector2(0, 0),
                    Vector2(WIDTH//13, HEIGHT//5.5),
                    "Dash Card",
                    RED,
                    TRANSPARENT_COLOR,
                    lambda: print("test")
                ),
                Button(
                    self,
                    Vector2(0, 0),
                    Vector2(WIDTH//13, HEIGHT//5.5),
                    "Double Jump Card",
                    GREEN,
                    TRANSPARENT_COLOR,
                    lambda: print("test")
                ),
                Button(
                    self,
                    Vector2(0, 0),
                    Vector2(WIDTH//13, HEIGHT//5.5),
                    "Wall Jump Card",
                    BLUE,
                    TRANSPARENT_COLOR,
                    lambda: print("test")
                ),
                Button(
                    self,
                    Vector2(0, 0),
                    Vector2(WIDTH//13, HEIGHT//5.5),
                    "Wall Jump Card",
                    BLUE,
                    TRANSPARENT_COLOR,
                    lambda: print("test")
                ),
                Button(
                    self,
                    Vector2(0, 0),
                    Vector2(WIDTH//13, HEIGHT//5.5),
                    "Wall Jump Card",
                    BLUE,
                    TRANSPARENT_COLOR,
                    lambda: print("test")
                ),
                Button(
                    self,
                    Vector2(0, 0),
                    Vector2(WIDTH//13, HEIGHT//5.5),
                    "Wall Jump Card",
                    BLUE,
                    TRANSPARENT_COLOR,
                    lambda: print("test")
                ),
                wrap=4,
                gap_x=WIDTH//55,
                gap_y=HEIGHT//55
            ),
            Label(
                self,
                Vector2(WIDTH//20, HEIGHT//1.9),
                Vector2(WIDTH//10, HEIGHT//20),
                "Titre",
                TRANSPARENT_COLOR,
                BLACK,
                
            ),
            Label(
                self,
                Vector2(WIDTH//5.5, HEIGHT//1.9),
                Vector2(WIDTH//5, HEIGHT//20),
                "Description",
                TRANSPARENT_COLOR,
                BLACK,
                
            ),
            Label(
                self,
                Vector2(WIDTH//5.5, HEIGHT//1.7),
                Vector2(WIDTH//5, HEIGHT//5.8),
                "Lorem Ipsul dsiniosninsifnisnf",
                TRANSPARENT_COLOR,
                BLACK,
            ),
            Label(
                self,
                Vector2(WIDTH//20, HEIGHT//1.14),
                Vector2(WIDTH//10, HEIGHT//35),
                "Acheter",
                TRANSPARENT_COLOR,
                BLACK,
            ),
            Label(
                self,
                Vector2(WIDTH//1.75, HEIGHT//1.13),
                Vector2(WIDTH//10, HEIGHT//35),
                "Vendre :",
                TRANSPARENT_COLOR,
                BLACK,      
            ),
             Label(
                self,
                Vector2(WIDTH//1.65, HEIGHT//1.13),
                Vector2(WIDTH//10, HEIGHT//35),
                "Vendre :",
                TRANSPARENT_COLOR,
                BLACK,      
            ),
        )


        self.player = Player(self, 0, 0, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.loadMap()

        self.leftPressed = False
        self.rightPressed = False
        self.up = False
        self.down = False
        self.tabPressed = False
        self.shopPressed = False

        self.camera = Camera(self, Vector2(0, 0), 5, self.player)
        self.clock = py.time.Clock()
        self.deltatime = 0
        self.ParaX = Parallax(self)

        # Créer les événements pour le checkpoint et le game over
        self.checkpoint_event = Event(start_checkpoint)
        self.game_over_event = Event(game_over)

    def load_shop_image(self):
        
        shop_image = py.image.load("Resources/magasin.png").convert_alpha()
        self.shop_image = py.transform.scale(shop_image, (WIDTH, HEIGHT))

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
        # self.interactible[0].transform.position.moveX(self.deltatime * 10)
        for elt in self.ground:
            elt.update()
        self.player.update()
        if self.player.transform.position.y() > TILETOTALSIZE + 50:
            self.player.transform.position = self.spawnpoint.copy()
        self.camera.update()

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
        if self.tabPressed and not self.shopPressed:
            self.MainMenu.blit(SCREEN)
        
        if self.shopPressed and not self.tabPressed:
            SCREEN.blit(self.shop_image, (0, 0))
            self.Shop.blit(SCREEN)
        elif not self.tabPressed:
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
            if not self.tabPressed and not self.shopPressed:
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
                        if not self.tabPressed and not self.shopPressed:
                            self.player.jump()
                    if event.key == py.K_LSHIFT:
                        self.player.dash()
                    if event.key == py.K_TAB:
                        if not self.shopPressed:
                            self.tabPressed = not self.tabPressed
                    #Ici pour gérer les event du shop
                    if event.key == py.K_e:
                        if not self.tabPressed:
                            self.shopPressed = not self.shopPressed
                        


g = Game()
g.run()