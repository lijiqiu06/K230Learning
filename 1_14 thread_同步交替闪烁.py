import _thread
import time
from machine import FPIOA,Pin

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

lock = _thread.allocate_lock()
led_state=0

def LED_G():
    global led_state
    while True:
        lock.acquire()
        try:
            if led_state==1:
                led_state=0
                RGB_G.low()
                RGB_B.high()
                print("LED_G",led_state)
                time.sleep(0.5)
               
        finally:
            lock.release()
        time.sleep(0.01)

def LED_B():
    global led_state
    while True:
        lock.acquire()
        try:
            if led_state==0:
                led_state=1
                RGB_B.low()
                RGB_G.high()
                print("LED_B",led_state)
                time.sleep(0.5)
               
        finally:
            lock.release()
        time.sleep(0.01)

_thread.start_new_thread(LED_G, ())
_thread.start_new_thread(LED_B, ())

while True:
    time.sleep(1)