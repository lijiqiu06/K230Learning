from machine import FPIOA, PWM
import time

fpioa=FPIOA()
fpioa.set_function(43,FPIOA.PWM1)
pwm=PWM(1,4000,50) # 4kHz, 50% duty cycle
pwm.enable(1)

while True:
    pwm.enable(1)
    time.sleep(1)
    pwm.enable(0)
    time.sleep(1)
