# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup as bs
from threading import Thread
from termcolor import colored
import time
import requests
import os
import re
import urllib, urllib2
import sys
# local
from content_page import content_page


class main_page:

	def __init__(self, query_key='', url=''):
		base_url = 'http://www10.eyny.com/'

		if query_key:
			post_url = 'http://www10.eyny.com/search.php?searchsubmit=yes'
			form_data = {
				'mod': 'forum',
				'formhash': 'c1379277',
				'srchtype': 'title',
				'srchfrom': '0',
				'cid': '',
				'srhfid': '',
				'srhlocality': 'forum::index',
				'srchtxt': query_key,
				'searchsubmit': 'true',
			}

			headers = {
				'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
				'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
				'Cache-Control': 'max-age=0',
				'Connection': 'keep-alive',
				'Content-Length': '124',
				'Content-Type': 'application/x-www-form-urlencoded',
				#'Cookie': 'djAX_e8d7_lastvisit=1462263079; __utma=49542194.860393406.1462266684.1462266684.1462266684.1; __utmc=49542194; __utmz=49542194.1462266684.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); djAX_e8d7_auth=11b9xMLy4Yw6TV62d%2BYV0EixwF3%2B2E06FCA8J9zJGhZSA6KATZuf6NI3hjWspNS6VlPj71nrp5nUawZEw05XvMpdeCYW; djAX_e8d7_home_readfeed=1463740614; djAX_e8d7_visitedfid=205D1716; username=willy821002; djAX_e8d7_ulastactivity=6bcb8%2BuzQ8PYxPqc9JKdRenYBFgHDSNJEhbs%2Ft3uUtdPSxnceK0C; djAX_e8d7_fid205=1463806035; djAX_e8d7_favorite=a%3A2%3A%7Bi%3A205%3Bs%3A29%3A%22%E9%9B%BB%E5%BD%B1%E4%B8%8B%E8%BC%89%E5%8D%80%28%E4%B8%8A%E5%82%B3%E7%A9%BA%E9%96%93%29%22%3Bi%3A1716%3Bs%3A32%3A%22%E9%9B%BB%E8%A6%96%E5%8A%87%E4%B8%8B%E8%BC%89%E5%8D%80%28%E4%B8%8A%E5%82%B3%E7%A9%BA%E9%96%93%29%22%3B%7D; djAX_e8d7_forum_lastvisit=D_1716_1463740729D_205_1463806888; djAX_e8d7_onlineusernum=25567; djAX_e8d7_checkpm=1; djAX_e8d7_sendmail=1; __utmt=1; djAX_e8d7_lastact=1463808005%09index.php%09; djAX_e8d7_sid=J4WXOE; __utma=72231445.1631616965.1463806231.1463806231.1463806231.1; __utmb=72231445.23.10.1463806231; __utmc=72231445; __utmz=72231445.1463806231.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __asc=b67e469c154d1a683b507903c63; __auc=fd62d81c15475e2e20dc822e901',
				'Host': 'www10.eyny.com',
				'Origin': 'http://www10.eyny.com',
				'Referer': 'http://www10.eyny.com/index.php',
				'Upgrade-Insecure-Requests': '1',
				'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
			}
			session = requests.Session()
			result = session.post(post_url, headers=headers, data=form_data)

		elif url:
			get_url = url

			headers = {
				'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
				'Accept-Encoding':'gzip, deflate, sdch',
				'Accept-Language':'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
				'Connection':'keep-alive',
				'Cookie':'__utma=49542194.1479373395.1460788155.1461477314.1461482977.3; __utmc=49542194; __utmz=49542194.1461482977.3.3.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); djAX_e8d7_lastvisit=1463574006; djAX_e8d7_secqaaS5X7aRi0=0c94aWBU4gRWrN8wXj6U%2BeGV2rDW1HYulQSsi41kuehEK6lkefT7zOqzWXwyKo86Cm6SGRQVykN4M8JOb1A4Am0yT%2BjPFMl5RJcGMZmZ%2BTSXAZdDTDt3NRCc; djAX_e8d7_viewuids=14614408_1443603_15485262; djAX_e8d7_home_diymode=1; djAX_e8d7_view_blogid=746051; djAX_e8d7_secqaaSFW7Qkk0=e532Rl5Hzk8h8PXGF4zFSkcKVd%2FXwcVc%2FT3x0htQv%2BAViQj%2BkFYaIaV%2BROBzYCy5oi7bSCErakMF2K9MmSWhUZ1KjCrWVoQ1aU2vOAgX5iOzhMUwA2sJ4Ib3; djAX_e8d7_collapse=_category_576_; djAX_e8d7_auth=6ff4q45oQkPdeAc2bIv5lXf%2BoyB0siPUlDaEQ8mKXjkFPZqmvCQtpNa9z%2Ffzckozoa2JLb%2B9SPP%2BFLLWJjwK4V6zEXAk; djAX_e8d7_home_readfeed=1465532492; djAX_e8d7_ulastactivity=d9f1GB%2B7ZPDIwRnb0NbT8dubAcMxCjSbEJF%2B0cVdewfr1K9ZeLko; djAX_e8d7_favorite=a%3A3%3A%7Bi%3A205%3Bs%3A29%3A%22%E9%9B%BB%E5%BD%B1%E4%B8%8B%E8%BC%89%E5%8D%80%28%E4%B8%8A%E5%82%B3%E7%A9%BA%E9%96%93%29%22%3Bi%3A576%3Bs%3A26%3A%22%E6%88%90%E4%BA%BA%E9%9B%BB%E5%BD%B1%28%E4%B8%8A%E5%82%B3%E7%A9%BA%E9%96%93%29%22%3Bi%3A2%3Bs%3A26%3A%22%E6%97%A5%E9%9F%93%E9%9B%BB%E5%BD%B1%28%E4%B8%8A%E5%82%B3%E7%A9%BA%E9%96%93%29%22%3B%7D; djAX_e8d7_forum_lastvisit=D_2_1464945841D_205_1465532501; djAX_e8d7_agree=577; djAX_e8d7_visitedfid=32D205D2D1716D68; djAX_e8d7_sendmail=1; djAX_e8d7_onlineusernum=24087; djAX_e8d7_checkpm=1; username=willy821002; __utmt=1; djAX_e8d7_lastact=1465545443%09search.php%09forum; djAX_e8d7_sid=F5aFU6; __utma=72231445.1436645782.1465545439.1465545439.1465545439.1; __utmb=72231445.2.10.1465545439; __utmc=72231445; __utmz=72231445.1465545439.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __asc=e7fffce4155394f2ee09101f1b5; __auc=bd9bb8a4153f8ce08a19fa87e53',
				'Host':'www10.eyny.com',
				'Referer':'http://www10.eyny.com/search.php?mod=forum&searchid=441298&orderby=lastpost&ascdesc=desc&searchsubmit=yes&srchfrom=0&kw=%E6%B3%A2',
				'Upgrade-Insecure-Requests':'1',
				'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
			}
			result = requests.get(get_url)

		else:
			eprint('------ ERROR : You Must Key In The Query Word Or URL ------')
			sys.exit(0)

		soup = bs(result.text, 'lxml')

		# get all sub-link in this page
		all_links_block = soup.findAll("a", {"class": "xst"})
		inner_page = list()
		threads = []

		# search main page all link
		for link in all_links_block:
			if link:
				content_page_link = base_url+link['href']
				package = {'href':content_page_link, 'title':link.text, 'read':0, 'inqueue':0}
				new_t = Thread(target=self.get_content_detail, args=(package, content_page_link))
				new_t.start()
				threads.append(new_t)
				inner_page.append(package)
		for t in threads:
			t.join()

		# get the link of next page
		next_page_link = soup.findAll("a", {"class": "nxt"})
		if next_page_link:
			next_main_page_link = base_url+next_page_link[0]['href']
		else:
			next_main_page_link = None


		self.inner_page = inner_page
		self.next_main_page_link = next_main_page_link

	def get_content_detail(self, package, url):
		package['content_page'] = content_page(url)


	def show_page_list(self):
		table_header = '📷 🔎 No. Title'
		print table_header
		for i in range(len(self.inner_page)):
			# user read this link or not
			if self.inner_page[i]['read'] == 1:
				read_symbol = colored(u'✓', 'green')
			else:
				read_symbol = colored(' ', 'green')

			# check this link has mega download link or not
			if not self.inner_page[i]['content_page'].links:
				title = colored(self.inner_page[i]['title'], 'red')
			else:
				if self.inner_page[i]['inqueue'] == 1:
					title = colored(self.inner_page[i]['title'], 'green')
				else:
					title = self.inner_page[i]['title']

			# count image in the link
			if len(self.inner_page[i]['content_page'].image_url_list):
				image_length = str(len(self.inner_page[i]['content_page'].image_url_list))
			else:
				image_length = ' '

			print "%s %s %3d %s" % (image_length, read_symbol, i+1, title)



def wait_animation():
	status = ['Searching | ...', 'Searching / ... ...', 'Searching - ... ... ...', 'Searching \\ ... ... ... ...']
	c = 0
	while True:
		os.system('clear')
		print status[c]
		time.sleep(1)
		c = (c+1)%len(status)




if __name__ == '__main__':
	""" FOR TEST """
	query_key = u'波'
	m = main_page(query_key=query_key)
	# n = main_page(url='http://www10.eyny.com/search.php?mod=forum&searchid=441298&orderby=lastpost&ascdesc=desc&searchsubmit=yes&srchfrom=0&page=D8OV2WF0')
	m.show_page_list()
