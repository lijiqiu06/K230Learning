from machine import FPIOA, PWM
import time

fpioa=FPIOA()
fpioa.set_function(47,FPIOA.PWM3)
pwm=PWM(3,2000,50) # 2kHz, 50% duty cycle

pwm.enable(1) #需要使能

while True:
    a=1
