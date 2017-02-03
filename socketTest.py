# -*- coding:utf-8 -*-
import socket

s=socket.socket()
host=socket.gethostname() #获得主机名
port=12345
#r=b'hello world' 最简单的办法就是在字符串前加个b
content='你好世界'
r=content.encode('utf-8') #将数据进行编码
s.bind((host,port))

s.listen(5)
while True:
	c,addr=s.accept() #被动接受TCP客户端连接,(阻塞式)等待连接的到来
	print('连接地址:',addr)
	c.send(r)
	c.close()