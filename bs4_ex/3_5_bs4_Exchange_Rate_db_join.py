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
conn = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset=charset)
cur = conn.cursor()


# sql="""
# CREATE TABLE IF NOT EXISTS cnt_cur (
# 	cnt_name varchar(20) NOT NULL,
# 	cur_id char(10) NOT NULL PRIMARY KEY
# );
# """
# cur.execute(sql)

# sql="""
# CREATE TABLE IF NOT EXISTS exc_rate (
# 	id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
# 	excName char(10) NOT NULL,
# 	trade_rate float UNSIGNED NOT NULL,
# 	excBuy float UNSIGNED,
# 	regDate varchar(20),
# 	FOREIGN KEY(excName) REFERENCES cnt_cur(cur_id)
# );
# """
# cur.execute(sql)




# nowDate  = datetime.datetime.now()
# # td = td.strftime("%Y-%m-%d-%H")
# nowDate = nowDate.strftime("%Y-%m-%d %H:%M:%S")
# # nowDate = datetime.datetime.strptime(nowDate, "%Y-%m-%d %H:%M:%S")
# # csv 파일 저장 : 테이블 이름

# tbody = soup.find_all("iframe tbody")
# tbody = soup.select("tbody > tr")

# if not os.path.exists("exchange_rate"):
#     os.mkdir("exchange_rate")

# fName = "exchange_rate/cnt_cur.csv"
# fName2 = "exchange_rate/exc_rate.csv"
# file1 = open(fName, "w", newline="", encoding="UTF-8-sig")
# file2 = open(fName2, "w", newline="", encoding="UTF-8-sig")

# arr = soup.select("body table.tbl_exchange tbody tr")



# datas_tb1 = []
# datas_tb2 = []
# for tr in tbody:
#     exName = tr.select_one("td:nth-child(1)").get_text(strip=True)
#     excId = exName.encode("UTF-8-sig").decode('ascii', 'ignore')
#     excId = excId.strip().split(" ")[0]
#     exName = re.sub(r"[^가-힣]", "", exName)
#     # print(excId)
#     exRate = tr.select_one("td:nth-child(2)").get_text(strip=True).replace(",", "")
#     exPurchase = tr.select_one("td:nth-child(3)").get_text(strip=True).replace(",", "")
#     datas_tb1.append([exName, excId])
#     if "N/A" == exPurchase:
#         datas_tb2.append([excId, exRate, exRate, nowDate])
#     else:
#         datas_tb2.append([excId, exRate, exPurchase, nowDate])

# # csv file 저장
# csv.writer(file1).writerows(datas_tb1)
# csv.writer(file2).writerows(datas_tb2)

# # print(datas_tb1)
# # print(datas_tb2)

# sql="""
#     INSERT INTO cnt_cur VALUES(
#             %s,
#             %s
#     )
# """

# cur.executemany(sql, datas_tb1)

# # conn.commit()

# sql = """
#     INSERT INTO exc_rate VALUES(
#             NULL,
#             %s,
#             %s,
#             %s,
#             %s
#     )
#     """
# cur.executemany(sql, datas_tb2)


# conn.commit()

# sql = """
# SELECT *
# FROM cnt_cur cc 
# 	JOIN exc_rate er 
# 	ON cc.cur_id = er.excName ;
# """

# df = pd.read_sql(sql, conn, index_col="cnt_name")
# print(f"")
# conn.close()