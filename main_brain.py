import serial
import threading
from multiprocessing import Pool
import _thread
import multiprocessing

from pong.pong import Pong as Pong
from pong.pong import pong_start as Pong_start

from temperature.temp import Temp as Temp
from temperature.temp import Temp_start as Temp_start

from face.face import Face
from face.face import Face_start
from face.face import showFaces

class BMOBrain():
    def __init__(self):
        self.ser = serial.Serial()
        self.pong = None
        self.temp = Temp()
        self.face = Face()

    def start(self):
        main_loop = multiprocessing.Process(self.run_loop())
        main_loop.start()

    def run_loop(self):
        self.ser.port = '/dev/cu.usbmodem1421'
        self.ser.baudrate = 9600
        # self.ser.timeout = 0
        self.ser.open()
        print("BMO-project v0.1 start!")
        spam_checker = False

        while (True):
            if self.ser.inWaiting() > 0:
                try:
                    data_str = str(self.ser.readline().decode('UTF-8').lstrip().rstrip())
                    print(data_str)
                    if data_str.startswith("OPEN") and (not spam_checker):
                        msg_arr = data_str.split(" ")
                        if msg_arr[1] == "PONG":  # Play pong game
                            if not Pong_start and not spam_checker:
                                self.pong = Pong(self.ser)
                                self.pong.run()
                            pass
                        elif msg_arr[1] == "TEMP":  # Show temperature
                            spam_checker = True

                            if not Temp_start:
                                self.temp.setTemp(32.6, 45)
                                self.temp.showTemp()
                            pass
                        elif msg_arr[1] == "FACE":  # Show face
                            spam_checker = True

                            if not Face_start:
                                showFaces()
                            pass
                        else:
                            pass
                    else:
                        spam_checker = False
                except:
                    pass
            else:
                continue
if __name__ == '__main__':
    brain = BMOBrain()
    brain.start()
