import pygame, sys
from pygame.locals import *
from threading import Thread
import time
# Number of frames per second
# Change this value to speed up or slow down your game
FPS = 60

#Global Variables to be used through our program

WINDOWWIDTH = 400
WINDOWHEIGHT = 300
LINETHICKNESS = 10
PADDLESIZE = 50
PADDLEOFFSET = 20
BASICFONT = 20
BASICFONTSIZE = None

# Set up the colours
BLACK     = (0  ,0  ,0  )
WHITE     = (255,255,255)

pong_start = False

class Pong():
    def __init__(self, ser):
        self.ser = ser
        self.key_up_pressing = False
        self.key_down_pressing = False
        self.key_esc_pressed = False
        self.score = 0
        self.FPSCLOCK = None
        self.screen = None
        self.ballDirX = None
        self.ballDirY = None
        self.paddle1 = None
        self.paddle2 = None
        self.ball = None
        pass

    #Draws the arena the game will be played in.
    def drawArena(self):
        # print("asdf")
        self.screen.fill((0,0,0))
        #Draw outline of arena
        # print("asdf")
        pygame.draw.rect(self.screen, WHITE, ((0, 0), (WINDOWWIDTH, WINDOWHEIGHT)), LINETHICKNESS*2)
        #Draw centre line
        # print("asdf")
        pygame.draw.line(self.screen, WHITE, (int((WINDOWWIDTH/2)), 0), (int((WINDOWWIDTH/2)), WINDOWHEIGHT), int((LINETHICKNESS/4)))


    #Draws the paddle
    def drawPaddle(self, paddle):
        #Stops paddle moving too low
        if paddle.bottom > WINDOWHEIGHT - LINETHICKNESS:
            paddle.bottom = WINDOWHEIGHT - LINETHICKNESS
        #Stops paddle moving too high
        elif paddle.top < LINETHICKNESS:
            paddle.top = LINETHICKNESS
        #Draws paddle
        pygame.draw.rect(self.screen, WHITE, paddle)


    #draws the ball
    def drawBall(self):
        pygame.draw.rect(self.screen, WHITE, self.ball)

    #moves the ball returns new position
    def moveBall(self):
        self.ball.x += self.ballDirX
        self.ball.y += self.ballDirY

    #Checks for a collision with a wall, and 'bounces' ball off it.
    #Returns new direction
    def checkEdgeCollision(self):
        if self.ball.top == (LINETHICKNESS) or self.ball.bottom == (WINDOWHEIGHT - LINETHICKNESS):
            self.ballDirY = self.ballDirY * -1
        if self.ball.left == (LINETHICKNESS) or self.ball.right == (WINDOWWIDTH - LINETHICKNESS):
            self.ballDirX = self.ballDirX * -1

    #Checks is the ball has hit a paddle, and 'bounces' ball off it.
    def checkHitBall(self):
        if self.ballDirX == -1 and self.paddle1.right == self.ball.left and self.paddle1.top+3 < self.ball.top and self.paddle1.bottom+3 > self.ball.bottom:
            return -1
        elif self.ballDirX == 1 and self.paddle2.left == self.ball.right and self.paddle2.top+3 < self.ball.top and self.paddle2.bottom+3 > self.ball.bottom:
            return -1
        else:
            return 1

    #Checks to see if a point has been scored returns new score
    def checkPointScored(self):
        #reset points if left wall is hit
        if self.ball.left == LINETHICKNESS:
            return 0
        #1 point for hitting the ball
        elif self.ballDirX == -1 and self.paddle1.right == self.ball.left and self.paddle1.top+8 < self.ball.top and self.paddle1.bottom+8 > self.ball.bottom:
            self.score += 1
        #5 points for beating the other paddle
        elif self.ball.right == WINDOWWIDTH - LINETHICKNESS:
            self.score += 5
        #if no points scored, return score unchanged
        else:
            pass

    #Artificial Intelligence of computer player
    def artificialIntelligence(self):
        #If ball is moving away from paddle, center bat
        if self.ballDirX == -1:
            if self.paddle2.centery < (WINDOWHEIGHT/2):
                self.paddle2.y += 1
            elif self.paddle2.centery > (WINDOWHEIGHT/2):
                self.paddle2.y -= 1
        #if ball moving towards bat, track its movement.
        elif self.ballDirX == 1:
            if self.paddle2.centery < self.ball.centery:
                self.paddle2.y += 1
            else:
                self.paddle2.y -=1

    #Displays the current score on the screen
    def displayScore(self):
        resultSurf = BASICFONT.render('Score = %s' % self.score, True, WHITE)
        resultRect = resultSurf.get_rect()
        resultRect.topleft = (WINDOWWIDTH - 150, 25)
        self.screen.blit(resultSurf, resultRect)

    #Main function
    def run(self):
        print("pong???")
        print("start game11")
        global pong_start
        self.score = 0
        pygame.init()
        print("start game12")
        ##Font information
        global BASICFONT, BASICFONTSIZE
        # BASICFONTSIZE = 20
        print("start game13")
        # BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
        # BASICFONT = pygame.font.SysFont('comicsansms.ttf', BASICFONTSIZE)
        print("start game2")
        self.FPSCLOCK = pygame.time.Clock()
        print("start game3")
        self.screen = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT), pygame.FULLSCREEN)
        # self.screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        print("start game4")
        pygame.display.set_caption('Pong')
        print("start game5")
        # Initiate variable and set starting positions
        # any future changes made within rectangles
        ballX = WINDOWWIDTH / 2 - LINETHICKNESS / 2
        ballY = WINDOWHEIGHT / 2 - LINETHICKNESS / 2
        playerOnePosition = (WINDOWHEIGHT - PADDLESIZE) / 2
        playerTwoPosition = (WINDOWHEIGHT - PADDLESIZE) / 2
        # print("start game")
        # Keeps track of ball direction
        self.ballDirX = -1  ## -1 = left 1 = right
        self.ballDirY = -1  ## -1 = up 1 = down
        # print("pong???")
        # Creates Rectangles for ball and paddles.
        self.paddle1 = pygame.Rect(PADDLEOFFSET, playerOnePosition, LINETHICKNESS, PADDLESIZE)
        # print("pong???")
        self.paddle2 = pygame.Rect(WINDOWWIDTH - PADDLEOFFSET - LINETHICKNESS, playerTwoPosition, LINETHICKNESS,
                                   PADDLESIZE)
        # print("pong?!!")
        self.ball = pygame.Rect(ballX, ballY, LINETHICKNESS, LINETHICKNESS)
        # print("pong?!!")

        # Draws the starting position of the Arena
        self.drawArena()
        # print("1")
        self.drawPaddle(self.paddle1)
        # print("2")
        self.drawPaddle(self.paddle2)
        # print("3")
        self.drawBall()

        pygame.mouse.set_visible(0)  # make cursor invisible
        # print("pong???")
        # self.ser.timeout = 0

        serialReadThread = Thread(target=self.check_input)
        serialReadThread.daemon = True
        serialReadThread.start()

        self.key_esc_pressed = False
        pong_start = True
        # print("pong!!!")
        while not self.key_esc_pressed: #main game loop

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                # keyboard movement commands
            if self.key_up_pressing:
                self.paddle1.y -= 1
            elif self.key_down_pressing:
                self.paddle1.y += 1

            self.drawArena()
            self.drawPaddle(self.paddle1)
            self.drawPaddle(self.paddle2)
            self.drawBall()

            self.moveBall()
            self.checkEdgeCollision()
            self.checkPointScored()
            self.ballDirX = self.ballDirX * self.checkHitBall()
            self.artificialIntelligence()

            # self.displayScore()

            pygame.display.update()
            self.FPSCLOCK.tick(FPS)
        pong_start = False
        self.screen.fill(pygame.color.Color(0, 0, 0))
        pygame.quit()
        self.key_esc_pressed = False

    def check_input(self):
        while True:
            if self.ser.inWaiting() > 0:
                try:
                    data_str = str(self.ser.readline().decode('UTF-8')).rstrip().lstrip()
                    # print("pong", data_str)

                    if data_str.startswith("PRESS"):
                        str_split = data_str.split(" ")
                        if str_split[1] == "UP":
                            self.key_up_pressing = True
                        elif str_split[1] == "DOWN":
                            self.key_down_pressing = True
                        elif str_split[1] == "ESC":
                            self.key_esc_pressed = True
                            break

                    if data_str.startswith("RELEASE"):
                        str_split = data_str.split(" ")
                        if str_split[1] == "UP":
                            self.key_up_pressing = False
                        elif str_split[1] == "DOWN":
                            self.key_down_pressing = False


                except Exception as e:
                    pass
                    print(e)

            else:
                pass
                # print("b")

def startPong():
    pong = Pong()
    pong.play_PONG()

if __name__ == '__main__':
    startPong()


