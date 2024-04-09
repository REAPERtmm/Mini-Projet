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
        
    def ShamanVoice(self, filedecider):
        dialogue_channel = py.mixer.Channel(1)
        filename = 'SoundFiles/ShamanMP3-{:02d}.mp3'.format(filedecider)
        dialogue_sound = py.mixer.Sound(filename)
        dialogue_sound.set_volume(2)
        dialogue_channel.play(dialogue_sound, loops=0)

    def ThemeMusic(self):
        PlaySound = py.mixer.Sound("SoundFiles/The Blinded Forest.mp3")
        PlaySound.set_volume(0.01)
        py.mixer.Channel(3).play(PlaySound, loops = -1)

    def PlayMenuSwap(self):
        PlaySound = py.mixer.Sound("SoundFiles/MenuSwapPercLighten.wav")
        py.mixer.Channel(2).play(PlaySound)

    def Walking(self):
        PlaySound = py.mixer.Sound("SoundFiles/GrassStep.mp3")
        PlaySound.set_volume(0.3)
        py.mixer.Channel(2).play(PlaySound, loops = -1)

    def VoiceStop(self):
        py.mixer.Channel(1).stop()

    def EffectStop(self):
        py.mixer.Channel(2).stop()

    def MusicStop(self):
        py.mixer.Channel(3).stop()