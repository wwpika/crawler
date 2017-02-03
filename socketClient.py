import socket

s=socket.socket()
host=socket.gethostname()
port=12345

s.connect((host,port))
content=s.recv(1024)
k=content.decode('utf-8') #对接收的数据进行解码
print (k) #接收TCP数据，数据以字符串形式返回，bufsize指定要接收的最大数据量
s.close()
