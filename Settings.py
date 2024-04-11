import pygame as py
from os import listdir

py.init()
py.font.init()
#py.mixer.init()

# CONSTANT
RESMULT = 2
WIDTH, HEIGHT = 800 * RESMULT, 600 * RESMULT
TITLE = "Echoes Of Harmony"
GRAVITY = 9.8 * 2 * RESMULT
RESOLUTION = 25 * RESMULT
TILERESOLUTION = 32
TILETOTALSIZE = RESOLUTION * TILERESOLUTION

# Player Values :
PLAYER_WIDTH = 50 * RESMULT
PLAYER_HEIGHT = 100 * RESMULT

# Trevor :
TREVOR_DELAY_BEFORE_START = 3# en seconde
TREVOR_SPEED = 400 * RESMULT  # pixels / sec

# Map:
MAP_LENGHT = 3

# SET THE VALUES
SCREEN = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption(TITLE)

# py.display.toggle_fullscreen()

# Yack
YACK_WIDTH = 200 * RESMULT
YACK_HEIGHT = 150 * RESMULT

# Fonts
Fonts = {
	"arial": py.font.Font("./Resources/arial.ttf", 12),
	"Grand arial": py.font.Font("./Resources/arial.ttf", 25),
}

CardImg = [
	py.transform.scale(py.image.load("Resources/Godspeed_Soul_Card.webp").convert_alpha(), (100 * RESMULT, 200 * RESMULT)),
	py.transform.scale(py.image.load("Resources/Elevate_Soul_Card.webp").convert_alpha(), (100 * RESMULT, 200 * RESMULT)),
	py.transform.scale(py.image.load("Resources/Purify_Soul_Card.webp").convert_alpha(), (100 * RESMULT, 200 * RESMULT)),
]

Flower = py.transform.scale(py.image.load("Resources/collectible_fleur.png").convert_alpha(), (64 * RESMULT, 64 * RESMULT))

MenuImg = [
	py.transform.scale(py.image.load("image/MenuImg/menu_pause_img.png").convert_alpha(), (1500, 750)),
	py.transform.scale(py.image.load("image/MenuImg/param_menu_img.png").convert_alpha(), (500, 550)),
	py.transform.scale(py.image.load("image/MenuImg/quit_menu_img.png").convert_alpha(), (1500, 750)),
	py.transform.scale(py.image.load("image/MenuImg/magasin.png").convert_alpha(), (1500, 1000)),
]

IMAGE_VIDE = py.surface.Surface((1, 1))
IMAGE_VIDE.set_alpha(0)

#Ground = py.transform.scale(py.image.load("Resources/ground.png"), (WIDTH, HEIGHT / 10))
Bg = [
	py.transform.scale(py.image.load(f"Resources/plx-{i}.png").convert_alpha(), (int(WIDTH * 1.5), int(HEIGHT * 1.5))) for i in range(1, 6)
]

Trevor = py.transform.scale(py.image.load("Resources/Trevor.png").convert_alpha(), (int(472 * TILETOTALSIZE / 281), TILETOTALSIZE))


Textures = [
	None,
	py.transform.smoothscale(py.image.load("Resources/Tiles/box.png").convert_alpha(), (RESOLUTION, RESOLUTION)),
	py.transform.smoothscale(py.image.load("Resources/Tiles/castle.png").convert_alpha(), (RESOLUTION, RESOLUTION)),
	py.transform.smoothscale(py.image.load("Resources/Tiles/groundNS_central.png").convert_alpha(), (RESOLUTION, RESOLUTION)),
	py.transform.smoothscale(py.image.load("Resources/Tiles/groundNS_topmid.png").convert_alpha(), (RESOLUTION, RESOLUTION)),
	py.transform.smoothscale(py.image.load("Resources/Tiles/groundS1_central.png").convert_alpha(), (RESOLUTION, RESOLUTION)),
	py.transform.smoothscale(py.image.load("Resources/Tiles/groundS1_topmid.png").convert_alpha(), (RESOLUTION, RESOLUTION)),
	py.transform.smoothscale(py.image.load("Resources/Tiles/groundS2_central.png").convert_alpha(), (RESOLUTION, RESOLUTION)),
	py.transform.smoothscale(py.image.load("Resources/Tiles/groundS2_topmid.png").convert_alpha(), (RESOLUTION, RESOLUTION)),
	py.transform.smoothscale(py.image.load("Resources/Tiles/Tile_Roc1.png").convert_alpha(), (RESOLUTION, RESOLUTION)),
	py.transform.smoothscale(py.image.load("Resources/Tiles/Tile_Roc2.png").convert_alpha(), (RESOLUTION, RESOLUTION)),
	py.transform.smoothscale(py.image.load("Resources/Tiles/Tile_Roc3.png").convert_alpha(), (RESOLUTION, RESOLUTION)),
	py.transform.smoothscale(py.image.load("Resources/Tiles/Tile_Roc4.png").convert_alpha(), (RESOLUTION, RESOLUTION)),
	py.transform.smoothscale(py.image.load("Resources/Tiles/Tile_Roc5.png").convert_alpha(), (RESOLUTION, RESOLUTION)),
	py.transform.smoothscale(py.image.load("Resources/Tiles/Tile_Roc6.png").convert_alpha(), (RESOLUTION, RESOLUTION)),
	py.transform.smoothscale(py.image.load("Resources/Tiles/Tile_Roc7.png").convert_alpha(), (RESOLUTION, RESOLUTION)),
	py.transform.smoothscale(py.image.load("Resources/Tiles/Tile_Roc8.png").convert_alpha(), (RESOLUTION, RESOLUTION)),
	py.transform.smoothscale(py.image.load("Resources/Tiles/Tile_Roc9.png").convert_alpha(), (RESOLUTION, RESOLUTION)),
]

TILES = ["Tile/" + path for path in listdir("./Tile")]

# Color Palette
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
SKY = (130, 200, 255)
CYAN = (0, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
TRANSPARENT_COLOR = (255, 255, 255, 0)


