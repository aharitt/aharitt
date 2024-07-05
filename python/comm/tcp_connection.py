import socket

TCP_IP = "127.0.0.1"
TCP_PORT = 13001
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print('Connection Address:', addr)

data_to_send = b"devId:100,zHeight:19.53,angle1:91.38,angle2:80.16,angle3:33.24,angle4:7.77,alpha:10.56,beta:120.32,wafStatus:1,rdtsc:12868882681,outlier:0\r"
while 1:
        conn.send(data_to_send)
        data = conn.recv(BUFFER_SIZE)
        if not data: break
        print('Received Data:', data)

conn.close()