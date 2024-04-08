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
        pygame.font.init()
        my_font = pygame.font.SysFont('Resources/GEO_AI__.TTF', 64)
        self.map.blit(SCREEN, self.camera)

        if self.tabPressed:
            self.main_menu.blit(SCREEN)

        # Calculate card positions
        card_positions = []
        for i in range(len(self.InvContents)):
            card_scale = self.CardScale[i]
            card_image = None
            if self.InvContents[i] == 'Dash':
                card_image = py.image.load("Resources/Godspeed_Soul_Card.webp")
            elif self.InvContents[i] == 'Jump+':
                card_image = py.image.load("Resources/Elevate_Soul_Card.webp")
            elif self.InvContents[i] == 'Bomb':
                card_image = py.image.load("Resources/Purify_Soul_Card.webp")
            
            if card_image is not None:
                card_width = int(card_image.get_width() * card_scale)
                card_height = int(card_image.get_height() * card_scale)
                card_positions.append((
                    ((WIDTH - (card_image.get_width() * 3)) - ((card_image.get_width() * -i) - 169) - card_image.get_width()),
                    (HEIGHT - 10) - card_height
                ))

        # Draw cards
        for i, (content, scale) in enumerate(zip(self.InvContents, self.CardScale)):
            card_image = None
            if content == 'Dash':
                card_image = py.image.load("Resources/Godspeed_Soul_Card.webp")
            elif content == 'Jump+':
                card_image = py.image.load("Resources/Elevate_Soul_Card.webp")
            elif content == 'Bomb':
                card_image = py.image.load("Resources/Purify_Soul_Card.webp")

            if card_image is not None:
                card_width = int(card_image.get_width() * scale)
                card_height = int(card_image.get_height() * scale)
                card_image = py.transform.scale(card_image, (card_width, card_height))
                card_rect = card_image.get_rect(topleft=card_positions[i])
                SCREEN.blit(card_image, card_rect)

        ImageB = py.transform.scale(py.image.load("Resources/collectible_fleur.png"), (64, 64))
        tracks = [self.BlueFlow, self.RedFlow, self.WhiteFlow]
        colors = [(51, 96, 163), (173, 56, 45), (242, 246, 252)]
        for i, (track, color) in enumerate(zip(tracks, colors)):
            track_text = my_font.render(str(track), True, color)
            SCREEN.blit(ImageB, (64, 12 + i * 64))
            SCREEN.blit(track_text, (24, 24 + i * 64))

        py.display.flip()

    def inv(self):
        self.BlueFlow = 0
        self.WhiteFlow = 0
        self.RedFlow = 0
        self.InvContents = []
        self.CardScale = [0, 0, 0]

    def run(self):
        selected_card = 0 
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
                    if event.key == py.K_r:
                        self.RedFlow += 1
                    if event.key == py.K_w:
                        self.WhiteFlow += 1
                    if event.key == py.K_i:
                        if len(self.InvContents) >= 3:
                            self.InvContents.pop(0)
                        self.InvContents.append("Dash")
                    if event.key == py.K_o:
                        if len(self.InvContents) >= 3:
                            self.InvContents.pop(0)
                        self.InvContents.append("Jump+")
                    if event.key == py.K_p:
                        if len(self.InvContents) >= 3:
                            self.InvContents.pop(0)
                        self.InvContents.append("Bomb")
                    if event.key == py.K_1:
                        selected_card = 0
                    if event.key == py.K_2:
                        selected_card = 1
                    if event.key == py.K_3:
                        selected_card = 2

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

            self.CardScale = [0.7, 0.7, 0.7]
            self.CardScale[selected_card] = 0.9

            


g = Game()
g.run()
