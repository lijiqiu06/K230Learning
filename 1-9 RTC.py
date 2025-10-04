from machine import FPIOA,Pin,RTC
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

rtc=RTC()

rtc.init((2025,10,4,6,23,17,0,0))
print("RTC 初始化完成 当前时间是：",rtc.datetime())

target_hour=23
target_min=25

def trigger_event():
    RGB_G.low()

def check_time():
    current_time=rtc.datetime()
    print("当前时间是：",current_time,"\n")

    if current_time[4]==target_hour and current_time[5]==target_min:
        trigger_event()

while True:
    check_time()
    time.sleep(0.5)

