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

def main():
	print download_page(URL)

if __name__=='__main__':
	main()
