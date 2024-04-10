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

        self.show_quit_screen = False
        self.show_param_screen = False

        self.mouse_down = False

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
                WHITE,
                BLACK,
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
                    self.screen_param
                ),
                Button(
                    self,
                    Vector2(0, 0),
                    Vector2(300, 50),
                    "Quitter",
                    BLUE,
                    BLACK,
                    "Grand arial",
                    self.screen_leave_game
                ),
                wrap=1,
                gap_x=50,
                gap_y=50
            )
        )

        self.QuitMenu = Menu(
            self,
            Vector2(WIDTH // 2 - 500 // 2, HEIGHT // 2 - 200 // 2),
            Vector2(500, 200),
            WHITE,
            Label(
                self,
                Vector2(WIDTH//2 - 500//2, HEIGHT//2 - 150//2),
                Vector2(500, 50),
                "Voulez-vous vraiment quitter le jeu ?",
                WHITE,
                BLACK,
                "Grand arial"
            ),
            Frame(
                self,
                Vector2(WIDTH//2 - 250//2, HEIGHT//2),
                Button(
                    self,
                    Vector2(0, 0),
                    Vector2(100, 50),
                    "OUI",
                    BLACK,
                    WHITE,
                    "Grand arial",
                    self.leaving_game
                ),
                Button(
                    self,
                    Vector2(0, 0),
                    Vector2(100, 50),
                    "NON",
                    BLACK,
                    WHITE,
                    "Grand arial",
                    self.screen_leave_game
                ),
                gap_x=50
            )
        )

        self.ParamMenu = Menu(
            self,
            Vector2(WIDTH // 2 - 500 // 2, HEIGHT // 2 - 500 // 2),
            Vector2(500, 500),
            WHITE,
            Label(
                self,
                Vector2(WIDTH // 2 - 300 // 2, HEIGHT // 2 - 400 // 2),
                Vector2(300, 50),
                "PARAMETRES",
                WHITE,
                BLACK,
                "Grand arial"
            ),
            Label(
                self,
                Vector2(WIDTH // 2 - 250 // 2, HEIGHT // 2 - 100 // 2),
                Vector2(250, 50),
                "Coming Soon !",
                WHITE,
                BLACK,
                "Grand arial"
            ),
            Button(
                self,
                Vector2(WIDTH // 2 - 450 // 2, HEIGHT // 2 + 350 // 2),
                Vector2(125, 50),
                "← Retour",
                BLACK,
                WHITE,
                "Grand arial",
                self.screen_param
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

    def screen_leave_game(self):
        if self.show_quit_screen:
            self.show_quit_screen = False
            self.tabPressed = True
        else:
            self.show_quit_screen = True
            self.tabPressed = False

    def leaving_game(self):
        self.running = False

    def screen_param(self):
        if self.show_param_screen:
            self.show_param_screen = False
            self.tabPressed = True
        else:
            self.show_param_screen = True
            self.tabPressed = False

    def update(self):
        if not self.tabPressed and not self.show_quit_screen and not self.show_param_screen:
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

        if self.show_quit_screen:
            self.QuitMenu.update()

        if self.show_param_screen:
            self.ParamMenu.update()

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

        if self.show_quit_screen:
            self.QuitMenu.blit(SCREEN)

        if self.show_param_screen:
            self.ParamMenu.blit(SCREEN)

        py.display.flip()

    def run(self):
        while self.running:
            SCREEN.fill(SKY)
            self.deltatime = self.clock.get_time() / 1000
            self.clock.tick(200)
            self.update()
            self.inv.update()
            self.draw()

            if self.leftPressed:
                self.player.velocity.x(-500 * self.deltatime)
            elif self.rightPressed:
                self.player.velocity.x(500 * self.deltatime)
            else:
                self.player.velocity.x(0)
            for event in py.event.get():
                if event.type == py.QUIT:
                    self.running = False
                if event.type == py.MOUSEBUTTONDOWN:
                    self.mouse_down = True
                else:
                    self.mouse_down = False
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