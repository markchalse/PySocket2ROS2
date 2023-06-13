from time import sleep_us, ticks_us


class HCSR04():
    def __init__(self, trig, echo):
        self.trig = trig
        self.echo = echo

    def getDistance(self):
        distance = 0
        self.trig.value(1)
        sleep_us(20)
        self.trig.value(0)
        while self.echo.value() == 0:
            pass
        if self.echo.value() == 1:
            ts = ticks_us()  # 开始时间
            while self.echo.value() == 1:
                pass
            te = ticks_us()  # 时间结束
            tc = te - ts
            distance = tc * 0.017  # 距离计算（单位： cm）
        return distance


from machine import Pin
import time

trig = Pin(5, Pin.OUT)
echo = Pin(18, Pin.IN)
HC = HCSR04(trig, echo)

def printDistance():
    i = 0
    for i in range(200):
        distance = HC.getDistance()
        print(str(distance) + ' cm')
        time.sleep(2)
        i += 1


