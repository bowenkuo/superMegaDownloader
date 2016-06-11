# -*- code: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs

r = requests.get('http://www10.eyny.com/forum.php?mod=viewthread&tid=10913039&highlight=%E6%B3%A2')
soup = bs(r.text, 'html.parser')
print soup.prettify().encode('utf-8')
