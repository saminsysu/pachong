#! /usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import bs4

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

URL='https://movie.douban.com/top250'

def download_page(url):
	return requests.get(url).content

def parse_html(html):
	s=BeautifulSoup(html,'html.parser')
	o=s.find("ol",attrs={'class':"grid_view"})
	film_list=[]
	for l in o.find_all("li"):
		Num=l.find("em",attrs={'class':''}).get_text()
		hd=l.find('div','hd')
		titles=hd.find_all("span","title")
		other_title=hd.find("span","other").get_text()
		Title=""
		for i in range(len(titles)):
			Title+=titles[i].get_text()
		Title+=other_title
		quote=l.find('span','inq')
		Quote=""
		if quote:
			Quote=quote.get_text()
		film_list.append({'num':Num,'title':Title,'quote':Quote})
	next_page=s.find("span","next").a
	if next_page:
		return film_list,URL+next_page['href']
	return film_list,None

def main():
	with open('films.txt','w') as fp:
		url=URL
		while url:
			filmList,url=parse_html(download_page(url))
			for film in filmList:
				fp.write(film['num']+'.'+film['title']+'\n'+film['quote']+'\n')

if __name__=='__main__':
	main()
