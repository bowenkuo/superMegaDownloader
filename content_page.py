# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup as bs
import requests
import re
# local
from open_photo import MainWin

class content_page:

	def __init__(self, url):

		form_data = {
			'mod': 'forum',
			'formhash': 'c1379277',
			'srchtype': 'title',
			'srchfrom': '0',
			'cid': '',
			'srhfid': '',
			'srhlocality': 'forum::index',
			'searchsubmit': 'true',
		}

		headers = {
			'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Accept-Language':'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
			'Cache-Control':'max-age=0',
			'Connection':'keep-alive',
			'Cookie':'djAX_e8d7_viewuids=14614408; djAX_e8d7_home_diymode=1; __utma=49542194.1479373395.1460788155.1461477314.1461482977.3; __utmc=49542194; __utmz=49542194.1461482977.3.3.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); djAX_e8d7_lastvisit=1463574006; djAX_e8d7_auth=13c75xDygKA0MgYEIPtN3IIMKCaA6T8dyhL%2BsrlgCCo1XVHQzqsxnOSWJ4pxSQEJK3ygu48tUBNOBnjJLH6fDeD3T1wM; djAX_e8d7_home_readfeed=1463577683; djAX_e8d7_agree=576; username=willy821002; djAX_e8d7_onlineusernum=31632; djAX_e8d7_ulastactivity=f2b5H8erFwRioFsoE5w4ejQaCjgSNOfnaohmfLxU0Px11Krgvn52; djAX_e8d7_sendmail=1; __utmt=1; djAX_e8d7_favorite=a%3A3%3A%7Bi%3A205%3Bs%3A29%3A%22%E9%9B%BB%E5%BD%B1%E4%B8%8B%E8%BC%89%E5%8D%80%28%E4%B8%8A%E5%82%B3%E7%A9%BA%E9%96%93%29%22%3Bi%3A576%3Bs%3A26%3A%22%E6%88%90%E4%BA%BA%E9%9B%BB%E5%BD%B1%28%E4%B8%8A%E5%82%B3%E7%A9%BA%E9%96%93%29%22%3Bi%3A2%3Bs%3A26%3A%22%E6%97%A5%E9%9F%93%E9%9B%BB%E5%BD%B1%28%E4%B8%8A%E5%82%B3%E7%A9%BA%E9%96%93%29%22%3B%7D; djAX_e8d7_forum_lastvisit=D_205_1463837366; djAX_e8d7_visitedfid=205D2D1716D68D537; djAX_e8d7_fid205=1463837277; djAX_e8d7_sid=495g1H; djAX_e8d7_lastact=1463837423%09home.php%09spacecp; djAX_e8d7_checkpm=1; __utma=133292552.858013555.1463837357.1463837357.1463837357.1; __utmb=133292552.4.10.1463837357; __utmc=133292552; __utmz=133292552.1463837357.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __asc=b0858fb2154d381753fb640c667; __auc=bd9bb8a4153f8ce08a19fa87e53',
			'Host':'www84.eyny.com',
			'Referer':'http://www84.eyny.com/forum-205-1.html',
			'Upgrade-Insecure-Requests':'1',
			'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
		}

		session = requests.Session()
		result = session.get(url, headers=headers)
		soup = bs(result.text, 'lxml')
		post_list = soup.findAll("div", {"id": "postlist"})

		
		try:
			# get page title
			title = soup.findAll("a", {"id": "thread_subject"})[0].text

			# get password
			first_floor_content = post_list[0].findAll('div')[2].text	
			passwd = re.search(u'密碼.*', first_floor_content)
			if passwd:
				passwd = passwd.group(0)

			# get mega download links
			links = list()
			content_split_by_a_href = str(post_list[0]).split('<a href="')
			for x in content_split_by_a_href:
				r = re.search("https://mega.co.nz/[A-Za-z0-9#!_-]*\" target=\"_blank\">", x)
				if r:
					links.append(r.group(0).split('"')[0])
				else:
					r = re.search('https://mega.nz/[A-Za-z0-9#!_-]*" target="_blank">', x)
					if r:
						links.append(r.group(0).split('"')[0])

			# get image link
			image_url_list = list()
			image_block = post_list[0].findAll("img", {"class": "zoom"})
			for image in image_block:
				if image['file']:
					image_url_list.append(image['file'])

		except:
			title = u'沒有權限'
			passwd = ''
			links = list()
			image_url_list = list()

		self.title  = title
		self.passwd = passwd
		self.links  = links
		self.image_url_list = image_url_list

	def show_image(self):
		if len(self.image_url_list) != 0:
			image_count = 0
			image_choice = ''
			while True:
				print "Image : " + str(image_count+1) + "/" + str(len(self.image_url_list))
				MainWin(self.image_url_list[image_count]).main()
				image_choice = raw_input("(N) - Show next image\n(P) - Show previous image\n(C) - Cancel\nYour choice : ")
				if image_choice == 'N' or image_choice == 'n':
					image_count = (image_count+1)%len(self.image_url_list)
				elif image_choice == 'P' or image_choice == 'p':
					image_count = (image_count-1)
					if image_count < 0:
						image_count += len(self.image_url_list)
				elif image_choice == 'C' or image_choice == 'c':
					return ''
				else:
					print "[ERR] - Wrong choice"

		else:
			return "[ERR] - This page has no image"



if __name__ == '__main__':
	TEST_URL = 'http://www10.eyny.com/forum.php?mod=viewthread&tid=8511942&highlight=%E6%9A%AE%E5%85%89%E4%B9%8B%E5%9F%8E'
	print '''FOR TESTING\nTESTING URL: {url}'''.format(url=TEST_URL)

	first_page = content_page(TEST_URL)
	print first_page.title.encode('utf-8')
	print first_page.passwd.encode('utf-8')
	print first_page.links