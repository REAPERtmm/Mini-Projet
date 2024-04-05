# from PIL import Image
import pygame as py
#from main import *

isBoughtCard = False
isBoughtUpgrade = False
isActivable = False

flower = 0
cardLevel = 0
maxUpgradeLevel = 3

backgroundShop = py.image.load("Ressources/signHangingBed").convert()
card = py.image.load("Ressources/windowOpen").convert()


class Deck:

    def __init__(self):
        self.cardList = ["carte pétée sa mère", "test", "wolaaaaa"]
    

class Card:

    def __init__(self):
        self.isAvailable = False 
        pass

    # def update(self):
    #     self.player.update()
    #     for elt in self.ground:
    #         elt.update()
    #     self.camera.update()

    #Achetée ou non (donc activée dans l'inventaire ou non)
    #appelé dans l'inventaire
    def isBought(self):
        for i in range(len(cardList)-1):
            if (isBoughtCard == True):
                isActivable = True
                availableCardList[i] = cardList[i]
                cardList[i].remove()
            else:
                isActivable = False

    #Upgrade *3 maxi achetable contre de l'argent

    def UpgradeCard(self):
        if (isActivable == True and cardLevel < maxUpgradeLevel and isBoughtUpgrade == True):
            cardLevel += 1

    #affichage carte
    def draw(self):
        Image.open(houseDarkMidRight) 





#class DashCard

    #Mettre un cooldown
    #backgroundShop = py.image.load("Ressources/DashCard").convert()
    #def CardCooldown():


class Shop:

    def __init__(self):
        pass

    def draw(self):
        Image.open(signHangingBed) 

    # def update(self):
        #self.player.update()
        #for elt in self.ground:
        #elt.update()
        #self.camera.update()
        #Achat de carte --> Check si le joueur a assez de fleurs 
        #et pas de doublon de carte dans l'inventaire ET dans la boutique (index unique)

    def isEnoughFlower(self):
        if (flower < 0):
            print("Voici les cartes : " + Deck.cardList[0])
            randomPrintCard()
        else:
            print("Vous n'avez aucune fleur sur vous")

        

    #Montrer des cartes de la boutique aléatoirement parmi une sélection
    def randomPrintCard(self):
        while (i < 5):
            rand = random.randrange(len(cardList)-1)
            print(cardList[rand])
            i += 1

    def quitShop(self):
        #sera utilisé lors de la selection du bouton quit


class DeckShop():
    def __init__(self):
        self.SlotList = [" "," "," "," "," "]

        for (i < 5):
            for i in range(len(self.InvContents)):
                if self.InvContents[i] == 'Dash':
                    SCREEN.blit(py.image.load("Resources/Godspeed_Soul_Card.webp"), (WIDTH-(200+(100*i)), HEIGHT-250))
                if self.InvContents[i] == 'Jump+':
                    SCREEN.blit(py.image.load("Resources/Base pack/bg_castle.png"), (WIDTH-(200+(100*i)), HEIGHT-250))
                if self.InvContents[i] == 'Bomb':
                    SCREEN.blit(py.image.load("Resources/Purify_Soul_Card.webp"), (WIDTH-(200+(100*i)), HEIGHT-250))

                i += 1


    #Bulle de dialogue ou description d'object

    #Quitter la boutique

