from machine import FPIOA,UART,Pin
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
fpioa.set_function(11,FPIOA.UART2_TXD)
fpioa.set_function(12,FPIOA.UART2_RXD)
fpioa.set_function(53,FPIOA.GPIO53)

UserKey=Key_Init()
uart=UART(UART.UART2,baudrate=115200, bits=UART.EIGHTBITS, parity=UART.PARITY_NONE, stop=UART.STOPBITS_ONE)
string="Hello World!\r\n"
data=bytes([0x01,0x02,0x03])

flag=0
while True:
    if Key_Scan(UserKey)==1 :
        if flag:
            uart.write(string)

        else:
            uart.write(data)

        print(flag)
        flag=not flag
    uart.write('a')
uart.deinit()
