import pygame as py
import random
from Inventory import *

class Shop:

    def __init__(self):
        self.cardPlacementShop = []
        pass

    #Montrer des cartes de la boutique aléatoirement parmi une sélection
    def randomPrintCard(self):
        while (i < 5):
            rand = random.randrange(0, len(Inventory.cardList)-1)
            print(Inventory.cardList[rand])
            i += 1
    def draw(self):
        py.transform.scale(py.image.load("Resources/magasin.png").convert_alpha(), (WIDTH, HEIGHT))

#Pas besoin ?
    # def quitShop(self):
    #     #sera utilisé lors de la selection du bouton quit
    #     exit(1)


class DeckShop():
    def __init__(self):
        self.SlotList = [" "," "," "]
        for i in range(5):
            for i in range(len(self.InvContents)):
                if self.InvContents[i] == 'Dash':
                    py.SCREEN.blit(py.image.load("Resources/Godspeed_Soul_Card.webp"), (py.WIDTH-(200+(100*i)), py.HEIGHT-250))
                if self.InvContents[i] == 'Jump+':
                    py.SCREEN.blit(py.image.load("Resources/Base pack/bg_castle.png"), (py.WIDTH-(200+(100*i)), py.HEIGHT-250))
                if self.InvContents[i] == 'Bomb':
                    py.SCREEN.blit(py.image.load("Resources/Purify_Soul_Card.webp"), (py.WIDTH-(200+(100*i)), py.HEIGHT-250))

                i += 1



    #Bulle de dialogue ou description d'object

    #Quitter la boutique