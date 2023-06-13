from machine import Pin
from neopixel import NeoPixel
import random

PIXEL_COUNT = 24
BRIGHTNESS = 8  # 亮度取值范围[0,255]
pin = Pin(16, Pin.OUT)  # set GPIO16(Wemos S2 Mini) to output to drive NeoPixels
np = NeoPixel(pin, PIXEL_COUNT)  # create NeoPixel driver on GPIO0 for 8 pixels

for i in range(PIXEL_COUNT):
    np[i] = (int(random.random() * BRIGHTNESS), int(random.random() * BRIGHTNESS), int(random.random() * BRIGHTNESS))
np.write()  # write data to all pixels
# r, g, b = np[0]         # get first pixel colour


# from apa106 import APA106
#
# pin = Pin(16, Pin.OUT)
# ap = APA106(pin, 8)
# ap[0] = (255, 255, 255)
# # r, g, b = ap[0]
# ap.write()
