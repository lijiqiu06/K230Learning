# 按一下长亮按一下长一下灭
from machine import FPIOA
from machine import Pin
import time

prebuttontime=0
button_state=0
def Key_Init():
    fpioa=FPIOA()
    fpioa.set_function(53,FPIOA.GPIO53)
    UserKey=Pin(53,Pin.IN,pull=Pin.PULL_DOWN)
    return UserKey

def Key_Scan(UserKey):
    global prebuttontime, button_state
    debounce = 20  # 消抖时间20ms
    cur = UserKey.value()
    now = time.ticks_ms()

    # 情况1：第一次检测到按下 → 记录时间，进入“等待确认”状态
    if cur == 1 and button_state == 0:
        prebuttontime = now
        button_state = 1

    # 情况2：持续按住，并且超过消抖时间 → 确认按下，返回1
    elif cur == 1 and button_state == 1:
        if time.ticks_diff(now, prebuttontime) > debounce:
            button_state = 2
            return 1

    # 情况3：松开按键 → 状态归零
    elif cur == 0:
        button_state = 0

    return 0



fpioa=FPIOA()
fpioa.set_function(20,FPIOA.GPIO20)
fpioa.set_function(62,FPIOA.GPIO62)
fpioa.set_function(63,FPIOA.GPIO63)
fpioa.set_function(53,FPIOA.GPIO53)

UserKey=Key_Init

RGB_B=Pin(20,Pin.OUT)
RGB_R=Pin(62,Pin.OUT)
RGB_G=Pin(63,Pin.OUT)
UserKey=Pin(53,Pin.IN,pull=Pin.PULL_DOWN)

RGB_B.high()
RGB_R.high()
RGB_G.high()

while True:
    if Key_Scan(UserKey):
        if RGB_R.value()==1:
            RGB_R.low()
        else:
            RGB_R.high()
