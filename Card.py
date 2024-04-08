# from PIL import Image
import pygame as py
#from main import *
import random



backgroundShop = py.image.load("Ressources/signHangingBed").convert()
card = py.image.load("Ressources/windowOpen").convert()


class Inventory:

    def __init__(self):
        self.cardList = []
        flower = 100
    

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
        cardLevel = 0

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
            if (cardLevel < self.MAX_UPGRADE_LEVEL):
                cardLevel += 1
                Inventory.flower -= self.upgradeCost
            else:
                print("Vous êtes déjà au maximum !")
        else:
            print("Okay pas d'upgrade dans ce cas !")

    #affichage carte


class Shop:

    def __init__(self):
        cardPlacement = []
        pass

    #Montrer des cartes de la boutique aléatoirement parmi une sélection
    def randomPrintCard(self):
        while (i < 5):
            rand = random.randrange(0, len(Inventory.cardList)-1)
            print(Inventory.cardList[rand])
            i += 1

    def quitShop(self):
        #sera utilisé lors de la selection du bouton quit
        exit(1)


class DeckShop():
    def __init__(self):
        self.SlotList = [" "," "," "," "," "]
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
def main():
    dashCard = Card()
    print(dashCard.isBuyable)
    dashCard.isBuyable = False 
    print(dashCard.isBuyable)

main()
