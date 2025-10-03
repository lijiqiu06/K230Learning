from machine import Pin
from machine import FPIOA
import time

fpioa=FPIOA()
fpioa.set_function(20,FPIOA.GPIO20)
fpioa.set_function(62,FPIOA.GPIO62)
fpioa.set_function(63,FPIOA.GPIO63)

RGB_G=Pin(20,Pin.OUT)
RGB_R=Pin(62,Pin.OUT)
RGB_B=Pin(63,Pin.OUT)

RGB_R.high()
RGB_G.high()
RGB_B.high()

def RGB_Set(r,g,b):
    if r==1:
        RGB_R.low()
    else:
        RGB_R.high()
    if g==1:
        RGB_G.low()
    else:
        RGB_G.high()
    if b==1:
        RGB_B.low()
    else:
        RGB_B.high()

while True:
    RGB_Set(0,0,1)  # blue
    time.sleep(1)
    RGB_Set(0,1,0)  # cyan
    time.sleep(1)
    RGB_Set(0,1,1)  # blue
    time.sleep(1)
    RGB_Set(1,0,0)  # red
    time.sleep(1)
    RGB_Set(1,0,1)  # purple
    time.sleep(1)
    RGB_Set(1,1,0)  # yellow
    time.sleep(1)
    RGB_Set(1,1,1)  # white
    time.sleep(1)
