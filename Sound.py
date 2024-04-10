from Settings import *
from GameObject import *
from Map import *
from Menus import *
from parallax import *
from random import randint


class Sound:
    def __init__(self, game):
        self.game = game
        self.clock = py.time.Clock()
        self.deltatime = self.clock.get_time() / 1000
        py.mixer.init()
        self.dialogue_sound = None
        self.dialogue_channel = None
        self.running = True
        self.soundflag = False
        self.soundTimer = 0
        
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
        py.mixer.Channel(4).play(PlaySound, loops = -1)

    def Jump(self):
        PlaySound = py.mixer.Sound("SoundFiles/Jump.mp3")
        PlaySound.set_volume(0.5)
        py.mixer.Channel(5).play(PlaySound, loops = 0)

    def FlowerCollect(self):
        PlaySound = py.mixer.Sound("SoundFiles/Success.mp3")
        PlaySound.set_volume(0.3)
        py.mixer.Channel(2).play(PlaySound, loops = 0)

    def Cardcollect(self):
        PlaySound = py.mixer.Sound("SoundFiles/CardCollect.mp3")
        PlaySound.set_volume(0.3)
        py.mixer.Channel(6).play(PlaySound, loops = 0)

    def CardSwap(self):
        PlaySound = py.mixer.Sound("SoundFiles/CardSwap.mp3")
        PlaySound.set_volume(0.1)
        py.mixer.Channel(7).play(PlaySound, loops = 0)

    def FlagOff(self):
        self.soundflag = False
    
    def FlagOn(self):
        self.soundflag = True

    def ShamanStart(self):
        if self.soundflag == True and self.soundTimer > 0.15:
                self.soundTimer = 0
                self.ShamanVoice(randint(1, 17))
        
    def VoiceStop(self):
        py.mixer.Channel(1).stop()

    def EffectStop(self):
        py.mixer.Channel(2).stop()

    def MusicStop(self):
        py.mixer.Channel(3).stop()

    def AmbientStop(self):
        py.mixer.Channel(4).stop()