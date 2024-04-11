import pygame as py
from os import listdir

py.init()
py.font.init()

# CONSTANT
TITLE = "Echoes Of Harmony"
RESMULT = 1.8
WIDTH, HEIGHT = int(800 * RESMULT), int(600 * RESMULT)
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
MAP_LENGHT = 4

# SET THE VALUES
SCREEN = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption(TITLE)

py.display.toggle_fullscreen()

# Yack
YACK_WIDTH = int(300 * RESMULT)
YACK_HEIGHT = int(225 * RESMULT)

# Fonts
Fonts = {
	"arial": py.font.Font("./Resources/arial.ttf", 12),
	"Grand arial": py.font.Font("./Resources/arial.ttf", 25),
	"centaur": py.font.SysFont("Centaur", 35),
}

HALO = py.transform.scale(py.image.load("Resources/Halo.png").convert_alpha(), (TILETOTALSIZE//2, TILETOTALSIZE))
HALO.set_alpha(100)

SHAMAN_WIDTH = 100
SHAMAN_HEIGHT = 200
SHAMAN = py.transform.scale(py.image.load("Resources/shaman.png").convert_alpha(), (SHAMAN_WIDTH, SHAMAN_HEIGHT))

CARD_WIDTH = int(55 * RESMULT)
CARD_HEIGHT = int(85 * RESMULT)

CardImg = [
	py.transform.scale(py.image.load("image/Card/carddash.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT)),
	py.transform.scale(py.image.load("image/Card/carddoublejump.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT)),
	py.transform.scale(py.image.load("image/Card/cardwalljump.png").convert_alpha(), (CARD_WIDTH, CARD_HEIGHT)),
]

FLOWER_SIZE = int(64 * RESMULT)
Flower = py.transform.scale(py.image.load("Resources/collectible_fleur.png").convert_alpha(), (FLOWER_SIZE, FLOWER_SIZE))

MenuImg = {
	"HomeMenu": py.transform.scale(py.image.load("image/MenuImg/home_menu.png").convert_alpha(), (500, 500)),
	"PauseMenu": py.transform.scale(py.image.load("image/MenuImg/pause_menu.png").convert_alpha(), (500, 500)),
	"ParamMenu": py.transform.scale(py.image.load("image/MenuImg/pause_menu.png").convert_alpha(), (500, 500)),
	"QuitMenu": py.transform.scale(py.image.load("image/MenuImg/banner_menu.png").convert_alpha(), (750, 250)),
	"ShopMenu": py.transform.scale(py.image.load("image/MenuImg/shop_menu.png").convert_alpha(), (1750, 1000)),
	"BigButton": py.transform.scale(py.image.load("image/MenuImg/big_button.png").convert_alpha(), (300, 50)),
	"FlowerButton": py.transform.scale(py.image.load("image/MenuImg/flower_button.png").convert_alpha(), (125, 50)),
	"LittleButton": py.transform.scale(py.image.load("image/MenuImg/little_button.png").convert_alpha(), (125, 50)),
	"MainMenu": py.transform.scale(py.image.load("image/MenuImg/UI menu principal.png").convert_alpha(), (WIDTH, HEIGHT)),
}

ENTREE_GROTTE = py.transform.scale(py.image.load("Resources/entree grotte.png").convert_alpha(), (500, 500))

IMAGE_VIDE = py.surface.Surface((1, 1))
IMAGE_VIDE.set_alpha(0)

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

Restart = py.transform.smoothscale(py.image.load("Resources/Restart.png").convert_alpha(), (WIDTH, HEIGHT))

Textures = [
	None,
	# Herbe
	py.transform.smoothscale(py.image.load("Resources/Tiles/haut gauche.png").convert_alpha(), (RESOLUTION, RESOLUTION)),
	py.transform.smoothscale(py.image.load("Resources/Tiles/haut centre.png").convert_alpha(), (RESOLUTION, RESOLUTION)),
	py.transform.smoothscale(py.image.load("Resources/Tiles/haut droite.png").convert_alpha(), (RESOLUTION, RESOLUTION)),
	py.transform.smoothscale(py.image.load("Resources/Tiles/gauche.png").convert_alpha(), (RESOLUTION, RESOLUTION)),
	py.transform.smoothscale(py.image.load("Resources/Tiles/centre.png").convert_alpha(), (RESOLUTION, RESOLUTION)),
	py.transform.smoothscale(py.image.load("Resources/Tiles/droite.png").convert_alpha(), (RESOLUTION, RESOLUTION)),
	py.transform.smoothscale(py.image.load("Resources/Tiles/bas gauche.png").convert_alpha(), (RESOLUTION, RESOLUTION)),
	py.transform.smoothscale(py.image.load("Resources/Tiles/bas.png").convert_alpha(), (RESOLUTION, RESOLUTION)),
	py.transform.smoothscale(py.image.load("Resources/Tiles/bas droite.png").convert_alpha(), (RESOLUTION, RESOLUTION)),
	# Pierre
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


