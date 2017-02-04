# -*- coding:utf-8 -*-
#threadpool模块与multiprocessing.pool中的threadpool有区别
import threadpool
import time
'''
def sayhello(str):
	print('hello',str)
	time.sleep(5)

name_list=['aa','bb','cc']
start_time=time.time()
for i in range(len(name_list)):
	sayhello(name_list[i])
print('%d s' %(time.time()-start_time))
'''
def sayhello(str):
	print('hello',str)
	time.sleep(5)

name_list=['aa','bb','cc']
start_time=time.time()
pool=threadpool.ThreadPool(10)
requests=threadpool.makeRequests(sayhello,name_list)
[pool.putRequest(req) for req in requests]
#等待所有线程完成工作后退出
pool.wait()
print('%d s' %(time.time()-start_time))