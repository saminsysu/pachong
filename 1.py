#! /usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import bs4

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


if __name__=='__main__':
	r=requests.get(url='http://www.qiushibaike.com/')
	s=BeautifulSoup(r.text,'html.parser')
	with open('joke.txt','w') as fp:
		count=1
		is_begin=1
		for tag in s.select(".content > span"):
			# print(tag.span.strings)
			# for string in tag.span.strings:
			# 	print string
			# 	fp.write(unicode(tag.span.string)+'\n')
			# print(tag)		
			# print type(unicode(tag.span.string))
			print(tag)			
			for child in tag.descendants:	
				if isinstance(child,bs4.element.NavigableString):
					if is_begin:
						fp.write(str(count)+'. '+unicode(child)+'\n')
						is_begin=0
					else:
						fp.write(unicode(child)+'\n')
					print child
			count+=1
			is_begin=1
