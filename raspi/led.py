import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import RPi.GPIO as GPIO
import time
import random
import constant 

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

LED1 = 21 # BCM P21
LED2 = 20

light_list = [LED1, LED2]

GPIO.setup(LED1, GPIO.OUT)
print("HELLO")
GPIO.setup(LED2, GPIO.OUT)
print("h")
pwm1 = GPIO.PWM(LED1,50) #50hz  
pwm2 = GPIO.PWM(LED2,50) #50hz  
print("!!")
pwm1.start(0)  
pwm2.start(0)  

dc = 0
power = False

print("--")

def lightOn(light):
    global dc, power
    dc = 100
    power = True
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    if(light==LED1):
        pwm1.ChangeDutyCycle(dc)
    elif(light==LED2):
        pwm2.ChangeDutyCycle(dc)
    


def lightOff(light):
    global dc, power
    dc = 0
    power = False
    GPIO.output(light, GPIO.LOW)


def lighting():
    global dc
    global power
    
    
    while power:                        # 무한 반복 - LED On/Off
        light = random.choice(light_list)
        
        GPIO.output(light, GPIO.HIGH) 
        dc = 100
        time.sleep(0.5)

        GPIO.output(light, GPIO.LOW)
        dc = 0
        time.sleep(0.5)
    
    print("finish")

def changDutyCycle(mode):
    global dc
    if(mode == 0):   
        dc -= 5
        pwm1.ChangeDutyCycle(dc)
        pwm2.ChangeDutyCycle(dc)
    else:
        dc += 5
        pwm1.ChangeDutyCycle(dc)
        pwm2.ChangeDutyCycle(dc)

def main():
    global power
    power = True
    print("light 1 on")
    lightOn(LED1)
    # if(baby.state == True):
    #     lighting()
        # while power:
        #     while(dc>=5):
        #         changDutyCycle(0)
        #         time.sleep(5)
        #     while(dc<=95):
        #         changDutyCycle(1)
        #         time.sleep(5)

if __name__ == "__main__":
	main() 

print("WOW")