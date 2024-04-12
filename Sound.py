from random import randint


class Sound:
    def __init__(self, game):
        try:
            self.game = game
            self.clock = py.time.Clock()
            self.deltatime = self.clock.get_time() / 1000
            py.mixer.init()
            self.dialogue_sound = None
            self.dialogue_channel = None
            self.running = True
            self.soundflag = False
            self.soundTimer = 0
            self.enable = True
        except:
            self.enable = False
        
    def ShamanVoice(self, filedecider):
        if self.enable:
            dialogue_channel = py.mixer.Channel(1)
            filename = 'SoundFiles/ShamanMP3-{:02d}.mp3'.format(filedecider)
            dialogue_sound = py.mixer.Sound(filename)
            dialogue_sound.set_volume(2)
            dialogue_channel.play(dialogue_sound, loops=0)

    def ThemeMusic(self):
        if self.enable:
            PlaySound = py.mixer.Sound("SoundFiles/The Blinded Forest.mp3")
            PlaySound.set_volume(0.01)
            py.mixer.Channel(3).play(PlaySound, loops = -1)

    def PlayMenuSwap(self):
        if self.enable:
            PlaySound = py.mixer.Sound("SoundFiles/MenuSwapPercLighten.wav")
            py.mixer.Channel(2).play(PlaySound)

    def Walking(self):
        if self.enable:
            PlaySound = py.mixer.Sound("SoundFiles/GrassStep.mp3")
            PlaySound.set_volume(0.3)
            py.mixer.Channel(4).play(PlaySound, loops = -1)

    def Jump(self):
        if self.enable:
            PlaySound = py.mixer.Sound("SoundFiles/Jump.mp3")
            PlaySound.set_volume(0.5)
            py.mixer.Channel(5).play(PlaySound, loops = 0)

    def FlowerCollect(self):
        if self.enable:
            PlaySound = py.mixer.Sound("SoundFiles/Success.mp3")
            PlaySound.set_volume(0.3)
            py.mixer.Channel(2).play(PlaySound, loops = 0)

    def Cardcollect(self):
        if self.enable:
            PlaySound = py.mixer.Sound("SoundFiles/CardCollect.mp3")
            PlaySound.set_volume(0.3)
            py.mixer.Channel(6).play(PlaySound, loops = 0)

    def CardSwap(self):
        if self.enable:
            PlaySound = py.mixer.Sound("SoundFiles/CardSwap.mp3")
            PlaySound.set_volume(0.1)
            py.mixer.Channel(7).play(PlaySound, loops = 0)


    def dash(self):
        if self.enable:
            PlaySound = py.mixer.Sound("SoundFiles/DashWind.mp3")
            PlaySound.set_volume(0.1)
            py.mixer.Channel(7).play(PlaySound, loops = 0)

    def FlagOff(self):
        if self.enable:
            self.soundflag = False
    
    def FlagOn(self):
        if self.enable:
            self.soundflag = True

    def ShamanStart(self):
        if self.enable:
            if self.soundflag == True and self.soundTimer > 0.15:
                    self.soundTimer = 0
                    self.ShamanVoice(randint(1, 17))
        
    def VoiceStop(self):
        if self.enable:
            py.mixer.Channel(1).stop()

    def EffectStop(self):
        if self.enable:
            py.mixer.Channel(2).stop()

    def MusicStop(self):
        if self.enable:
            py.mixer.Channel(3).stop()

    def AmbientStop(self):
        if self.enable:
            py.mixer.Channel(4).stop()