from Inventory import *
from Game_over_test import *
from Sound import *


class Game:
    def __init__(self):
        self.running = True
        self.spawnpoint: Vector2 = None
        self.lastPoint: Vector2 = None
        self.map: Map = None
        # self.sounds = Sound(self)

        self.boss = Boss(self, TILETOTALSIZE * MAP_LENGHT, TILERESOLUTION * 10)

        self.ground = []
        self.interactible = [
            StaticObject(self, -Trevor.get_width() - 100, 0, 1000 * RESMULT, 1000 * RESMULT, "Trevor", Trevor),
            StaticObject(self, MAP_LENGHT * TILETOTALSIZE - TILERESOLUTION * 2, 0, TILERESOLUTION * 2, TILERESOLUTION * 4, "Portail")
        ]

        self.game_over = GameOver(500)

        self.show_quit_screen = False
        self.show_param_screen = False
        self.show_dash_card_description = False
        self.show_doublejump_card_description = False
        self.show_walljump_card_description = False

        self.mouse_down = False

        self.MainMenu = Menu(
            self,
            Vector2(WIDTH//2 - 500//2, HEIGHT//2 - 500//2),
            MenuImg["PauseMenu"],
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
                    MenuImg["BigButton"],
                    BLACK,
                    "Grand arial",
                    self.btn_play
                ),
                Button(
                    self,
                    Vector2(0, 0),
                    Vector2(300, 50),
                    "Paramètres",
                    MenuImg["BigButton"],
                    BLACK,
                    "Grand arial",
                    self.screen_param
                ),
                Button(
                    self,
                    Vector2(0, 0),
                    Vector2(300, 40),
                    "Quitter",
                    MenuImg["BigButton"],
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
            Vector2(WIDTH // 2 - 500 // 2, HEIGHT // 2 - 500 // 2),
            MenuImg["ParamMenu"],
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
                MenuImg["LittleButton"],
                BLACK,
                "Grand arial",
                self.screen_param
            )
        )
        self.QuitMenu = Menu(
            self,
            Vector2(WIDTH // 2 - 1500 // 2, HEIGHT // 2 - 750 // 2),
            MenuImg["QuitMenu"],
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
            Vector2(-200, -50),
            MenuImg["ShopMenu"],
            Frame(
                self,
                Vector2(115, 130),
                Button(
                    self,
                    Vector2(0, 0),
                    Vector2(102, 155),
                    "",
                    CardImg[0],
                    BLACK,
                    "arial",
                    self.dash_card_description
                ),
                Button(
                    self,
                    Vector2(0, 0),
                    Vector2(102, 155),
                    "",
                    CardImg[0],
                    BLACK,
                    "arial",
                    self.dash_card_description
                ),
                Button(
                    self,
                    Vector2(0, 0),
                    Vector2(102, 155),
                    "",
                    CardImg[1],
                    BLACK,
                    "arial",
                    self.doublejump_card_description
                ),
                Button(
                    self,
                    Vector2(0, 0),
                    Vector2(102, 155),
                    "",
                    CardImg[1],
                    BLACK,
                    "arial",
                    self.doublejump_card_description
                ),
                Button(
                    self,
                    Vector2(0, 0),
                    Vector2(102, 155),
                    "",
                    CardImg[2],
                    BLACK,
                    "arial",
                    self.walljump_card_description
                ),
                Button(
                    self,
                    Vector2(0, 0),
                    Vector2(102, 155),
                    "",
                    CardImg[2],
                    BLACK,
                    "arial",
                    self.walljump_card_description
                ),
                wrap=4,
                gap_x=32,
                gap_y=26
            )
        )
        self.DashCardDescription = Menu(
            self,
            Vector2(0, 0),
            IMAGE_VIDE,
            Label(
                self,
                Vector2(165, 535),
                Vector2(0, 0),
                "Carte",
                IMAGE_VIDE,
                BLACK,
                "Grand arial",
            ),
            Rectangle(
                self,
                Vector2(115, 555),
                Vector2(110, 175),
                CardImg[0],
            ),
            Button(
                self,
                Vector2(100, 750),
                Vector2(125, 50),
                "Buy",
                MenuImg["FlowerButton"],
                BLACK,
                "Grand arial",
                self.add_dash_card_to_deck
            ),
            Label(
                self,
                Vector2(450, 535),
                Vector2(0, 0),
                "Description",
                IMAGE_VIDE,
                BLACK,
                "Grand arial",
            ),
            Label(
                self,
                Vector2(450, 625),
                Vector2(0, 0),
                "Permet d'effectuer",
                IMAGE_VIDE,
                BLACK,
                "Grand arial",
            ),
            Label(
                self,
                Vector2(450, 650),
                Vector2(0, 0),
                "un dash",
                IMAGE_VIDE,
                BLACK,
                "Grand arial",
            ),
            Label(
                self,
                Vector2(550, 790),
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
                Vector2(165, 535),
                Vector2(0, 0),
                "Carte",
                IMAGE_VIDE,
                BLACK,
                "Grand arial",
            ),
            Rectangle(
                self,
                Vector2(115, 555),
                Vector2(110, 175),
                CardImg[1],
            ),
            Button(
                self,
                Vector2(100, 750),
                Vector2(125, 50),
                "Buy",
                MenuImg["FlowerButton"],
                BLACK,
                "Grand arial",
                self.add_dash_card_to_deck
            ),
            Label(
                self,
                Vector2(450, 535),
                Vector2(0, 0),
                "Description",
                IMAGE_VIDE,
                BLACK,
                "Grand arial",
            ),
            Label(
                self,
                Vector2(450, 625),
                Vector2(0, 0),
                "Permet d'effectuer",
                IMAGE_VIDE,
                BLACK,
                "Grand arial",
            ),
            Label(
                self,
                Vector2(450, 650),
                Vector2(0, 0),
                "un double jump",
                IMAGE_VIDE,
                BLACK,
                "Grand arial",
            ),
            Label(
                self,
                Vector2(550, 790),
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
                Vector2(165, 535),
                Vector2(0, 0),
                "Carte",
                IMAGE_VIDE,
                BLACK,
                "Grand arial",
            ),
            Rectangle(
                self,
                Vector2(115, 555),
                Vector2(110, 175),
                CardImg[2],
            ),
            Button(
                self,
                Vector2(100, 750),
                Vector2(125, 50),
                "Buy",
                MenuImg["FlowerButton"],
                BLACK,
                "Grand arial",
                self.add_dash_card_to_deck
            ),
            Label(
                self,
                Vector2(450, 535),
                Vector2(0, 0),
                "Description",
                IMAGE_VIDE,
                BLACK,
                "Grand arial",
            ),
            Label(
                self,
                Vector2(450, 625),
                Vector2(0, 0),
                "Permet d'effectuer",
                IMAGE_VIDE,
                BLACK,
                "Grand arial",
            ),
            Label(
                self,
                Vector2(450, 650),
                Vector2(0, 0),
                "un wall jump",
                IMAGE_VIDE,
                BLACK,
                "Grand arial",
            ),
            Label(
                self,
                Vector2(550, 790),
                Vector2(0, 0),
                "0",
                IMAGE_VIDE,
                BLACK,
                "Grand arial",
            )
        )

        self.TrevorIsMoving = False
        self.player = Player(self, 0, 0)
        self.inv = Inventory(self)
        fill_inventory(self.inv, "Dash", "Jump+", "WallJump")

        self.delay = time.time() + TREVOR_DELAY_BEFORE_START

        self.loadMap()
        self.interactible[1].transform.position = self.lastPoint - self.interactible[1].transform.size

        self.leftPressed = False
        self.rightPressed = False
        self.up = False
        self.down = False
        self.tabPressed = False
        self.shopPressed = False
        self.is_Interacting = False

        self.shaman = StaticObject(self, TILETOTALSIZE/2, TILETOTALSIZE - RESOLUTION * 7 - SHAMAN_HEIGHT, 0, 0, "Shaman", SHAMAN)
        self.camera = Camera(self, Vector2(0, 0), 5, self.player)
        self.clock = py.time.Clock()
        self.deltatime = 0
        self.ParaX = Parallax(self, HEIGHT / 3)
        self.firstTileLeft = createfulltile(self, Vector2(-TILETOTALSIZE, 0))

    def loadBoss(self):
        self.boss.Start(creatingMapStrict(
            self,
            [
                createTileFromPath(self, "BossTile/1.tile"),
                createTileFromPath(self, "BossTile/2.tile"),
                createTileFromPath(self, "BossTile/3.tile")
            ],
            [1, 0, 2, 1],
            Vector2(TILETOTALSIZE * MAP_LENGHT + 1000, 0))
        )

    def loadMap(self):
        self.map = createMapStartingWith(self, MAP_LENGHT, 0)
        self.loadBoss()

        firstground = 0
        for i in range(len(self.map.map[0].t_left) - 1, -1, -1):
            tile = self.map.map[0].t_left[i]
            if tile == 0:
                firstground += RESOLUTION
        self.spawnpoint = Vector2(0, firstground - PLAYER_HEIGHT)

        firstground = 0
        for i in range(len(self.map.map[-1].t_right) - 1, -1, -1):
            tile = self.map.map[-1].t_right[i]
            if tile == 0:
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

    def kill(self):
        if not self.game_over.is_game_over:
            self.game_over.game_over()
            self.boss.is_Active = False

    def update(self):
        self.game_over.fade(self.deltatime)
        if distance(self.player.transform.position, self.shaman.transform.position) > 100:
            self.shopPressed = False

        if not self.game_over.is_game_over:
            if not self.TrevorIsMoving and self.player.transform.position.x() > TILETOTALSIZE:
                self.TrevorIsMoving = True

            if not self.tabPressed and not self.show_quit_screen and not self.show_param_screen:
                self.ground.clear()
                if self.boss.is_Active:
                    self.ground = self.boss.get_physic(self.camera)
                else:
                    self.ground = self.map.get_physique_on_screen(self.camera)
                if not self.TrevorIsMoving:
                    self.ground.append(self.firstTileLeft.collision[0])
                if self.TrevorIsMoving and self.interactible[0].transform.position.x() < TILETOTALSIZE * MAP_LENGHT:
                    self.interactible[0].transform.position.moveX(self.deltatime * TREVOR_SPEED)
                for elt in self.ground:
                    elt.update()
                self.player.update()
                self.boss.update()
                if self.player.transform.CollideRect(self.interactible[1].transform):
                    self.boss.EnterRoom()
                    self.player.transform.position = Vector2(TILETOTALSIZE * (MAP_LENGHT + len(self.boss.map.map) // 2), 0)
                    self.boss.is_Active = True
                    self.ParaX.set_current("Grotte")
                    self.ParaX.offsetY = HEIGHT / 5

                if self.player.transform.position.y() > TILETOTALSIZE + 50:
                    self.player.transform.position = self.spawnpoint.copy()
                self.camera.update()

                if self.player.transform.CollideRect(self.boss.transform) or self.player.transform.CollideRect(self.interactible[0].transform):
                    self.kill()

            if self.tabPressed:
                self.MainMenu.update()

            if self.show_quit_screen:
                self.QuitMenu.update()

            if self.show_param_screen:
                self.ParamMenu.update()
        else:
            if self.game_over.reset:
                self.player.animator.set_anim("idle")
                self.player.transform.position = self.spawnpoint.copy()
                self.camera.position = self.spawnpoint - Vector2(self.camera.size / 2, self.camera.size / 2)
                self.ParaX.set_current("Plaine")
                self.ParaX.offsetY = HEIGHT / 3
                self.loadBoss()
                self.TrevorIsMoving = False
                self.interactible[0].transform.position.x(-Trevor.get_width() - 100)

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
        # dessine le parallax
        self.ParaX.draw_bg(SCREEN)

        if not self.boss.is_Active:
            # dessine la map
            self.map.blit(SCREEN, self.camera)

            # dessine le point de Tp au boss et la Tornade
            for elt in self.interactible:
                elt.blit(SCREEN)

            self.firstTileLeft.blit(SCREEN)

        # Cache le bas de l'écran
        py.draw.rect(SCREEN, (50, 25, 5) if self.ParaX.current == "Plaine" else BLACK, (0, TILETOTALSIZE - self.camera.position.y(), WIDTH, HEIGHT))

        if self.boss.is_Active:
            # dessine le boss et la map du boss
            self.boss.blit(SCREEN)

        # dessine le shaman
        self.shaman.blit(SCREEN)

        # dessine le joueur
        self.player.blit(SCREEN)

        # dessine l'ATH
        self.inv.draw()

        # Dessine l'UI du menu
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

        # dessine les fps et le temps
        SCREEN.blit(Fonts["arial"].render(f"fps : {self.clock.get_fps()}", True, GREEN, BLACK), (10, 10))

        # Dessine d'autre Menus
        if self.show_quit_screen:
            self.QuitMenu.blit(SCREEN)
        if self.show_param_screen:
            self.ParamMenu.blit(SCREEN)

        # dessine l'affichage du fade du game over (opacitée variante)
        self.game_over.Affichage(SCREEN)

        # actualise l'écran
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
                        self.inv.select("WallJump")
                        # self.sounds.FlagOn()
                    if event.key == py.K_2:
                        self.inv.select("Jump+")
                        # self.sounds.FlagOff()
                    if event.key == py.K_3:
                        self.inv.select("Dash")
                        # self.sounds.FlagOff()
                    if event.key == py.K_a:
                        self.is_Interacting = False

                if event.type == py.KEYDOWN:
                    if event.key == py.K_q:
                        self.leftPressed = True
                        # self.sounds.Walking()
                    if event.key == py.K_d:
                        self.rightPressed = True
                        # self.sounds.Walking()
                    if event.key == py.K_SPACE:
                        if not self.tabPressed and not self.shopPressed:
                            self.player.double_jump()
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

                    if event.key == py.K_a:
                        self.is_Interacting = True

                    # Ici pour gérer les event du shop
                    if event.key == py.K_e:
                        if not self.tabPressed and distance(self.player.transform.position, self.shaman.transform.position) < 100:
                            self.shopPressed = not self.shopPressed


g = Game()
g.run()
