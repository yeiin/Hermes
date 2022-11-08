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
LAMP = 26

light_list = [LED1, LED2]

GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)
GPIO.setup(LAMP, GPIO.OUT)

pwm3 = GPIO.PWM(LAMP, 50)
pwm3.start(0)

lamp_dc = 0
power = False
lamp_power = False

#pwm lamp on
def lampLightOn(): 
    global lamp_power, lamp_dc
    lamp_power = True

    lamp_dc = 0
    pwm3.ChangeDutyCycle(lamp_dc)
    
    while lamp_power:
        if(lamp_dc<=90):
            lamp_dc += 10
            pwm3.ChangeDutyCycle(lamp_dc)
        time.sleep(2)
    return

#lamp off
def lampOff():
    GPIO.output(LAMP, GPIO.LOW)
    return

#pwm lamp off
def lampLightOff():
    global lamp_dc, lamp_power
    
    while lamp_dc:
        lamp_dc-=10
        pwm3.ChangeDutyCycle(lamp_dc)
        time.sleep(2)
    
    lamp_power = False
    return
        

def randomLight():
    global dc, power
    power = True
    while power:
        light = random.choice(light_list)
        dc = 100
        if(light==LED1):
            GPIO.output(LED1, GPIO.HIGH)
            time.sleep(1)
            dc = 0
            GPIO.output(LED1, GPIO.LOW)
        elif(light==LED2):
            GPIO.output(LED2, GPIO.HIGH) 
            time.sleep(1)
            dc = 0
            GPIO.output(LED2, GPIO.LOW)

