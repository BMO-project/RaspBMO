import pygame
from threading import Thread
FPS = 60
Temp_start = False
WINDOWWIDTH = 480
WINDOWHEIGHT = 320

is_running = True

class Temp():
    def __init__(self, ser):
        global is_running
        self.ser = ser
        self.temp = 0
        self.humi = 0
        self.key_esc_pressed = False
        is_running = True

    def setTemp(self, temp, humi):
        self.temp = temp
        self.humi = humi


    def showTemp(self):
        global is_running
        global Temp_start

        pygame.init()

        screen = pygame.display.set_mode((480, 320), pygame.FULLSCREEN)

        pygame.display.set_caption("Key Event")
        clock = pygame.time.Clock()

        Temp_start = True
        pygame.mouse.set_visible(0)  # make cursor invisible
        serialReadThread = Thread(target=self.check_input)
        serialReadThread.daemon = True
        serialReadThread.start()

        while not self.key_esc_pressed:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # esc 누르면 종
                        run = False

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

        Temp_start = False
        screen.fill(pygame.color.Color(0, 0, 0))
        pygame.quit()

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