import socket
import baby
import led
import mobile
import audio
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

def init():
    global server_socket, client_socket, addr
    
    # Pick an open Port (1000+ recommended), must match the server port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(">>>>>>>>>>>>>")
    client_socket, addr = server_socket.accept()

    print("client_socket")
    print(client_socket)

def receive():
    global code, client_socket, addr
    
    # 무한루프를 돌면서 
    while True:
        
        # 클라이언트가 보낸 메시지를 수신하기 위해 대기합니다. 
        data = client_socket.recv(1024)
        
        # # 빈 문자열을 수신하면 루프를 중지합니다. 
        if not data:
            break

        print('Received from', addr, data.decode())
        
        if data == b'\x00\x012':
            print("mobile on")
        elif data == b'\x00\x0222':
            print("mobile off")
        elif data == b'\x00\x013':
            print("led on")
        elif data == b'\x00\x0233':
            print("led off")
        elif data == b'\x00\x014':
            print("illuminance on")
        elif data == b'\x00\x0244':
            print("illuminance off")
        elif data == b'\x00\x015':
            print("music on")
        elif data == b'\x00\x0255':
            print("music off")
        elif data == b'\x00\x016':
            print("voice on")
        elif data == b'\x00\x0266':
            print("voice off")
        
 
def send():   
    global msg, client_socket
    
    while 1:
        if baby.baby == constant.WAKE:
            msg = "1"
        else:
            msg = "0"
        
        if mobile.mobile_state == True:
            msg = msg + "1"
        else:
            msg = msg + "0"
            
        if led.power == True:
            msg = msg + "1"
        else:
            msg = msg + "0"
        
        #illu
        msg += "1"
        
        if audio.end == False:
            msg = msg + "1"
        else:
            msg = msg + "0"
        # voice
        msg += "1"
        print(">>>>>>>>>>>>>>>>>>>>>>>>msg", msg)
        client_socket.sendall(msg.encode())
    
    


def close():
    global client_socket, server_socket
# 소켓을 닫습니다.
    client_socket.close()
    server_socket.close()


def main():
   
    try:
        init()
        
        t1 = threading.Thread(target=receive)
        t1.start()
        t2 = threading.Thread(target=send)
        t2.start()
        
        while True:
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("Ctrl+C Pressed.")
        close()
        t1.join()
        t2.join()
        #need to 

if __name__ == "__main__":
	main()