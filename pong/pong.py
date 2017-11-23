import pygame, sys
from pygame.locals import *

# Number of frames per second
# Change this value to speed up or slow down your game
FPS = 500

#Global Variables to be used through our program

WINDOWWIDTH = 400
WINDOWHEIGHT = 300
LINETHICKNESS = 10
PADDLESIZE = 50
PADDLEOFFSET = 20

# Set up the colours
BLACK     = (0  ,0  ,0  )
WHITE     = (255,255,255)

pong_start = False

class Pong():
    def __init__(self):
        pass

    #Draws the arena the game will be played in.
    def drawArena(self):
        DISPLAYSURF.fill((0,0,0))
        #Draw outline of arena
        pygame.draw.rect(DISPLAYSURF, WHITE, ((0, 0), (WINDOWWIDTH, WINDOWHEIGHT)), LINETHICKNESS*2)
        #Draw centre line
        pygame.draw.line(DISPLAYSURF, WHITE, (int((WINDOWWIDTH/2)), 0), (int((WINDOWWIDTH/2)), WINDOWHEIGHT), int((LINETHICKNESS/4)))


    #Draws the paddle
    def drawPaddle(self, paddle):
        #Stops paddle moving too low
        if paddle.bottom > WINDOWHEIGHT - LINETHICKNESS:
            paddle.bottom = WINDOWHEIGHT - LINETHICKNESS
        #Stops paddle moving too high
        elif paddle.top < LINETHICKNESS:
            paddle.top = LINETHICKNESS
        #Draws paddle
        pygame.draw.rect(DISPLAYSURF, WHITE, paddle)


    #draws the ball
    def drawBall(self):
        pygame.draw.rect(DISPLAYSURF, WHITE, self.ball)

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
        else: return 1

    #Checks to see if a point has been scored returns new score
    def checkPointScored(self):
        #reset points if left wall is hit
        if self.ball.left == LINETHICKNESS:
            return 0
        #1 point for hitting the ball
        elif self.ballDirX == -1 and self.paddle1.right == self.ball.left and self.paddle1.top < self.ball.top and self.paddle1.bottom > self.ball.bottom:
            self.score += 1
        #5 points for beating the other paddle
        elif self.ball.right == WINDOWWIDTH - LINETHICKNESS:
            self.score += 5
        #if no points scored, return score unchanged
        else: pass

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
        resultSurf = BASICFONT.render('Score = %s' %self.score, True, WHITE)
        resultRect = resultSurf.get_rect()
        resultRect.topleft = (WINDOWWIDTH - 150, 25)
        DISPLAYSURF.blit(resultSurf, resultRect)

    #Main function
    def play_PONG(self):
        self.score = 0
        pygame.init()
        global DISPLAYSURF
        ##Font information
        global BASICFONT, BASICFONTSIZE
        BASICFONTSIZE = 20
        BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

        self.FPSCLOCK = pygame.time.Clock()
        # DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT), pygame.FULLSCREEN)
        DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        pygame.display.set_caption('Pong')

        # Initiate variable and set starting positions
        # any future changes made within rectangles
        ballX = WINDOWWIDTH / 2 - LINETHICKNESS / 2
        ballY = WINDOWHEIGHT / 2 - LINETHICKNESS / 2
        playerOnePosition = (WINDOWHEIGHT - PADDLESIZE) / 2
        playerTwoPosition = (WINDOWHEIGHT - PADDLESIZE) / 2

        # Keeps track of ball direction
        self.ballDirX = -1  ## -1 = left 1 = right
        self.ballDirY = -1  ## -1 = up 1 = down

        # Creates Rectangles for ball and paddles.
        self.paddle1 = pygame.Rect(PADDLEOFFSET, playerOnePosition, LINETHICKNESS, PADDLESIZE)
        self.paddle2 = pygame.Rect(WINDOWWIDTH - PADDLEOFFSET - LINETHICKNESS, playerTwoPosition, LINETHICKNESS,
                                   PADDLESIZE)
        self.ball = pygame.Rect(ballX, ballY, LINETHICKNESS, LINETHICKNESS)

        # Draws the starting position of the Arena
        self.drawArena()
        self.drawPaddle(self.paddle1)
        self.drawPaddle(self.paddle2)
        self.drawBall()

        pygame.mouse.set_visible(0)  # make cursor invisible

        global pong_start
        while True: #main game loop
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                # keyboard movement commands
            if pygame.key.get_pressed()[pygame.K_UP] != 0:
                self.paddle1.y -= 1
            elif pygame.key.get_pressed()[pygame.K_DOWN] != 0:
                self.paddle1.y += 1

            if (pygame.key.get_pressed()[pygame.K_ESCAPE] != 0 or
                pygame.key.get_pressed()[pygame.K_BACKSPACE] != 0):
                pong_start = False
                #pygame.quit()
                #sys.exit()
                break

            self.drawArena()
            self.drawPaddle(self.paddle1)
            self.drawPaddle(self.paddle2)
            self.drawBall()

            self.moveBall()
            self.checkEdgeCollision()
            self.checkPointScored()
            self.ballDirX = self.ballDirX * self.checkHitBall()
            self.artificialIntelligence()

            self.displayScore()

            pygame.display.update()
            self.FPSCLOCK.tick(FPS)

            pong_start = True
            
def startPong():
    pong = Pong()
    pong.play_PONG()

if __name__ == '__main__':
    startPong()


