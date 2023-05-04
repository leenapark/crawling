# 데이터 수집
# DB 생성(sql)
# Table 생성
# Data insert : 코드 작성


import requests as req
from bs4 import BeautifulSoup as bs
import datetime
import os
import csv
import pymysql
import pandas as pd
from db_info import *
import re


url = "https://finance.naver.com/marketindex/exchangeList.naver"
res = req.get(url)
soup = bs(res.text, "html.parser")
# print(soup)

td, nowDate = datetime.datetime.now(), datetime.datetime.now()
td = td.strftime("%Y-%m-%d-%H")
nowDate = nowDate.strftime("%Y-%m-%d %H:%M:%S")
nowDate = datetime.datetime.strptime(nowDate, "%Y-%m-%d %H:%M:%S")
# print(td)
# print(nowDate)
# print(type(nowDate))
tbody = soup.find_all("iframe tbody")
tbody = soup.select("tbody > tr")

if not os.path.exists("exchange_rate"):
    os.mkdir("exchange_rate")

fName = "exchange_rate/" + td + ".csv"
file = open(fName, "w", newline="", encoding="UTF-8-sig")

arr = soup.select("body table.tbl_exchange tbody tr")

data = []
for tr in tbody:
    exName = tr.select_one("td:nth-child(1)").get_text(strip=True)
    excId = exName.encode("UTF-8-sig").decode('ascii', 'ignore')
    excId = excId.strip().split(" ")[0]
    exName = re.sub(r"[^가-힣]", "", exName)
    # print(excId)
    exRate = tr.select_one("td:nth-child(2)").get_text(strip=True).replace(",", "")
    exPurchase = tr.select_one("td:nth-child(3)").get_text(strip=True).replace(",", "")
    if "N/A" == exPurchase:
        data.append([exName, excId, exRate, exRate, td])
    else:
        data.append([exName, excId, exRate, exPurchase, td])


# print(data)

# csv file 저장
csv.writer(file).writerows(data)

conn = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset=charset)
cur = conn.cursor()

# fileCSV = open("exchange_rate/2023-05-04-15.csv", "r")
# csvReader = csv.reader(fileCSV)


# 생성된 csv 파일 가져와서 db 저장
# df = pd.read_csv("exchange_rate/2023-05-04-15.csv", sep=",")
# print(df)
# df = csv.reader("exchange_rate/2023-05-04-15.csv", delimiter=" ", quotechar="|")
# print(df)

sql = """
    INSERT INTO exchange VALUES(
            %s,
            %s,
            %s,
            %s,
            %s
    )
    """
cur.executemany(sql, data)



# for curData in df.iterrows():
# for curData in csvReader:
#     print(curData)
#     country = curData[0]
#     excName = curData[1]
#     excSd = curData[2]
#     excBuy = curData[3]
#     regDate = curData[4]
#     # print(curData[0])
#     # print(curData[1])
#     # print(curData[2])
#     sql = """
#     INSERT INTO exchange VALUES(
#             %s,
#             %s,
#             %s,
#             %s,
#             %s
#     )
#     """
#     print(country)
#     # cur.execute(sql, (country, excName, excSd, excBuy, regDate))

conn.commit()
# fileCSV.close()
# conn.close()

sql = """
SELECT *
FROM exchange
"""

df = pd.read_sql(sql, conn, index_col="country")
print(df)