#! /usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import bs4, time
from PIL import Image
import cookielib, os

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

session=requests.Session()

URL='https://www.zhihu.com/'


headers={
	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/53.0.2785.143 Chrome/53.0.2785.143 Safari/537.36',
	'Host': 'www.zhihu.com',
	'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language': 'zh-CN,zh;q=0.8'
}


def get_xsrf():
	url='https://www.zhihu.com/#signin'
	r=session.get(url)
	s=BeautifulSoup(session.get(url,headers=headers).content,'html.parser')
	xsrf=s.select('[name=_xsrf]')[0]['value']
	print('_xsrf:%s' %xsrf)
	return xsrf

def get_captcha():
	t=str(int(time.time()*1000))
	url='https://www.zhihu.com/captcha.gif?r='+t+'&type=login'
	captcha=session.get(url,headers=headers).content
	with open('captcha.png','wb') as fp:
		fp.write(captcha)
	img=Image.open('captcha.png')
	img.show()
	captcha=raw_input('please input the captcha:')
	return captcha

def login(phone_num,password):
	url='https://www.zhihu.com/login/phone_num'
	data={
		'password': password,
		'phone_num': phone_num,
		'remember_me': 'true',
		'_xsrf': get_xsrf()
	}
	data['captcha']=get_captcha()
	post=session.post(url,headers=headers,data=data)
	if post.json()['r']==0:
		print 'login success~~~'
		cookie_jar = cookielib.LWPCookieJar()
		requests.utils.cookiejar_from_dict({c.name: c.value for c in session.cookies}, cookie_jar)
		cookie_jar.save(phone_num + '_cookies.txt',ignore_discard=True, ignore_expires=True)
	else:
		print 'login fail!!!'
	
def get_cookies(phone_num):
	if os.path.exists(phone_num + '_cookies.txt'):
		load_cookiejar = cookielib.LWPCookieJar()
		load_cookiejar.load(phone_num + '_cookies.txt', ignore_discard=True, ignore_expires=True)
		load_cookies = requests.utils.dict_from_cookiejar(load_cookiejar)
		cookies = requests.utils.cookiejar_from_dict(load_cookies)
		session.cookies=cookies
		return cookies
	else:
		return None


def download_page(url):
	return session.get(url,headers=headers).content

def parse_html(html):
	s=BeautifulSoup(html,'html.parser')
	feed_list=s.find('div',{'id':'js-home-feed-list'})
	with open('zhihu.txt','w') as fp:
		for item in feed_list.find_all('div','feed-item'):
			author=''
			summary=''
			item_author=item.find('a','author-link')
			item_summary=item.find('div','summary')
			if item_author:
				author=item_author.get_text()
			if item_summary:
				summry=item_summary.get_text()
			fp.write(author+': '+'\n'+summry+'\n')

def main():
	phone_num='18819481131'
	password='xiejiacun'
	if get_cookies(phone_num):
		print('you has already logged in~!')
		# session.cookies.update(get_cookies(phone_num))
	else:
		login(phone_num,password)
	html=download_page(URL)
	parse_html(html)

if __name__=='__main__':
	main()
