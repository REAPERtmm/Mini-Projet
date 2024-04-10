from Settings import *
from Sound import *
import time


CardEq = {
    "Dash": 0,
    "Jump+": 1,
    "Bomb": 2
}


def fill_inventory(inv, *cards):
    for elt in cards:
        inv.AddCard(elt)


class Inventory:
    def __init__(self, game):
        # Références
        self.game = game
        self.my_font = py.font.SysFont('Resources/GEO_AI__.TTF', 64)
        # self.sounds = Sound(self)

        # UI Datas
        self.ui_hide_timer = 0
        self.hide_ui = True

        # Flower Count
        self.RedFlow = 0

        # Inventory
        self.InvContents = []
        self.selected_card = 0

    def AddCard(self, type):
        """Add New Card to the 1st slot"""
        """ INUTILE + Casse tout + ratio
        if len(self.InvContents) >= 3:
            self.InvContents.pop(0)
            self.RedFlow += 50
            self.ui_hide_timer = time.time()
            self.hide_ui = False
            """
        # self.sounds.Cardcollect()
        self.InvContents.append(type)

    def select(self, card):
        # self.sounds.CardSwap()
        if issubclass(type(card), int):
            self.selected_card = card
        else:
            self.selected_card = self.InvContents.index(card)

    def increaseRed(self):
        """increment the Red flower count"""
        # self.sounds.FlowerCollect()
        self.RedFlow += 10
        self.ui_hide_timer = time.time()
        self.hide_ui = False

    def update(self):
        """update the inventory"""
        if not self.hide_ui and time.time() - self.ui_hide_timer >= 3:
            self.hide_ui = True
            

    def draw(self):
        """Draw the inventory"""
        for i in range(len(self.InvContents)):
            if self.InvContents[i] not in CardEq:
                img = CardImg[0]  # Image par défault
            else:
                img = CardImg[CardEq[self.InvContents[i]]]  # Image equivalant au text

            SCREEN.blit(img, (SCREEN.get_width() - (i + 1) * 100, SCREEN.get_height() - (100 if self.selected_card == i else 10)))

        tracks = self.RedFlow
        colors = (173, 56, 45)
        if not self.hide_ui:
            track_text = self.my_font.render(str(tracks), True, colors)
            SCREEN.blit(Flower, (24, 64))
            SCREEN.blit(track_text, (24, 24))
        

