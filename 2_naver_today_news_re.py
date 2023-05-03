# 필요한 라이브러리 임폴트
# 필요한 데이터 url 찾기
# url로 request 요청 -> http 응답결과 옴
# 응답 결과의 text를 soup 객체로 만들기 : html 요소 지정 용이
# 추출할 데이터(크롤링할 데이터)의 요소 찾기(html tag, css, selector)
# soup.select("요소 태그")로 원하는 데이터 추출 진행
# 출력할 곳 정하기 (터미널/파일/DB)

import requests as req
from bs4 import BeautifulSoup as bs
import datetime
import os

# 네이버 뉴스 헤드 라인 추출
url = "https://news.naver.com/"

res = req.get(url)
soup = bs(res.text, "html.parser")
# print(soup)
news_title = soup.select("div.comp_journal_subscribe div.cjs_news_tw div.cjs_t")
# print(news_title)
td = datetime.datetime.today()
td = td.strftime("%Y-%m-%d-%H")
fname = "naver_news/" + td + "3.csv"


if not os.path.exists("naver_news"):
    os.mkdir("naver_news")



with open(fname, "a", encoding="UTF-8") as file:
    for headLine in news_title:
        headLine = headLine.get_text(strip=True)
        file.write(f"{headLine}\n")
    file.close()