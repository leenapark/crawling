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
fname = "naver_news/" + td + ".csv"


if not os.path.exists("naver_news"):
    os.mkdir("naver_news")

# 첫라인 뽑기 : 생략 가능해짐
# with open(fname, "w", encoding="UTF-8") as file:
#         file.write(news_title[0].string)
#         file.close()


# titleList=[]
for headLine in news_title:
    # print(headLine.string)
    # print(headLine.get_text(strip=True)) # strip 등 사용 가능
    # print(type(headLine.get_text())) # 'str'
    # print(type(news_title)) # 'bs4.element.Tag'
    # print(type(news_title.string)) # 'bs4.element.NavigableString'
    header = headLine.string
    # titleList.append(header)

    # 첫라인 뽑기 : "a"가 file이 없을 경우 생성되기 때문에 위에 with open("w")는 생략해도 됨
    with open(fname, "a", encoding="UTF-8") as fileAdd:
        fileAdd.write(header + "\n")
        fileAdd.close()

