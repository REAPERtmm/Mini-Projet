import pygame as py

py.init()
py.font.init()
py.mixer.init()

# CONSTANT
WIDTH, HEIGHT = 800, 600
TITLE = "JEU VACHEMENT COOL"
GRAVITY = 9.8
RESOLUTION = 50

# SET THE VALUES
SCREEN = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption(TITLE)

# Fonts
Fonts = {
	"arial": py.font.Font("./Resources/arial.ttf", 12),
	"Grand arial": py.font.Font("./Resources/arial.ttf", 25),
}

Textures = [
	None,
	py.transform.smoothscale(py.image.load("Resources/Base pack/Tiles/box.png"), (RESOLUTION, RESOLUTION))
]

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

