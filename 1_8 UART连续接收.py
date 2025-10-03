from machine import FPIOA,UART
import time



fpioa=FPIOA()
fpioa.set_function(11,FPIOA.UART2_TXD)
fpioa.set_function(12,FPIOA.UART2_RXD)



uart=UART(UART.UART2,baudrate=115200, bits=UART.EIGHTBITS, parity=UART.PARITY_NONE, stop=UART.STOPBITS_ONE)

data=0


while True:
    data=uart.read()
    if data:
        print(data.hex())#data.hex()返回字符串
        uart.write(data)
        print(int(data.hex(),16)*2)
    time.sleep(0.5)

