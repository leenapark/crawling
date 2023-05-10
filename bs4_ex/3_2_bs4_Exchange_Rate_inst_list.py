import requests as req
from bs4 import BeautifulSoup as bs
import datetime
import os

url = "https://finance.naver.com/marketindex/exchangeList.naver"
res = req.get(url)
soup = bs(res.text, "html.parser")
# print(soup)
tbody = soup.find_all("iframe tbody")
tbody = soup.select("tbody > tr")

data = []
for tr in tbody:
    # soup.메서드 실습
    # td = tr.find_all("td")[0].text
    # td = tr.find("td")
    # td = tr.select("td")[0].text
    # td = tr.select_one("td").text
    # 통화명 / 매매가
    # 통화명 추출, 양쪽 공백 strip 처리
    # dataList = []
    exName = tr.select_one("td.tit a").get_text(strip=True)
    # print(exName)
    exRate = tr.select_one("td.sale").get_text(strip=True).replace(",", "")
    # print(exRate)
    # dataList.append(exName)
    # dataList.append(exRate)
    data.append([exName, exRate])
    # data.append(dataList)
    # print(dataList)
print(data)
    