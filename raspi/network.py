import socket
import baby
import led
import mobile
import music
import constant
import threading
import time

HOST = '192.168.0.17'
# Enter IP or Hostname of your server
PORT = 12345

code = ""
msg = ""
server_socket = None
client_socket = None
addr = None
rt = None
st = None

def init():
    global server_socket, client_socket, addr
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((HOST, PORT))
    server_socket.listen()

    client_socket, addr = server_socket.accept()
    print(">>>>>>>>>>>>>>client", client_socket)

def receive():
    global code, client_socket, addr
    
    while True:
        
        data = client_socket.recv(1024)
        
        print(">>>>>>>>>>>>>>>>>>>>>>>>data is ", data.decode())
        
        if not data:
            break
        
        if data == b'\x00\x012':
            print("mobile on")

            if(baby.thread_state == True):
                baby.makeThread("mobile")
            else:
                baby.makeThread("mobile") 
                baby.thread_state = True
                
        elif data == b'\x00\x0222':
            print("mobile off")
            baby.joinThread("mobile")
            
        elif data == b'\x00\x013':
            print("led on")
            #need
            if(baby.thread_state == True):
                baby.makeThread("led")
            else:
                baby.makeThread("led") 
                baby.thread_state = True
            
        elif data == b'\x00\x0233':
            print("led off")
            baby.joinThread("led")
            
        # elif data == b'\x00\x014':
        #     print("illuminance on")
        
        #     if baby.thread_state == True:
        #         if baby.lamp_thd == None:
        #             baby.makeThread("lamp")
        #         else:
        #             led.changLampDutyCycle(1)
        #     else:
        #         if baby.lamp_thd == None:
        #             baby.makeThread("lamp")
        #         else:
        #             led.changLampDutyCycle(1)
        #         baby.thread_state = True
                 
        # elif data == b'\x00\x0244':
        #     print("illuminance off")
            
        #     if led.lamp_dc >= 10:
        #         led.changLampDutyCycle(0)
        #     else:
        #         baby.joinThread("lamp")
                
        elif data == b'\x00\x015\x00\x015':
            print("music a")
            
            if(baby.thread_state == True):
                baby.makeThread("music")
            else:
                baby.makeThread("music") 
                baby.thread_state = True
            music.music = "a"
            
        elif data == b'\x00\x015\x00\x015\x00\x015':
            print("music b") 
            if(baby.thread_state == True):
                baby.makeThread("music")
            else:
                baby.makeThread("music") 
                baby.thread_state = True
            music.music = "b"
            
        elif data == b'\x00\x015':
            print("music stop")
            baby.joinThread("music")
        # elif data == b'\x00\x016':
        #     print("voice on")
        # elif data == b'\x00\x0266':
        #     print("voice off")

        else:
            print(data)
        
 
def send():   
    global msg, client_socket
    
    while 1:
        if baby.baby == constant.AWAKE:
            msg = "1"
        elif(baby.baby == constant.ASLEEP):
            msg = "0"
        elif(baby.baby == constant.SLEEP):
            msg = "2"
        elif(baby.baby == constant.NONE):
            msg = "4"
        else:
            msg = "3"
        
        if mobile.mobile_state == True:
            msg = msg + "1"
        else:
            msg = msg + "0"
            
        if led.power == True:
            msg = msg + "1"
        else:
            msg = msg + "0"
        
        if music.music_state == True:
            msg = msg + "1"
        else:
            print(">>>>>>>>>>>>>>>must be here")
            msg = msg + "0"
        
        if led.lamp_dc == 10:
            msg = msg + "A"
        else:
            msg = msg + "{}".format(int(led.lamp_dc/10))
            
        msg += "0"
        # print(">>>>>>>>>>>>>>>>>>>>>>>>send msg", msg)
        client_socket.sendall(msg.encode())
        
        time.sleep(1)
    
    


def close():
    global rt, st
    print(">>>>>>>network join")
    global client_socket, server_socket
    # 소켓을 닫습니다.
    if client_socket != None:
        client_socket.close()
    server_socket.close()
    if rt != None:
        rt.join()
    if st != None:
        st.join()


def main():
    global rt, st
    try:
        init()
        rt = threading.Thread(target=receive)
        rt.start()
        st = threading.Thread(target=send)
        st.start()
        
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        close()

if __name__ == "__main__":
	main()