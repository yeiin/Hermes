import pygame
import time
import constant
 
music = constant.DEFAULT_MUSIC
music_state = None


def playMusic():
    global music_state
    pygame.mixer.init()
    
    if(music=="a"):
        pygame.mixer.music.load("/home/pi/Hermes/raspi/asset/music_a.mp3")
    else:
        pygame.mixer.music.load("/home/pi/Hermes/raspi/asset/music_b.mp3") 
    
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy() == True and music_state == True:
        continue


def changeMusic(newMusic):
    global music_state
    global music
    
    music_state = False
    music = newMusic
    music_state = True
    
    playMusic()


def endMusic():
    global music_state
    music_state = False
    pygame.mixer.music.stop()
    return