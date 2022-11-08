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
eye_list = [ None for i in range(100) ]

wlimit = 100
wcnt = 0
slimit = 100
scnt = 0

#previous status
prev = 0

#for threads
thread_state = False
led_thd = None
lamp_thd = None
mobile_thd = None
music_thd = None

mobile_flag = False
led_flag = False
music_flag= False


temp = None

########## STATS : 완전히 깬 상태 WAKE, 완전히 잠든 상태 SLEEP, 잠드려고 하는 상태 ASLEEP  ##########
########## global variable !! ##########

#status
STATS = None

def asleep():
    STATS = constant.ASLEEP
    # GPIO 가동 down

def wake():
    global STATS
    STATS = constant.WAKE

def sleep():
    global STATS
    # STATS = constant.SLEEP
    STATS = constant.SLEEP

def wakecounter():
    global wcnt
    global wlimit
    global STATS
    wcnt += 1
    STATS = constant.WCHECK
    if wcnt == wlimit:
        wcnt = 0
        wake() # GPIO 가동 up
           
def sleepcounter():
    global scnt
    global slimit
    global STATS
    scnt += 1
    STATS = constant.SCHECK
    if scnt == slimit:
        scnt = 0
        sleep()# GPIO stop

def rateCalculator(): #opening eyes rate calculator
    global eye_list
    
    rate = 0

    count0 = eye_list.count(constant.OPEN) #open
    count1 = eye_list.count(constant.CLOSE) #close
      
    if count0 != 0 or count1 != 0:
        rate = count0/(count0 + count1)
        
    return rate

def eyeController():
    
    global baby
    global INIT_STATS # baby status when count 10
    global eye_list
    global init_cnt, exist_cnt
    global prev
    global STATS
    global flag
    global scnt, wcnt
    global slimit, wlimit

    count0 = eye_list.count(constant.OPEN) #open
    count1 = eye_list.count(constant.CLOSE) #close
    
    if count0 != 0 and count1 != 0:
        if baby == constant.WAKE or baby == constant.SLEEP:
            if INIT_STATS != constant.NONE:
                INIT_STATS = baby
            flag = 1
    
    rate = rateCalculator()
    
    if(eye_list[len(eye_list)-1] == constant.EMPTY and flag == 0): #baby detection failed
        exist_cnt = exist_cnt + 1
        if exist_cnt == 10:
            STATS = constant.NONE
            baby = constant.NONE
            exist_cnt = 0
    else: #baby detected:
        if eye_list.count(constant.EMPTY) == 15:
            STATS = constant.NONE
            baby = constant.NONE
        if rate >= 0.8:
            baby = constant.WAKE
            INIT_STATS = constant.WAKE
            wakecounter()
            prev = 1
        elif rate >= 0.4: #0.2 
            if INIT_STATS == constant.SLEEP:
                baby = constant.AWAKE
                STATS = baby
                if STATS == constant.SCHECK:
                    scnt = 0 # SLEEP 임계값 체크 중인데 AWAKE라면 cnt 초기화

            elif INIT_STATS == constant.WAKE:
                baby = constant.ASLEEP
                if prev == 1:
                    asleep() # 졸린 첫 순간, 순차적으로 GPIO 가동
                if STATS == constant.WCHECK:
                    wcnt = 0 # WAKE 임계값 체크 중인데 ASLEEP라면 cnt 초기화
        else:
            baby = constant.SLEEP    
            INIT_STATS = constant.SLEEP  
            sleepcounter()

def statusController():

    global STATS, thread_state, mobile_thd, led_thd, music_thd, lamp_thd, temp
    global mobile_flag, music_flag, led_flag

    if STATS == constant.WAKE:
        
        if(mobile_thd == None and mobile_flag == False):
            makeThread("mobile")
        
        if(led_thd == None and led_flag == False):
            makeThread("led")
        
        if(music_thd == None and music_flag == False):
            music.music = "a"
            makeThread("music")
        
        if(lamp_thd == None):
            makeThread("lamp")
    
    
    if STATS == constant.SLEEP:
        if(thread_state == True):
            joinGpioThread()


    if STATS == constant.AWAKE:
        mobile_flag = False
        music_flag = False
        led_flag = False

        
    if baby == constant.ASLEEP:
        mobile_flag = False
        music_flag = False
        led_flag = False
        
        if(music_thd != None):
            joinThread("music")
             
        if(led_thd != None):
            led.power = False
            led_thd.join() 
        
        if(lamp_thd != None):
            led.lamp_power = False
            led.lampLightOff()
            lamp_thd.join()



def makeThread(thd):
    global led_thd,lamp_thd, mobile_thd, music_thd
    
        
    if(thd == "led" and led_thd == None):
        led_thd = threading.Thread(target=led.randomLight) 
        led.power = True
        led_thd.start()
    
    elif(thd == "lamp" and lamp_thd == None):
        lamp_thd = threading.Thread(target=led.lampLightOn)
        led.lamp_power = True
        lamp_thd.start()
     
    elif(thd == "mobile" and mobile_thd == None):
        mobile_thd = threading.Thread(target=mobile.mobile) 
        mobile.mobile_state = True
        mobile_thd.start()

    elif(thd == "music" and music_thd == None):
        music_thd = threading.Thread(target=music.playMusic)
        music.music_state = True
        music_thd.start()
    
    return
        
        

def joinThread(thd):
    global led_thd,lamp_thd, mobile_thd, music_thd
    global mobile_flag, led_flag, music_flag
     
    if(thd == "led" and led_thd != None):
        led.power = False
        led_thd.join()
        led_thd = None
    
    elif(thd == "lamp" and lamp_thd != None):
        led.lamp_power = False
        led.lampLightOff()
        lamp_thd.join()
        lamp_thd = None
        
    elif(thd == "mobile" and mobile_thd != None):
        mobile.mobile_state = False
        mobile_thd.join()
        mobile_thd = None
        
    elif(thd == "music" and music_thd != None ):
        music.endMusic()
        music_thd.join()
        music_thd = None
    
    return

def joinGpioThread():    
    global led_thd,lamp_thd, mobile_thd, music_thd
    
    if(led_thd != None):
       joinThread("led")

    if(lamp_thd != None):
        led.lamp_power = False
        led.lampOff()
        lamp_thd.join()
        lamp_thd = None
    
    if(mobile_thd != None):
       joinThread("mobile")
    
    if(music_thd != None):
        joinThread("music")
        
    return 

def checkThd():
    global led_thd, lamp_thd, mobile_thd, music_thd, thread_state
    
    if led_thd == None and lamp_thd == None and mobile_thd == None and music_thd == None: 
        thread_state = False
    else:
        thread_state = True
    
    return

def main():
    global baby, thread_state
    global led_thd, lamp_thd, mobile_thd, music_thd
    while(1):
        try:
            #eye ratio and baby stats
            eyeController()
            
            #GPIO
            statusController()
            
            #if baby is none thd all false 
            if(thread_state==True and baby==constant.NONE):
                joinGpioThread()
            
            checkThd()
                
        except KeyboardInterrupt:
            joinGpioThread()
            checkThd()
            
            
if __name__ == "__main__":
    main()