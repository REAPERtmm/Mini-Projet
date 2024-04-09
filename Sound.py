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
        # Generate a random index for the dialogue sound file
        filedecider = randint(1, 17)
        
        # Construct the file path based on the random index
        filename = 'SoundFiles/ShamanMP3-{:02d}.mp3'.format(filedecider)
        
        # Load the dialogue sound
        dialogue_sound = py.mixer.Sound(filename)
        
        # Create a sound channel for dialogue
        dialogue_channel = py.mixer.Channel(0)
        
        # Play the dialogue sound in a loop
        dialogue_channel.play(dialogue_sound, loops=-1)

    def ShamanVoiceStop(self):
        py.mixer.Channel(0).stop()
