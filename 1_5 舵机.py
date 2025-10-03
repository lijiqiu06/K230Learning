import time
from machine import PWM, FPIOA

fpioa=FPIOA()
fpioa.set_function(47,FPIOA.PWM3)
pwm=PWM(3,50,0) #50Hz, 0% duty cycle
pwm.enable(1)

pwm.duty(1.5/20*100) #90度
time.sleep(1)
pwm.duty(0.5/20*100) #0度
time.sleep(1)

while True:
    for i in range(0,181,5):
        pwm.duty((0.5+i/180*2)/20*100)
        time.sleep(0.1)
    time.sleep(0.1)
    for i in range(180,-1,-5):
        pwm.duty((0.5+i/180*2)/20*100)
        time.sleep(0.1)
    time.sleep(0.1)

