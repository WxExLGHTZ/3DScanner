import serial
import time

class Arduino():

    def __init__(self, comPort, baudRate, timeout):
        self.comPort = comPort
        self.baudRate = baudRate
        self.timeout = timeout
        self.serPort = serial.Serial(self.comPort, self.baudRate, timeout=self.timeout)
        time.sleep(2)
        self.curstep = 0

#rotationsbefehl an arduino
    def rotieren(self, steps):
        self.steps = steps
        self.neg = int(self.steps < 0)
        if self.neg:
            self.steps = -self.steps
        self.stepsString = str(self.steps)
        self.serPort.write([self.neg])
        for i in range(5 - len(self.stepsString)):
            self.serPort.write([0])
        for i in range(len(self.stepsString)):
            self.serPort.write([int(self.stepsString[i])])

#warten auf ende der rotation
    def warteAufRotation(self):
        while True:
            self.data = str(self.serPort.readline())
            if self.data != "b''":
                self.curstep += self.steps
                if int(str(self.data)[2:len(self.data) - 1]) != self.steps:
                    self.close()
                    raise Exception("The Arduino returned the wrong number of steps!")
                break

#gibt den winkel der ROtation zurück
    def winkel(self):
        self.gearRatio = 6
        self.currentAngle = ((self.curstep * 360) / 2048) / self.gearRatio
        return self.currentAngle

    def close(self):
        self.serPort.close()
