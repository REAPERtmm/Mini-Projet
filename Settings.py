import pygame as py
from os import listdir

py.init()
py.font.init()
py.mixer.init()

# CONSTANT
WIDTH, HEIGHT = 800, 600
TITLE = "JEU VACHEMENT COOL"
GRAVITY = 9.8
RESOLUTION = 25
TILERESOLUTION = 32

# SET THE VALUES
SCREEN = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption(TITLE)

# Fonts
Fonts = {
	"arial": py.font.Font("./Resources/arial.ttf", 12),
	"Grand arial": py.font.Font("./Resources/arial.ttf", 25),
}

CardImg = [
	py.transform.scale(py.image.load("Resources/Godspeed_Soul_Card.webp"), (100, 200)),
	py.transform.scale(py.image.load("Resources/Elevate_Soul_Card.webp"), (100, 200)),
	py.transform.scale(py.image.load("Resources/Purify_Soul_Card.webp"), (100, 200)),
]

Flower = py.transform.scale(py.image.load("Resources/collectible_fleur.png"), (64, 64))
#Ground = py.transform.scale(py.image.load("Resources/ground.png"), (WIDTH, HEIGHT / 10))
Bg = [
	py.transform.scale(py.image.load(f"Resources/plx-{i}.png"), (WIDTH * 1.5, HEIGHT * 1.5)) for i in range(1, 6)
]


Textures = [
	None,
	py.transform.smoothscale(py.image.load("Resources/groundNS_central.png"), (RESOLUTION, RESOLUTION)),
	py.transform.smoothscale(py.image.load("Resources/groundNS_topmid.png"), (RESOLUTION, RESOLUTION)),
    py.transform.smoothscale(py.image.load("Resources/groundS1_central.png"), (RESOLUTION, RESOLUTION)),
    py.transform.smoothscale(py.image.load("Resources/groundS1_topmid.png"), (RESOLUTION, RESOLUTION)),
    py.transform.smoothscale(py.image.load("Resources/groundS2_central.png"), (RESOLUTION, RESOLUTION)),
    py.transform.smoothscale(py.image.load("Resources/groundS2_topmid.png"), (RESOLUTION, RESOLUTION)),
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


