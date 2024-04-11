import pygame as py
from os import listdir

py.init()
py.font.init()

# CONSTANT
RESMULT = 1.8
WIDTH, HEIGHT = int(800 * RESMULT), int(600 * RESMULT)
TITLE = "JEU VACHEMENT COOL"
GRAVITY = 9.8 * 2 * RESMULT
RESOLUTION = int(25 * RESMULT)
TILERESOLUTION = 32
TILETOTALSIZE = RESOLUTION * TILERESOLUTION

# Player Values :
PLAYER_WIDTH = int(50 * RESMULT)
PLAYER_HEIGHT = int(100 * RESMULT)

# Trevor :
TREVOR_DELAY_BEFORE_START = 3# en seconde
TREVOR_SPEED = int(400 * RESMULT)  # pixels / sec

# Map:
MAP_LENGHT = 3

# SET THE VALUES
SCREEN = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption(TITLE)

# TODO Remettre le FullScreen
# py.display.toggle_fullscreen()

# Yack
YACK_WIDTH = int(300 * RESMULT)
YACK_HEIGHT = int(225 * RESMULT)

# Fonts
Fonts = {
	"arial": py.font.Font("./Resources/arial.ttf", 12),
	"Grand arial": py.font.Font("./Resources/arial.ttf", 25),
}

CLOCHE = py.transform.scale(py.image.load("Resources/cloche purificatrice.png").convert_alpha(), (235, 333))
HALO = py.transform.scale(py.image.load("Resources/Halo.png").convert_alpha(), (TILETOTALSIZE//2, TILETOTALSIZE))

SHAMAN_WIDTH = 100
SHAMAN_HEIGHT = 200
SHAMAN = py.transform.scale(py.image.load("Resources/shaman.png").convert_alpha(), (SHAMAN_WIDTH, SHAMAN_HEIGHT))

CARD_WIDTH = int(100 * RESMULT)
CARD_HEIGHT = int(200 * RESMULT)
CardImg = [
	py.transform.scale(py.image.load("Resources/Godspeed_Soul_Card.webp").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT)),
	py.transform.scale(py.image.load("Resources/Elevate_Soul_Card.webp").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT)),
	py.transform.scale(py.image.load("Resources/Purify_Soul_Card.webp").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT)),
]

FLOWER_SIZE = int(64 * RESMULT)
Flower = py.transform.scale(py.image.load("Resources/collectible_fleur.png").convert_alpha(), (FLOWER_SIZE, FLOWER_SIZE))

MenuImg = [
	py.transform.scale(py.image.load("image/MenuImg/menu_pause_img.png").convert_alpha(), (100, 200)),
	py.transform.scale(py.image.load("image/MenuImg/param_menu_img.png").convert_alpha(), (100, 200)),
	py.transform.scale(py.image.load("image/MenuImg/quit_menu_img.png").convert_alpha(), (100, 200)),
]


# Parallax
PARALLAX_WIDTH = int(WIDTH * 1.5)
PARALLAX_HEIGHT = int(HEIGHT * 1.5)
Bg = {
	"Plaine": [
		py.transform.scale(py.image.load(f"Resources/Parallax/Plaine/{i}.png").convert_alpha(), (PARALLAX_WIDTH, PARALLAX_HEIGHT)) for i in range(1, 4)
	],
	"Grotte": [
			py.transform.scale(py.image.load(f"Resources/Parallax/Grotte/{i}.png").convert_alpha(), (PARALLAX_WIDTH, PARALLAX_HEIGHT)) for i in range(1, 4)
		]
}

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


