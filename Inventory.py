from Settings import *
from Sound import *
import time


CardEq = {
    "Dash": 0,
    "Jump+": 1,
    "WallJump": 2
}


def fill_inventory(inv, *cards):
    for elt in cards:
        inv.AddCard(elt)


class Inventory:
    def __init__(self, game):
        # Références
        self.game = game
        self.my_font = Fonts["arial"]
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
        # self.sounds.Cardcollect()
        if len(self.InvContents) < 3:
            try:
                self.game.player.ability_enable[type] = True
            except KeyError:
                pass

            self.InvContents.append(type)

    def RemoveCard(self, index):
        if index < len(self.InvContents):
            try:
                self.game.player.ability_enable[self.InvContents[index]] = False
            except KeyError:
                pass
            self.InvContents.pop(index)

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
