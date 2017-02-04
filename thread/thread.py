# -*- coding:utf-8 -*-
from queue import Queue 
from threading import Thread,Lock
import urllib.parse
import socket
import time
import re

seen_urls=set(['/']) #存储已经解析到的url地址
lock=Lock()

class Fetcher(Thread):
	def __init__(self,tasks):
		Thread.__init__(self)
		self.tasks=tasks
		#主程序中断退出后，子线程也会中断退出
		self.daemon=True
		self.start()

	def run(self):
		while  True:
			url=self.tasks.get()
			print(url)	
			sock=socket.socket()
			sock.connect(('localhost',3000))
			#get内容:
			#GET / HTTP/1.0
			#Host: localhost
			get='GET {} HTTP/1.0\r\nHost: localhost\r\n\r\n'.format(url)
			sock.send(get.encode('ascii'))
			response=b''
			chunk=sock.recv(4096)
			while chunk:
				response+=chunk
				chunk=sock.recv(4096)

			#response保存的是整个页面的html
			links=self.parse_links(url,response)

			lock.acquire()
			#difference是集合的方法，去掉共有的元素，返回一个新的集合
			for link in links.difference(seen_urls):
				self.tasks.put(link)

			#update是集合中的方法，添加多个元素
			seen_urls.update(links)
			lock.release()
			self.tasks.task_done()

	def parse_links(self,fetched_url,response):
		if not response:
			print('error:{}'.format(fetched_url))
			return set()
		if not self._is_html(response):
			return set()

		#匹配 href="......" 不区分大小写
		urls=set(re.findall(r'''(?i)href=["']?([^\s"'<>]+)''',
							self.body(response)))
		
		links=set()
		for url in urls:
			#如果url是相对路径，需要join一下
			#urllib.parse.urljoin():fetched_url+url
			normalized=urllib.parse.urljoin(fetched_url,url)
			
			#urllib.parse.urlparse():解析地址
			parts=urllib.parse.urlparse(normalized)
			if parts.scheme not in ('','http','https'):
				continue

			#获取主机名和端口号
			host,port=urllib.parse.splitport(parts.netloc)
			if host and host.lower() not in ('localhost'):
				continue

			#有的页面会通过path中的#frag后缀在页面内跳转，去掉path中frag的部分
			defragmented,frag=urllib.parse.urldefrag(parts.path)
			links.add(defragmented)

		return links

	#去掉response中的响应头部分的数据，只需要<!DOCTYPE html PUBLIC以后的部分
	def body(self,response): 
		body=response.split(b'\r\n\r\n',1)[1]
		return body.decode('utf-8')
		
	#通过响应头的数据来判断返回的response是不是html
	def _is_html(self,response):
		head,body=response.split(b'\r\n\r\n',1)
		headers=dict(h.split(': ') for h in head.decode().split('\r\n')[1:])
		return headers.get('Content-Type','').startswith('text/html')

class ThreadPool:
	def __init__(self,num_threads):
		self.tasks=Queue()
		for _ in range(num_threads):
			Fetcher(self.tasks)

	def add_task(self,url):
		self.tasks.put(url)

	def wait_completion(self):
		self.tasks.join() #当前函数阻塞在这一步直到队列中存储的url都被get完

if __name__=='__main__':
	start=time.time()
	pool=ThreadPool(4)
	pool.add_task('/')
	pool.wait_completion()
	print('{} URLs fetched in {:.1f} seconds'.format(len(seen_urls),time.time()-start))
	print(start)








