from machine import Pin, Timer,FPIOA
import time

fpioa=FPIOA()
fpioa.set_function(62,FPIOA.GPIO62)
fpioa.set_function(20,FPIOA.GPIO20)
fpioa.set_function(63,FPIOA.GPIO63)

RGB_R=Pin(62,Pin.OUT)
RGB_G=Pin(20,Pin.OUT)
RGB_B=Pin(63,Pin.OUT)

RGB_R.high()
RGB_G.high()
RGB_B.high()


def led_toggle(timer):
    global led_state
    RGB_R.high()
    RGB_G.high()
    RGB_B.high()
    if led_state==0:
        RGB_R.low()
    elif led_state==1:
        RGB_G.low()
    elif led_state==2:
        RGB_B.low()

    led_state=(led_state+1)%3

led_state=0
timer=Timer(-1)
timer.init(mode=Timer.PERIODIC,period=1000,callback=led_toggle)
while True:
    print(led_state)
    time.sleep(0.1)
