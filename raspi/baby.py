import constant
import threading
import led
import mobile
import audio
import time

#baby status NONE, ASLEEP, SLEEP, AWAKE, WAKE
baby = None

#count if baby is not detected
exist_cnt = 0

#count to check baby's initial status
init_cnt = 0
flag = 0

#baby's initial status
INIT_STATS = None

#baby's status list from camera.py
#OPEN, CLOSE, EMPTY
eye_list = [ None for i in range(30) ]

#for threads
state = False
camerat = None
mobilet = None
audiot = None

def rateCalculator(): #opening eyes rate calculator
    
    global eye_list
    
    rate = 0

    count0 = eye_list.count(constant.OPEN) #open
    count1 = eye_list.count(constant.CLOSE) #close
    print(count0, count1)
    
    if count0 != 0 and count1 != 0:
        rate = count0/(count0 + count1)
    
    return rate

def eyeController():
    
    global baby
    global INIT_STATS # baby status when count 10
    global eye_list
    global init_cnt, exist_cnt
    global flag
    
    count0 = eye_list.count(constant.OPEN) #open
    count1 = eye_list.count(constant.CLOSE) #close
    
    if count0 != 0 and count1 != 0 and flag == 0:
        INIT_STATS = baby
        flag = 1
    
    rate = rateCalculator()
    
    print("rate", rate)
    print(INIT_STATS)
    

    if(eye_list[len(eye_list)-1] == constant.EMPTY): #baby detection failed
        print("baby isn't detected")
        exist_cnt = exist_cnt + 1
        if exist_cnt == 10:
            baby = constant.NONE
            exist_cnt = 0
    else: #baby detected
        print("baby is detected")
        if rate >= 0.85:
            print("baby is waken")
            baby = constant.WAKE
        elif rate >= 0.1:
            if INIT_STATS == constant.SLEEP:
                print("baby is awaked!!")
                baby = constant.AWAKE
            elif INIT_STATS == constant.AWAKE:
                print("baby is falling asleep")
                baby = constant.ASLEEP
        else:
            print("baby is sleeping")
            baby = constant.SLEEP        

def main():
    print("baby main ok")
    global baby, state
    global camerat, mobilet, audiot
    while(1):
        try:
            eyeController()
            if(baby==constant.AWAKE or baby== constant.WAKE and state == False):
                print("make gpio thread")
                ledt = threading.Thread(target=led.main)
                mobilet = threading.Thread(target=mobile.main)
                audiot = threading.Thread(target=audio.playMusic)
                state = True
                ledt.start()
                mobilet.start()
                audiot.start()
                print(f"ledt is {ledt}, mobilet is {mobilet} audiot = {audiot}")
                baby=constant.WAKE
                
            if(state==True and baby==constant.NONE):
                print("Enter join gpio thread")
                state = False
                joinGpioThread(ledt, mobilet, audiot)
        except KeyboardInterrupt:
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>.baby interrupt")
            joinGpioThread(ledt, mobilet, audiot)
            

def joinGpioThread(ledt, mobilet, audiot):    
    print(">>>>>>>>>>>>>>joinGpioThread")
    led.power = False
    ledt.join()
    mobilet.join()
    audio.end = True
    audiot.join() 
    return 
            
if __name__ == "__main__":
    main()