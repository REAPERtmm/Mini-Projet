
from Settings import *
from GameObject import *
from Map import *
from Menus import *

#define game variables
scroll = 0

ground_image = py.image.load("ground.png").convert_alpha()
ground_width = ground_image.get_width()
ground_height = ground_image.get_height()

bg_images = []
for i in range(1, 6):
  bg_image = py.image.load(f"plx-{i}.png").convert_alpha()
  bg_images.append(bg_image)
bg_width = bg_images[0].get_width()

class parallax:
    def __init__(self):

        # define game variables
        self.scroll = 0

        self.ground_image = py.image.load("ground.png").convert_alpha()
        self.ground_width = self.ground_image.get_width()
        self.ground_height = self.ground_image.get_height()

        self.bg_images = []
        for i in range(1, 6):
            self.bg_image = py.image.load(f"plx-{i}.png").convert_alpha()
            self.bg_images.append(self.bg_image)
        self.bg_width = self.bg_images[0].get_width()

    def draw_bg(self, screen):
        for x in range(5):
            speed = 1
            for i in self.bg_images:
                screen.blit(i, ((x * self.bg_width) - self.scroll * speed, 0))
                speed += 0.2

    def draw_ground(self, screen):
        for x in range(15):
            screen.blit(self.ground_image, ((x * self.ground_width) - self.scroll * 2.5, WIDTH - self.ground_height))

