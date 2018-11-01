# to speech conversion
from gtts import gTTS
import pygame
import winsound
import os

def textPlay():
    f = open("output.txt", "r")

    text = f.read()


    # Language in which you want to convert
    language = 'en'

    # Passing the text and language to the engine, 
    # here we have marked slow=False. Which tells 
    # the module that the converted audio should 
    # have a high speed
    myobj = gTTS(text=text, lang=language, slow=False)
    myobj.save("welcome.wav")
    '''
    print('Playing')
    winsound.PlaySound("This is real this is me",winsound.SND_FILENAME)
    pygame.init()
    t= pygame.mixer.Sound("welcome.wav")
    t.play()'''

    os.system("start welcome.wav")
