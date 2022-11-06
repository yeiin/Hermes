import pygame
import time
import constant
 
music = constant.DEFAULT_MUSIC
end = False

def playMusic():
    global end
    global count
    print(">>>>>>>>>>>playMusic")
    pygame.mixer.init()
    
    if(music=="a"):
        pygame.mixer.music.load("/home/pi/Hermes/raspi/asset/music_a.mp3")
    else:
        pygame.mixer.music.load("/home/pi/Hermes/raspi/asset/music_b.mp3") 
    
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy() == True and end == False:
        continue


def changeMusic(newMusic):
    global end
    global music
    
    end = True
    music = newMusic
    end = False
    
    playMusic()


def endMusic():
    global end
    end = True

def main():
    playMusic()

if __name__ == "__main__":
	main()