from machine import FPIOA,UART
import time



fpioa=FPIOA()
fpioa.set_function(11,FPIOA.UART2_TXD)
fpioa.set_function(12,FPIOA.UART2_RXD)



uart=UART(UART.UART2,baudrate=115200, bits=UART.EIGHTBITS, parity=UART.PARITY_NONE, stop=UART.STOPBITS_ONE)

data=0


while True:
    message="Senser data: "+str(data)+"\r\n"
    data+=1
    uart.write(message)
    time.sleep(0.5)

