import constant
import threading
import led
import mobile
import music
import time

#baby status NONE, ASLEEP, SLEEP, AWAKE, WAKE
baby = None

#count if baby is not detected
exist_cnt = 0

#count to check baby's initial status
init_cnt = 0

#baby's initial status
INIT_STATS = None
flag = 0

#baby's status list from camera.py
#OPEN, CLOSE, EMPTY
eye_list = [ None for i in range(30) ]

#previous status
prev = 0

#for threads
thread_state = False
led_thd = None
lamp_thd = None
mobile_thd = None
music_thd = None

########## STATS : 완전히 깬 상태 WAKE, 완전히 잠든 상태 SLEEP, 잠드려고 하는 상태 ASLEEP  ##########
########## global variable !! ##########

#status
STATS = None

class Status:

    global STATS

    def __init__(self):
        self.wlimit = 100
        self.wcnt = 0
        self.slimit = 100
        self.scnt = 0
    
    def wakecounter(self):
        self.wcnt += 1
        STATS = 'WCHECK'
        if self.wcnt == self.wlimit:
            self.wcnt = 0
            self.wake() # GPIO 가동 up
           
    def sleepcounter(self):
        self.scnt += 1
        STATS = 'SCHECK'
        if self.scnt == self.slimit:
            self.scnt = 0
            self.sleep()# GPIO stop

    def asleep(self):
        STATS = 'ASLEEP'
        # GPIO 가동 down

    def wake(self):
        STATS = 'WAKE'

    def sleep(self):
        STATS = 'SLEEP'

s = Status()

def rateCalculator(): #opening eyes rate calculator
    global eye_list
    
    rate = 0

    count0 = eye_list.count(constant.OPEN) #open
    count1 = eye_list.count(constant.CLOSE) #close
    
    
    if count0 != 0 or count1 != 0:
        rate = count0/(count0 + count1)
        
    print("open", count0, "close", count1, "rate", rate)
    
    return rate

def eyeController():
    
    global baby
    global INIT_STATS # baby status when count 10
    global eye_list
    global init_cnt, exist_cnt
    global prev
    global STATS
    global flag
    
    count0 = eye_list.count(constant.OPEN) #open
    count1 = eye_list.count(constant.CLOSE) #close
    
    if count0 != 0 and count1 != 0:
        if INIT_STATS != 'NONE':
            INIT_STATS = baby
        flag = 1
    
    rate = rateCalculator()
    
    # print("rate", rate, "init stats", INIT_STATS)
    print("eye list: ", eye_list)
    if(eye_list[len(eye_list)-1] == constant.EMPTY and flag == 0): #baby detection failed
        print("rate", rate, "init stats", INIT_STATS, "baby isn't detected")
        exist_cnt = exist_cnt + 1
        if exist_cnt == 10:
            STATS = 'EXIT'
            baby = constant.NONE
            exist_cnt = 0
    else: #baby detected:
        if rate >= 0.85:
            print("rate", rate, "init stats", INIT_STATS,"baby is waken")
            baby = constant.WAKE
            INIT_STATS = constant.WAKE
            s.wakecounter()
            prev = 1
        elif rate >= 0.1:
            if INIT_STATS == constant.SLEEP:
                print("rate", rate, "init stats", INIT_STATS,"baby is awaked!!")
                baby = constant.AWAKE
                if STATS == "SCHECK":
                    s.scnt = 0 # SLEEP 임계값 체크 중인데 AWAKE라면 cnt 초기화

            elif INIT_STATS == constant.WAKE:
                print("rate", rate, "init stats", INIT_STATS,"baby is falling asleep")
                baby = constant.ASLEEP
                if prev == 1:
                    s.asleep() # 졸린 첫 순간, 순차적으로 GPIO 가동
                if STATS == "WCHECK":
                    s.wcnt = 0 # WAKE 임계값 체크 중인데 ASLEEP라면 cnt 초기화

        else:
            print("rate", rate, "init stats", INIT_STATS, "baby is sleeping")
            baby = constant.SLEEP    
            INIT_STATS = constant.SLEEP  
            s.sleepcounter()

