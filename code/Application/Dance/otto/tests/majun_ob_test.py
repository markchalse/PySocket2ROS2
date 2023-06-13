from rklib.HCSR04 import HCSR04
from machine import Pin
import time
trig = Pin(5, Pin.OUT)
echo = Pin(18, Pin.IN)
HC = HCSR04(trig, echo)
ts = time.ticks_us()  # 上一次获取超声波时间
 
def modeHCSR():
    global ts
    te = time.ticks_us()  # 当前时间
    tc = te - ts
    if tc > 1000000:  #1秒内不重新检测
        ts = te
        distance = HC.getDistance()
        print("distance",distance)
        if distance < 5: #<5cm, 后退一步
            print("<5cm, 后退一步")
            Otto.walk(1, int(1000), int(-1))