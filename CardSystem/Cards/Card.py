import pygame as py
from main import *
import CardSystem.Inventory as Inventory



# backgroundShop = py.image.load("Ressources/signHangingBed").convert()
# card = py.image.load("Ressources/windowOpen").convert()

class Card:

    MAX_UPGRADE_LEVEL = 3

    def __init__(self):
        self.title = "Default Title"
        self.description = "Default Description"
        self.upgradeDescription = "Defaut Upgrade Description"
        self.cooldown = 2
        self.cost = 2
        self.upgradeCost = 3
        self.isBuyable = True 
        self.isBoughtUpgrade = False
        self.cardLevel = 0
        self.cardImage = None

        pass

    #Achetée ou non (donc activée dans l'inventaire ou non)
    #appelé dans l'inventaire
    def buyCard(self):
        for i in range(len(Inventory.cardList)-1):
            if(Inventory.flower >= self.cost):
                if (self.isBuyable == True):
                    self.isBuyable = False
                    Inventory.cardList[i].append()
                    Inventory.flower -= self.cost
                    print("Merci pour votre achat de carte !")
                else:
                    print("Vous possédez déjà cette carte")
            else:
                print("Vous n'avez pas assez de fleurs !")

    #Upgrade *3 maxi achetable contre de l'argent

    def UpgradeCard(self):
        isBoughtUpgrade = input("Voulez-vous acheter l'amélioration ?")
        if (isBoughtUpgrade.lower() == 'y'):
            if (self.cardLevel < self.MAX_UPGRADE_LEVEL):
                self.cardLevel += 1
                Inventory.flower -= self.upgradeCost
            else:
                print("Vous êtes déjà au maximum !")
        else:
            print("Okay pas d'upgrade dans ce cas !")

    #affichage carte
