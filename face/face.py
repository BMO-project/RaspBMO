from PIL import Image

import threading
import pygame
import pygame.time
from pygame.locals import *

facesIdx = [1,2,3,4,6,7,8,9,10,14,15,16,17,18,22,23,24,25,26,52]
Face_start = False

class Face():
    def __init__(self):
        pass

def showFaces():
    global Face_start
    Face_start = True
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    c = pygame.time.Clock()

    for i in facesIdx:
        filename = "images/bmo" + str(i) + ".jpg"
        img = pygame.image.load(filename)


        #img = Image.open(filename)
        #
        # mode = img.mode
        # size = img.size
        # data = img.tobytes()
        #
        # print(size)
        #
        # py_img = pygame.image.fromstring(data, size, mode)
        screen.blit(img, (0, 0))

        pygame.display.flip()

        c.tick(1)