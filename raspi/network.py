import socket

HOST = '192.168.0.17'
# Enter IP or Hostname of your server
PORT = 22
# Pick an open Port (1000+ recommended), must match the server port
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((HOST, PORT))
server_socket.listen()
print('Connected by', addr)


# 무한루프를 돌면서 
while True:

    # 클라이언트가 보낸 메시지를 수신하기 위해 대기합니다. 
    data = client_socket.recv(1024)

    # 빈 문자열을 수신하면 루프를 중지합니다. 
    if not data:
        break


    # 수신받은 문자열을 출력합니다.
    print('Received from', addr, data.decode())

    # 받은 문자열을 다시 클라이언트로 전송해줍니다.(에코) 
    client_socket.sendall(data)


# 소켓을 닫습니다.
client_socket.close()
server_socket.close()
