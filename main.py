from Inventory import *
from Game_over_test import *
from Sound import *


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
        self.lastPoint: Vector2 = None
        self.map: Map = None
        # self.sounds = Sound(self)
        self.boss = Boss(self, TILETOTALSIZE * MAP_LENGHT, 100 * RESMULT, 75 * RESMULT, 75 * RESMULT)

        self.ground = []
        self.interactible = [
            StaticObject(self, -Trevor.get_width(), 0, 1000 * RESMULT, 1000 * RESMULT, "Trevor", Trevor),
            StaticObject(self, MAP_LENGHT * TILETOTALSIZE - TILERESOLUTION * 2, 0, TILERESOLUTION * 2, TILERESOLUTION * 4, "Portail")
        ]

        self.inv = Inventory(self)
        fill_inventory(self.inv, "Dash", "Jump+", "Bomb")

        self.game_over = GameOver()

        self.show_quit_screen = False
        self.show_param_screen = False
        self.show_dash_card_description = False
        self.show_doublejump_card_description = False
        self.show_walljump_card_description = False

        self.mouse_down = False

        self.MainMenu = Menu(
            self,
            Vector2(WIDTH//2 - 1500//2, HEIGHT//2 - 750//2),
            MenuImg[0],
            Label(
                self,
                Vector2(WIDTH//2 - 300//2, HEIGHT//2 - 400//2),
                Vector2(300, 50),
                "PAUSE",
                IMAGE_VIDE,
                BLACK,
                "Grand arial"
            ),
            Frame(
                self,
                Vector2(WIDTH//2 - 300//2, HEIGHT//2 - 135//2),
                Button(
                    self,
                    Vector2(0, 0),
                    Vector2(300, 50),
                    "Jouer",
                    IMAGE_VIDE,
                    BLACK,
                    "Grand arial",
                    self.btn_play
                ),
                Button(
                    self,
                    Vector2(0, 0),
                    Vector2(300, 50),
                    "Paramètres",
                    IMAGE_VIDE,
                    BLACK,
                    "Grand arial",
                    self.screen_param
                ),
                Button(
                    self,
                    Vector2(0, 0),
                    Vector2(300, 40),
                    "Quitter",
                    IMAGE_VIDE,
                    BLACK,
                    "Grand arial",
                    self.screen_leave_game
                ),
                wrap=1,
                gap_y=40
            )
        )
        self.ParamMenu = Menu(
            self,
            Vector2(WIDTH // 2 - 500 // 2, HEIGHT // 2 - 550 // 2),
            MenuImg[1],
            Label(
                self,
                Vector2(WIDTH // 2 - 300 // 2, HEIGHT // 2 - 400 // 2),
                Vector2(300, 50),
                "PARAMETRES",
                IMAGE_VIDE,
                BLACK,
                "Grand arial"
            ),
            Label(
                self,
                Vector2(WIDTH // 2 - 250 // 2, HEIGHT // 2 - 100 // 2),
                Vector2(250, 50),
                "Coming Soon !",
                IMAGE_VIDE,
                BLACK,
                "Grand arial"
            ),
            Button(
                self,
                Vector2(WIDTH // 2 - 370 // 2, HEIGHT // 2 + 350 // 2),
                Vector2(125, 50),
                "Retour",
                IMAGE_VIDE,
                BLACK,
                "Grand arial",
                self.screen_param
            )
        )
        self.QuitMenu = Menu(
            self,
            Vector2(WIDTH // 2 - 1500 // 2, HEIGHT // 2 - 750 // 2),
            MenuImg[2],
            Label(
                self,
                Vector2(WIDTH // 2 - 500 // 2, HEIGHT // 2 - 150 // 2),
                Vector2(500, 50),
                "Voulez-vous vraiment quitter le jeu ?",
                IMAGE_VIDE,
                BLACK,
                "Grand arial"
            ),
            Frame(
                self,
                Vector2(WIDTH // 2 - 290 // 2, HEIGHT // 2 - 10 // 2),
                Button(
                    self,
                    Vector2(0, 0),
                    Vector2(105, 50),
                    "OUI",
                    IMAGE_VIDE,
                    BLACK,
                    "Grand arial",
                    self.leaving_game
                ),
                Button(
                    self,
                    Vector2(0, 0),
                    Vector2(100, 50),
                    "NON",
                    IMAGE_VIDE,
                    BLACK,
                    "Grand arial",
                    self.screen_leave_game
                ),
                gap_x=80
            )
        )

        self.ShopMenu = Menu(
            self,
            Vector2(0, 0),
            MenuImg[3],
            Frame(
                self,
                Vector2(95, 125),
                Button(
                    self,
                    Vector2(0, 0),
                    Vector2(110, 175),
                    "Dash Card",
                    IMAGE_VIDE,
                    BLACK,
                    "arial",
                    self.dash_card_description
                ),
                Button(
                    self,
                    Vector2(0, 0),
                    Vector2(110, 175),
                    "Dash Card",
                    IMAGE_VIDE,
                    BLACK,
                    "arial",
                    self.dash_card_description
                ),
                Button(
                    self,
                    Vector2(0, 0),
                    Vector2(110, 175),
                    "Double Jump Card",
                    IMAGE_VIDE,
                    BLACK,
                    "arial",
                    self.doublejump_card_description
                ),
                Button(
                    self,
                    Vector2(0, 0),
                    Vector2(110, 175),
                    "Double Jump Card",
                    IMAGE_VIDE,
                    BLACK,
                    "arial",
                    self.doublejump_card_description
                ),
                Button(
                    self,
                    Vector2(0, 0),
                    Vector2(110, 175),
                    "Wall Jump Card",
                    IMAGE_VIDE,
                    BLACK,
                    "arial",
                    self.walljump_card_description
                ),
                Button(
                    self,
                    Vector2(0, 0),
                    Vector2(110, 175),
                    "Wall Jump Card",
                    IMAGE_VIDE,
                    BLACK,
                    "arial",
                    self.walljump_card_description
                ),
                wrap=4,
                gap_x=32,
                gap_y=24
            )
        )
        self.DashCardDescription = Menu(
            self,
            Vector2(0, 0),
            IMAGE_VIDE,
            Label(
                self,
                Vector2(150, 565),
                Vector2(0, 0),
                "Carte",
                IMAGE_VIDE,
                BLACK,
                "Grand arial",
            ),
            Rectangle(
                self,
                Vector2(95, 586),
                Vector2(110, 175),
                IMAGE_VIDE,
            ),
            Button(
                self,
                Vector2(80, 820),
                Vector2(100, 50),
                "Buy",
                IMAGE_VIDE,
                BLACK,
                "Grand arial",
                self.add_dash_card_to_deck
            ),
            Label(
                self,
                Vector2(450, 565),
                Vector2(0, 0),
                "Description",
                IMAGE_VIDE,
                BLACK,
                "Grand arial",
            ),
            Label(
                self,
                Vector2(450, 650),
                Vector2(0, 0),
                "Permet d'effectuer",
                IMAGE_VIDE,
                BLACK,
                "Grand arial",
            ),
            Label(
                self,
                Vector2(450, 675),
                Vector2(0, 0),
                "un dash",
                IMAGE_VIDE,
                BLACK,
                "Grand arial",
            ),
            Label(
                self,
                Vector2(550, 845),
                Vector2(0, 0),
                "0",
                IMAGE_VIDE,
                BLACK,
                "Grand arial",
            )
        )
        self.DoubleJumpCardDescription = Menu(
            self,
            Vector2(0, 0),
            IMAGE_VIDE,
            Label(
                self,
                Vector2(150, 565),
                Vector2(0, 0),
                "Carte",
                IMAGE_VIDE,
                BLACK,
                "Grand arial",
            ),
            Rectangle(
                self,
                Vector2(95, 586),
                Vector2(110, 175),
                IMAGE_VIDE,
            ),
            Button(
                self,
                Vector2(80, 820),
                Vector2(100, 50),
                "Buy",
                IMAGE_VIDE,
                BLACK,
                "Grand arial",
                self.add_jump_card_to_deck
            ),
            Label(
                self,
                Vector2(450, 565),
                Vector2(0, 0),
                "Description",
                IMAGE_VIDE,
                BLACK,
                "Grand arial",
            ),
            Label(
                self,
                Vector2(450, 650),
                Vector2(0, 0),
                "Permet d'effectuer",
                IMAGE_VIDE,
                BLACK,
                "Grand arial",
            ),
            Label(
                self,
                Vector2(450, 675),
                Vector2(0, 0),
                "un double saut",
                IMAGE_VIDE,
                BLACK,
                "Grand arial",
            ),
            Label(
                self,
                Vector2(550, 845),
                Vector2(0, 0),
                "0",
                IMAGE_VIDE,
                BLACK,
                "Grand arial",
            )
        )
        self.WallJumpCardDescription = Menu(
            self,
            Vector2(0, 0),
            IMAGE_VIDE,
            Label(
                self,
                Vector2(150, 565),
                Vector2(0, 0),
                "Carte",
                IMAGE_VIDE,
                BLACK,
                "Grand arial",
            ),
            Rectangle(
                self,
                Vector2(95, 586),
                Vector2(110, 175),
                IMAGE_VIDE,
            ),
            Button(
                self,
                Vector2(80, 820),
                Vector2(100, 50),
                "Buy",
                IMAGE_VIDE,
                BLACK,
                "Grand arial",
                self.add_walljump_card_to_deck
            ),
            Label(
                self,
                Vector2(450, 565),
                Vector2(0, 0),
                "Description",
                IMAGE_VIDE,
                BLACK,
                "Grand arial",
            ),
            Label(
                self,
                Vector2(450, 650),
                Vector2(0, 0),
                "Permet d'effectuer",
                IMAGE_VIDE,
                BLACK,
                "Grand arial",
            ),
            Label(
                self,
                Vector2(450, 675),
                Vector2(0, 0),
                "un saut contre le mur",
                IMAGE_VIDE,
                BLACK,
                "Grand arial",
            ),
            Label(
                self,
                Vector2(550, 845),
                Vector2(0, 0),
                "0",
                IMAGE_VIDE,
                BLACK,
                "Grand arial",
            )
        )

        self.delay = time.time() + TREVOR_DELAY_BEFORE_START
        self.player = Player(self, 0, 0)

        self.loadMap()
        self.interactible[1].transform.position = self.lastPoint - self.interactible[1].transform.size

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

    def loadMap(self):
        self.map = createMapStartingWith(self, MAP_LENGHT, 0)
        self.boss.Start(creatingMapStrict(
            self,
            [
                createTileFromPath(self, "BossTile/1.tile"),
                createTileFromPath(self, "BossTile/3.tile")
            ],
            [0, 1],
            Vector2(TILETOTALSIZE * MAP_LENGHT + 1000, 0))
        )

        firstground = 0
        for tile in self.map.map[0].t_left:
            if tile != 0:
                break
            firstground += RESOLUTION
        self.spawnpoint = Vector2(0, firstground - PLAYER_HEIGHT)

        firstground = 0
        for tile in self.map.map[-1].t_right:
            if tile != 0:
                break
            firstground += RESOLUTION
        self.lastPoint = Vector2(MAP_LENGHT * TILETOTALSIZE - 1, firstground)
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

    """3 fonctions pour faire presque la même chose, parce que pas le temps de généraliser avec un dictionnaire"""
    def dash_card_description(self):
        self.show_dash_card_description = True
        self.show_walljump_card_description = False
        self.show_doublejump_card_description = False

    def doublejump_card_description(self):
        self.show_doublejump_card_description = True
        self.show_walljump_card_description = False
        self.show_dash_card_description = False

    def walljump_card_description(self):
        self.show_walljump_card_description = True
        self.show_doublejump_card_description = False
        self.show_dash_card_description = False

    def add_dash_card_to_deck(self):
        self.inv.AddCard("Dash")

    def add_jump_card_to_deck(self):
        self.inv.AddCard("Jump+")

    def add_walljump_card_to_deck(self):
        self.inv.AddCard("WallJump")

    def update(self):
        if not self.tabPressed and not self.show_quit_screen and not self.show_param_screen:
            self.ground.clear()
            self.ground += self.map.get_physique_on_screen(self.camera)
            if self.player.transform.position.x() > (MAP_LENGHT - 1) * TILETOTALSIZE:
                print("COLLISION !")
                self.ground += self.boss.map.get_physique_on_screen(self.camera)

            """if time.time() > self.delay and self.interactible[0].transform.position.x() < MAP_LENGHT * TILETOTALSIZE - self.interactible[0].transform.size.x():
                self.interactible[0].transform.position.moveX(self.deltatime * TREVOR_SPEED)"""

            for elt in self.ground:
                elt.update()
            self.player.update()
            self.boss.update()
            if self.player.transform.CollideRect(self.interactible[1].transform):
                self.player.transform.position = Vector2(TILETOTALSIZE * (MAP_LENGHT + len(self.boss.map.map) // 2), 0)
                self.boss.is_Active = True

            if self.player.transform.position.y() > TILETOTALSIZE + 50:
                self.player.transform.position = self.spawnpoint.copy()
            self.camera.update()

        if self.tabPressed:
            self.MainMenu.update()
        if self.show_quit_screen:
            self.QuitMenu.update()
        if self.show_param_screen:
            self.ParamMenu.update()

        if self.shopPressed:
            self.ShopMenu.update()
        if self.show_dash_card_description:
            self.DashCardDescription.update()
        if self.show_doublejump_card_description:
            self.DoubleJumpCardDescription.update()
        if self.show_walljump_card_description:
            self.WallJumpCardDescription.update()

    def draw(self):
        self.ParaX.draw_bg(SCREEN)
        for elt in self.interactible:
            elt.blit(SCREEN)
        self.map.blit(SCREEN, self.camera)
        self.player.blit(SCREEN)
        py.draw.rect(SCREEN, (50, 25, 5), (0, TILETOTALSIZE - self.camera.position.y(), WIDTH, HEIGHT))
        Xpos = self.interactible[0].transform.position.x() - self.camera.position.x() + self.interactible[0].transform.size.x()
        py.draw.line(SCREEN, (255, 0, 0), (Xpos, 0), (Xpos, TILETOTALSIZE))

        py.draw.line(SCREEN, (255, 0, 0), (self.boss.map.offset.x() - self.camera.position.x(), 0), (self.boss.map.offset.x() - self.camera.position.x(), TILETOTALSIZE))
        self.boss.map.blit(SCREEN, self.camera)
        self.boss.blit(SCREEN)
        # self.ParaX.draw_ground(SCREEN)

        self.inv.draw()

        if self.tabPressed:
            self.MainMenu.blit(SCREEN)
        if self.show_quit_screen:
            self.QuitMenu.blit(SCREEN)
        if self.show_param_screen:
            self.ParamMenu.blit(SCREEN)

        if self.shopPressed and not self.tabPressed:
            self.ShopMenu.blit(SCREEN)
        if self.show_dash_card_description:
            self.DashCardDescription.blit(SCREEN)
        if self.show_doublejump_card_description:
            self.DoubleJumpCardDescription.blit(SCREEN)
        if self.show_walljump_card_description:
            self.WallJumpCardDescription.blit(SCREEN)

        self.interactible[1].blit(SCREEN)

        SCREEN.blit(Fonts["arial"].render(f"fps : {self.clock.get_fps()}", True, GREEN, BLACK), (10, 10))
        SCREEN.blit(Fonts["arial"].render(f"time : {time.time_ns()}", True, GREEN, BLACK), (10, 30))

        # self.game_over.Affichage(SCREEN)

        py.display.flip()

    def run(self):
        # self.sounds.ThemeMusic()
        while self.running:
            SCREEN.fill(SKY)
            self.deltatime = self.clock.get_time() / 1000
            self.clock.tick(200)
            self.update()
            self.inv.update()
            self.draw()
            # self.sounds.ShamanStart()
            # self.sounds.soundTimer += self.deltatime

            if self.leftPressed:
                self.player.velocity.x(-500 * self.deltatime * RESMULT)
            elif self.rightPressed:
                self.player.velocity.x(500 * self.deltatime * RESMULT)
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
                        # self.sounds.AmbientStop()
                    if event.key == py.K_d:
                        self.rightPressed = False
                        # self.sounds.AmbientStop()
                    if event.key == py.K_r:
                        self.inv.increaseRed()
                    if event.key == py.K_1:
                        self.inv.select("Bomb")
                        # self.sounds.FlagOn()
                    if event.key == py.K_2:
                        self.inv.select("Jump+")
                        # self.sounds.FlagOff()
                    if event.key == py.K_3:
                        self.inv.select("Dash")
                        # self.sounds.FlagOff()

                if event.type == py.KEYDOWN:
                    if event.key == py.K_q:
                        self.leftPressed = True
                        # self.sounds.Walking()
                    if event.key == py.K_d:
                        self.rightPressed = True
                        # self.sounds.Walking()
                    if event.key == py.K_SPACE:
                        if not self.tabPressed and not self.shopPressed:
                            self.player.jump()
                            self.player.wall_jump()
                            # self.sounds.Jump()
                    if event.key == py.K_LSHIFT:
                        self.player.dash()
                        # self.sounds.dash()
                    if event.key == py.K_TAB:
                        if self.tabPressed:
                            self.tabPressed = False
                        else:
                            self.tabPressed = True
                    if event.key == py.K_o:
                        self.game_over.game_over()

                    #Ici pour gérer les event du shop
                    if event.key == py.K_e:
                        if not self.tabPressed:
                            self.shopPressed = not self.shopPressed


g = Game()
g.run()
