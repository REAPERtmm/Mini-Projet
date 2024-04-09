from Settings import *
from GameObject import *
from Map import *
from Menus import *
from parallax import *
from random import randint


class Sound:
    def __init__(self, game):
        self.game = game
        py.mixer.init()
        self.dialogue_sound = None
        self.dialogue_channel = None
        self.running = True
        
    def ShamanVoice(self):
        filedecider = randint(1, 17)
        filename = 'SoundFiles/ShamanMP3-{:02d}.mp3'.format(filedecider)
        dialogue_sound = py.mixer.Sound(filename)
        dialogue_channel = py.mixer.Channel(0)
        dialogue_channel.play(dialogue_sound, loops=-1)

    def ShamanVoiceStop(self):
        py.mixer.Channel(0).stop()

    def PlayMenuSwap(self):
        PlaySound = py.mixer.Sound("SoundFiles/MenuSwapPercLighten.wav")
        py.mixer.Sound.play(PlaySound)