import constant
import threading
import led
import mobile
import audio
import time


baby = None
before = None
state = False
eye_list = [ None for i in range(100) ]
close_counter = 0
wake_counter = 0
camerat = None
mobilet = None
audiot = None


def eyeController():
    global baby,before
    global close_counter,wake_counter
    global eye_list
    
    count0 = eye_list.count(constant.OPEN) #open
    count1 = eye_list.count(constant.CLOSE) #close
    
    print("open baby", count0)
    print("close baby", count1)
    
    if(eye_list.count(constant.EMPTY)>=80):
        baby = constant.NONE
        wake_counter = 0
        close_counter = 0
    else:
        if(baby == constant.ASLEEP and count1>=70):
            baby = constant.SLEEP
            wake_counter = 0
            
        elif(baby == constant.AWAKE and count0>=70 and wake_counter>=1000):
            baby = constant.WAKE
            
        elif(baby != constant.WAKE and count0 >= 5):
            baby = constant.AWAKE
            wake_counter += 1
            close_counter = 0
            
        elif(baby != constant.SLEEP and close_counter>=10 and count0>=60):
            baby = constant.ASLEEP
            wake_counter = 0
            
        elif(eye_list[50:].count(constant.CLOSE)>=35 and eye_list[50:].count(constant.EMPTY)<=10):
            close_counter += 1
    if(baby != before):
        print(f"baby is {baby} before {before}")
        before = baby
    

    
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