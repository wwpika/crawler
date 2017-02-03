# -*- coding:utf-8 -*-
from queue import Queue
from queue import LifoQueue

q=Queue()

for i in range(5):
	q.put(i)

while not q.empty():
	print (q.get())

q2=LifoQueue()

for i in range(3):
	q2.put(i)

while not q2.empty():
	print(q2.get())
