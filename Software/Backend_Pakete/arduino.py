import serial
import time

class Arduino():

    def __init__(self, comPort, baudRate, timeout):
        self.comPort = comPort
        self.baudRate = baudRate
        self.timeout = timeout
        self.totalAngle = 0
        self.s = serial.Serial(self.comPort, self.baudRate, timeout=self.timeout)
        time.sleep(2)
        self.currentstep = 0

    def rotate(self, steps):
        self.steps = steps
        self.negative = int(self.steps < 0)
        if self.negative:
            self.steps = -self.steps
        self.stepsAsString = str(self.steps)
        self.s.write([self.negative])
        for i in range(5 - len(self.stepsAsString)):
            self.s.write([0])
        for i in range(len(self.stepsAsString)):
            self.s.write([int(self.stepsAsString[i])])

    def waitForRotation(self):
        while True:
            self.data = str(self.s.readline())
            if self.data != "b''":
                self.currentstep += self.steps
                if int(str(self.data)[2:len(self.data) - 1]) != self.steps:
                    self.close()
                    raise Exception("The Arduino returned the wrong number of steps!")
                break

    def giveAngle(self):
        self.gearRatio = 6
        self.currentAngle = ((self.currentstep * 360) / 2048) / self.gearRatio
        return self.currentAngle

    def close(self):
        self.s.close()