def statusController():

    global STATS
    
    
    if STATS == 'WAKE':
        # print("WAKE")
        # 애기 완전히 깸. GPIO UP
        
        if(thread_state == False):
            if(mobile_thd == None):
                    mobile_thd = threading.Thread(target=mobile.main)
                    mobile_thd.start() 
                    mobile.mobile_state = True 
            
            if(led_thd == None):
                    led_thd = threading.Thread(target=led.randomLight)
                    led_thd.start()
                    led.power = True
            
            if(music_thd == None):
                    music_thd = threading.Thread(target=music.playMusic)
                    music_thd.start()
                    music.music = "a"
                    music.music_state = True 
            
            if(lamp_thd == None):
                    lamp_thd = threading.Thread(target=led.lampLightOn)
                    lamp_thd.start()
                    led.lamp_power = True 
            thread_state = True
    
    if STATS == 'SLEEP':
        # print("SLEEP")
        # 애기 완전히 잠들었음. GPIO stop
        
        if(thread_state == True):
            joinGpioThread()

    if STATS == 'ASLEEP':
        # print("ASLEEP")
        
        if(music_thd == None):
            music_thd = threading.Thread(target=music.playMusic)
            music_thd.start()
            music.music = "b"
            music.music_state = True 
        
        if(lamp_thd != None):
            led.lightOff()
            
        # 애기 잠드려고 함. GPIO DOWN
        


def makeThread(thd):
    global led_thd,lamp_thd, mobile_thd, music_thd
    
    if(thd == "led"):
        led_thd = threading.Thread(target=led.randomLight) 
        led.power = True
        led_thd.start()
    
    elif(thd == "lamp"):
        lamp_thd = threading.Thread(target=led.lampLightOn)
        led.lamp_power = True
        lamp_thd.start()
     
    elif(thd == "mobile"):
        mobile_thd = threading.Thread(target=mobile.main) 
        mobile.mobile_state = True
        mobile_thd.start()

    elif(thd == "music"):
        music_thd = threading.Thread(target=music.playMusic)
        music.music_state = True
        # print(">>>>>>>>>>music state")
        music_thd.start()
        
        

def joinThread(thd):
    global led_thd,lamp_thd, mobile_thd, music_thd
    print(f"join {thd}")
    
    if(thd == "led" and led_thd != None):
        led.power = False
        led_thd.join()
        led_thd = None
    
    elif(thd == "lamp" and lamp_thd != None):
        led.lamp_power = False
        lamp_thd.join()
        lamp_thd = None
        
    elif(thd == "mobile" and mobile_thd != None):
        mobile.mobile_state = False
        mobile_thd.join()
        mobile_thd = None
        
    elif(thd == "music" and music_thd != None):
        music.music_state = False
        music_thd.join()
        music_thd = None

def joinGpioThread():    
    print(">>>>>>>>>>>>>>joinGpioThread")
    global led_thd,lamp_thd, mobile_thd, music_thd
    
    if(led_thd != None):
        led.power = False
        led_thd.join()
        led_thd = None
    
    if(lamp_thd != None):
        led.lamp_power = False
        lamp_thd.join()
        lamp_thd = None
    
    if(mobile_thd != None):
        mobile.mobile_state = False
        mobile_thd.join()
        mobile_thd = None
    
    if(music_thd != None):
        music.music_state = False
        music_thd.join() 
        music_thd = None 
        
    return 

def main():
    print("baby main ok")
    global baby, thread_state
    global led_thd, lamp_thd, mobile_thd, music_thd
    while(1):
        try:
            eyeController()
            statusController()
            
            
            print()
            
            if(led_thd == None and lamp_thd == None and mobile_thd == None and music_thd == None):
                thread_state = False
                
            if(thread_state==True and baby==constant.NONE):
                print("Enter join gpio thread")
                thread_state = False
                joinGpioThread()
            
                
        except KeyboardInterrupt:
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>.baby interrupt")
            joinGpioThread()
            
            
if __name__ == "__main__":
    main()