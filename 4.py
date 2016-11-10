#! /usr/bin/env python
# -*- coding:utf-8 -*-

'''多线程爬虫'''

import threading
import Queue
from bs4 import BeautifulSoup
import requests 

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

urlQueue=['http://www.sysu.edu.cn/2012/cn/zdgk/zdgk01/15746.htm',
	'http://www.sysu.edu.cn/2012/cn/zdgk/zdgk01/15747.htm',
	'http://www.sysu.edu.cn/2012/cn/zdgk/zdgk01/15748.htm',
	'http://www.sysu.edu.cn/2012/cn/zdgk/zdgk01/15749.htm',
	'http://www.sysu.edu.cn/2012/cn/zdgk/zdgk01/index.htm',
	'http://www.sysu.edu.cn/2012/cn/zdgk/zdgk01/15751.htm'
]
workQueue=Queue.Queue(10)
queueLock=threading.Lock()
is_done=0
threads=[]

class myThread(threading.Thread):
	def __init__(self,threadId):
		threading.Thread.__init__(self)
		self.threadId=threadId
	
	def run(self):
		print('starting thread-%d' %self.threadId)
		parse_html(self.threadId)
		print('ending thread-%d' %self.threadId)

def parse_html(threadId):
	while not is_done:
		queueLock.acquire()
		if not workQueue.empty():
			url=workQueue.get()
			queueLock.release()
			print('thread-%d start parse url:%s' %(threadId,url))
			html=requests.get(url).content
			s=BeautifulSoup(html,'html.parser')
			contentcontainer=s.find('div',attrs={'id':'contentcontainer'})
			title=contentcontainer.find('h1').get_text()
			content=contentcontainer.find('div',attrs={'id':'cont'}).get_text()
			queueLock.acquire()
			with open('sysu.txt','a+') as fp:
				fp.write(title+'\n'+content+'\n\n\n')
			queueLock.release()

		else:
			queueLock.release()

for i in range(3):
	t=myThread(i)
	t.start()
	threads.append(t)

#添加任务，在添加任务的时候主线程锁定资源
queueLock.acquire()
for url in urlQueue:
	workQueue.put(url)
queueLock.release() 	

while not workQueue.empty():
	pass

is_done=1

for thread in threads:
	thread.join()

print('ending main thread')
