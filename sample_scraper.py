from bs4 import BeautifulSoup
import re

from urllib.request import Request, urlopen

req = Request(
    url='https://www.7mj.net/view/32237.html', 
    headers={'User-Agent': 'Mozilla/5.0'}
)

html_page = urlopen(req).read()
print(html_page)
soup = BeautifulSoup(html_page,features="html.parser")

images = []
for img in soup.findAll('img'):
    images.append(img.get('data-src'))

print(images)