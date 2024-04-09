from Settings import *
from Sound import *
import time


class Inventory:
    def __init__(self, game):
        # Références
        self.game = game
        self.my_font = py.font.SysFont('Resources/GEO_AI__.TTF', 64)

        # UI Datas
        self.ui_hide_timer = 0
        self.hide_ui = True

        # Flower Count
        self.BlueFlow = 0
        self.WhiteFlow = 0
        self.RedFlow = 0

        # Inventory
        self.InvContents = ["Bomb", "Jump+", "Dash"]
        self.selected_card = 0

    def AddCard(self, type):
        """Add New Card to the 1st slot"""
        if len(self.InvContents) >= 3:
            self.InvContents.pop(0)
            self.RedFlow += 50
            self.ui_hide_timer = time.time()
            self.hide_ui = False
        self.InvContents.append(type)

    def increaseBlue(self):
        """increment the blue flower count"""
        self.BlueFlow += 10
        self.ui_hide_timer = time.time()
        self.hide_ui = False

    def increaseWhite(self):
        """increment the White flower count"""
        self.WhiteFlow += 10
        self.ui_hide_timer = time.time()
        self.hide_ui = False

    def increaseRed(self):
        """increment the Red flower count"""
        self.RedFlow += 10
        self.ui_hide_timer = time.time()
        self.hide_ui = False
        print()

    def update(self):
        """update the inventory"""
        if not self.hide_ui and time.time() - self.ui_hide_timer >= 3:
            self.hide_ui = True

    def draw(self):
        """Draw the inventory"""
        for i in range(len(self.InvContents)):
            img = None
            if self.InvContents[i] == 'Dash':
                img = CardImg[0]
            elif self.InvContents[i] == 'Jump+':
                img = CardImg[1]
            elif self.InvContents[i] == 'Bomb':
                img = CardImg[2]

            SCREEN.blit(img, (SCREEN.get_width() - (i + 1) * 100, SCREEN.get_height() - (100 if self.selected_card == i else 10)))

        tracks = [self.RedFlow]
        colors = [(173, 56, 45)]
        if not self.hide_ui:
            for i, (track, color) in enumerate(zip(tracks, colors)):
                track_text = self.my_font.render(str(track), True, color)
                SCREEN.blit(Flower, (24, 64 + i * 64))
                SCREEN.blit(track_text, (24, 24 + i * 64))
        

