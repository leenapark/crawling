import requests as req
from bs4 import BeautifulSoup as bs
import datetime
import os
import csv

url = "https://finance.naver.com/marketindex/exchangeList.naver"
res = req.get(url)
soup = bs(res.text, "html.parser")
# print(soup)

td = datetime.datetime.today()
td = td.strftime("%Y-%m-%d-%H")
tbody = soup.find_all("iframe tbody")
tbody = soup.select("tbody > tr")

if not os.path.exists("exchange_rate"):
    os.mkdir("Exchange_Rate")

fName = "exchange_rate/" + td + ".csv"
file = open(fName, "w", newline="", encoding="UTF-8-sig")

arr = soup.select("body table.tbl_exchange tbody tr")

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
    exName = tr.select_one("td:nth-child(1)").get_text(strip=True)
    # print(exName)
    exRate = tr.select_one("td:nth-child(2)").get_text(strip=True).replace(",", "")
    exPurchase = tr.select_one("td:nth-child(3)").get_text(strip=True).replace(",", "")
    # if "N/A" == exPurchase:
    #     data.append([exName, exRate, exRate])
    # else:
    #     data.append([exName, exRate, exPurchase])
    if "N/A" == exPurchase:
        exPurchase = exRate
        print(exPurchase)

    data.append([exName, exRate, exPurchase])
    # print(exRate)
    # dataList.append(exName)
    # dataList.append(exRate)
    # data.append(dataList)
    # print(dataList)
print(data)

# csv file 저장
csv.writer(file).writerows(data)
# write.writerows(data)