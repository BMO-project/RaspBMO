import serial
import time
import multiprocessing

from pong.pong import Pong as Pong
from pong.pong import pong_start as Pong_start

from temperature.temp import Temp as Temp
from temperature.temp import Temp_start as Temp_start

from face.face import Face
from face.face import Face_start

class BMOBrain():
    def __init__(self):
        self.ser = serial.Serial()
        self.pong = None
        self.temp = None
        self.face = None

    def start(self):
        main_loop = multiprocessing.Process(self.run_loop())
        main_loop.start()

    def run_loop(self):
        self.ser.port = '/dev/cu.usbmodem1421'
        self.ser.baudrate = 9600
        self.ser.timeout = 1
        self.ser.open()
        print("BMO-project v0.1 start!")
        spam_checker = False
        self.face = Face(self.ser)
        while True:
            if self.ser.inWaiting() > 0:
                try:
                    data_str = str(self.ser.readline().decode('UTF-8').lstrip().rstrip())
                    print("main", data_str)

                    if data_str.startswith("OPEN") and (not spam_checker):
                        msg_arr = data_str.split(" ")
                        if msg_arr[1] == "PONG":  # Play pong game
                            if not Pong_start:
                                self.pong = None
                                self.pong = Pong(self.ser)
                                self.pong.run()
                                # time.sleep(1)
                            pass
                        elif msg_arr[1] == "TEMP":  # Show temperature
                            if not Temp_start:
                                self.temp = Temp(self.ser)
                                self.temp.setTemp(32.6, 45)
                                self.temp.showTemp()
                                time.sleep(1)
                            pass
                        elif msg_arr[1] == "FACE":  # Show face
                            if not Face_start:
                                self.face.showFaces()
                                # time.sleep(1)
                            pass
                        else:
                            pass
                    elif data_str.startswith("PRESS"):
                        str_split = data_str.split(" ")
                        if str_split[1] == "UP":
                            self.face.showFaces()
                        elif str_split[1] == "DOWN":
                            self.face.showFaces()
                    else:
                        spam_checker = False
                except:
                    pass
            else:
                continue


if __name__ == '__main__':
    brain = BMOBrain()
    brain.start()
