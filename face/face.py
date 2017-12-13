import pygame
import pygame.time
from PIL import Image
import random
from threading import Thread
import time

# Change this value to speed up or slow down your game
FPS = 60

#Global Variables to be used through our program

WINDOWWIDTH = 480
WINDOWHEIGHT = 320
LINETHICKNESS = 10
PADDLESIZE = 50
PADDLEOFFSET = 20

# Set up the colours
BLACK     = (0  ,0  ,0  )
WHITE     = (255,255,255)

facesIdx = [1,2,3,4,6,7,8,9,10,14,15,16,17,18,22,23,24,25,26,52]
Face_start = False


class Face():
    def __init__(self, ser):
        self.ser = ser
        self.key_esc_pressed = False

    def showFaces(self):
        global Face_start
        Face_start = True

        # pygame.init()
        size = (WINDOWWIDTH, WINDOWHEIGHT)
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Face")
        c = pygame.time.Clock()  # create a clock object for timing

        # serialReadThread = Thread(target=self.check_input)
        # serialReadThread.daemon = True
        # serialReadThread.start()
        print("Face start!")
        # while not self.key_esc_pressed:
            # pass
        idx = random.randrange(0, len(facesIdx))
        filename = "images/bmo" + str(facesIdx[idx]) + ".jpg"
        img = pygame.image.load(filename)
        screen.blit(img, (0, 0))
        pygame.display.update()
        c.tick(60)
        # if serialReadThread.isAlive:
        #     print("Face serial alive!")
        Face_start = False
        # pygame.quit()


    def check_input(self):
        while True:
            try:
                data_str = str(self.ser.readline().decode('UTF-8')).rstrip().lstrip()
                # print("face", data_str)

                if "PONG" in data_str or "TEMP" in data_str:
                    self.key_esc_pressed = True
                    break
            except Exception as e:
                pass
