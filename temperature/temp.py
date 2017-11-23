import pygame

Temp_start = False

class Temp():
    def __init__(self):
        self.temp = 0
        self.humi = 0

    def setTemp(self, temp, humi):
        self.temp = temp
        self.humi = humi

    def showTemp(self):
        global Temp_start

        pygame.init()

        screen = pygame.display.set_mode((500, 300))

        pygame.display.set_caption("Key Event")
        clock = pygame.time.Clock()
        run = True

        text = ""

        Temp_start = True

        while run:
            # pygame.event.get() : 키를 눌렀을때 이벤트
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # esc 누르면 종
                        run = False

            # pygame.key.get_pressed() - 전체 키배열중 현재 눌려져있는 키를 bool형식의 튜플로 반환
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                text = "Left key press..."
            elif keys[pygame.K_RIGHT]:
                text = "Right key press..."
            elif keys[pygame.K_UP]:
                text = "Up key press..."
            elif keys[pygame.K_DOWN]:
                text = "Down key press..."
            else:
                text1 = "Temperature : "+str(self.temp)+"'C"
                text2 = "Humidity    : "+str(self.humi) + "%"

            screen.fill(pygame.color.Color(0, 0, 0))

            # SysFont(폰트명, 폰트크기) - SysFont 객체 생성
            sysfont = pygame.font.SysFont("Monospace", 30, bold=True)

            # render(텍스트, 안티알리아싱여부, 색상) - 텍스트를 그려넣고 Surface 객체 반환
            textrender1 = sysfont.render(text1, True, (0, 150, 0))
            textrender2 = sysfont.render(text2, True, (0, 150, 0))

            # Surface.blit(Surface객체, (x좌표, y좌표)) - 다른 Surface객체를 그려넣음
            screen.blit(textrender1, (30, 45))  # 윈도우에 text1가 있는 Surface객체 그림
            screen.blit(textrender2, (30, 80))  # 윈도우에 text2가 있는 Surface객체 그림

            pygame.display.flip()

            clock.tick(60)

        pygame.quit()