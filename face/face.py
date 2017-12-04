import pygame
import pygame.time
from PIL import Image

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

    image = Image.open("../images/bmo1.jpg")
    image.show()


    # for i in facesIdx:
    #     filename = "images/bmo" + str(i) + ".jpg"
    #     img = pygame.image.load(filename)
    #
    #     screen.blit(img, (0, 0))
    #
    #     pygame.display.flip()
    #
    #     c.tick(1)

if __name__ == '__main__':
    showFaces()