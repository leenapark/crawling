# pip install beautifulsoup4
# pip install requests

import requests as req
from bs4 import BeautifulSoup as bs

# 1. 원하는 url을 requests를 통해 response 받아옴
url = "https://www.naver.com/"
res = req.get(url) # 지정한 url html 문서를 가져올 때 : get("지정한 url")
# print(res)
# print(type(res)) # type : requests.models.Response
# print(res.text) : html string으로 가져옴 : 파싱 작업 필요
soup = bs(res.text, "html.parser")
# print(soup)
# print(type(soup)) # type : bs4.BeautifulSoup
print(soup.title) # soup.html태그명 불러오기 가능
print(soup.title.text)
print(soup.title.string)
print(soup.title.strings)

for i in soup.div.strings:
    print(i)
