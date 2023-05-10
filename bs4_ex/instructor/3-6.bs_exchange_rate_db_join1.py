# 각 나라별 화폐 환율 추출하기
# 1. 라이브러리
# 2. url로 request 요청, response 받기
# 3. text(html)만 추출 -> 텍스트
# 4. soup 객체로 생성
# 5. soup 메서드로 원하는 데이터 추출하기

import requests as req
from bs4 import BeautifulSoup as BS

import csv
import os
import datetime

import pymysql
from mydb_env_lesley import *

# url="https://finance.naver.com/marketindex/"
# iframe으로 되어 있어서 iframe의 url을 가져옴
# 환율 정보가 있는 url
url= "https://finance.naver.com/marketindex/exchangeList.naver"

# 2. url로 request 요청, response 받기
# 3. text(html)만 추출 -> 텍스트
# 4. soup 객체로 생성
res = req.get(url)
soup = BS(res.text, "html.parser")
# tbody = soup.find_all("iframe tbody")
tbody = soup.select("tbody > tr")
# print(tbody)

total_data_set = []

# join을 위해 리스트 변수 생성
# 통화 id, 나라 이름
country_datas = []
# 통화 id, 환율, 현금살때, 날짜
exchange_rate_datas = []

for tr in tbody:
  # 하나의 레코드를 위한 리스트
  data_set1=[]
  data_set2=[]
  # 통화명, 매매기준율 추출
  # 통화명 추출, 양쪽 공백 트림(자름)
  exc_name = tr.select_one("td.tit a").get_text(strip=True)


  # 통화 id(exc_id), 나라 이름(cnt_name) 추출해서 구분해야 함
  exc_id = exc_name.split(" ")[1].strip()
  cnt_name = exc_name.split(" ")[0].strip()

  if not exc_id.isupper():
    exc_id = exc_name.split(" ")[2].strip()
    cnt_name = exc_name.split(" ")[0:2]  # ['남아프리카', '공화국'] 예외 처리
    cnt_name = cnt_name[0] + cnt_name[1]
  print(f"{exc_id}-{cnt_name}")


  # 매매기준율 추출, 공백제거, ',' 제거
  exc_rate = tr.select_one("td.sale").get_text(strip=True)
  exc_rate = exc_rate.replace(',','')
  # 현금으로 살때 환율 금액 : cash_buy
  cash_buy = tr.select_one("td:nth-child(3)").get_text(strip=True)
  # 값중에 N/A으로 들어가 있는게 다수가 있음
  # N/A인 경우, 매매기준율로 대체함
  if(cash_buy == 'N/A'):
     cash_buy = exc_rate
  cash_buy = cash_buy.replace(',','')
  # print(cash_buy)


  # 통화 id, 나라 이름 : 하나의 레코드 구성
  data_set1.append(exc_id)
  data_set1.append(cnt_name)
  # 통화 id, 환율, 현금살때, 날짜 : 하나의 레코드 구성
  data_set2.append(exc_id)
  data_set2.append(exc_rate)
  data_set2.append(cash_buy)


  # list로 만들기(exchange_rate_datas.append()에서 했으므로 삭제)
  # data_set.append(exc_id)
  # data_set.append(exc_name)
  # data_set.append(exc_rate)
  # data_set.append(cash_buy)
  # print(data_set)
  # 전체 레코드를 저장하는 list에 data_set 추가

  # 데이터 생성날짜 format 만들기
  now_dt = datetime.datetime.now()
  now_date = now_dt.strftime('%Y-%m-%d %H:%M:%S')
  
  # data list에 날짜 시간 추가
  data_set2.append(now_date)


  # 2차원 리스트에 추가
  country_datas.append(data_set1)
  exchange_rate_datas.append(data_set2)

print(country_datas)
print(exchange_rate_datas)

# csv 파일로 저장
# 폴더이름 : exc_rate/
# 파일이름 : 2023-05-04-시간.csv

# 저장할 파일 이름 구하기
# 날짜 시간값을 원하는 포맷으로 변경
# 저장 file 이름 문자열로 정의
# !!!!!!!!!!!050423 = 각각 2개의 csv 파일로 저장 : 테이블이름.csv

now_t = now_dt.strftime("%Y-%m-%d-%H")
fname = now_t + ".csv"



# # exc_rate/ 디렉토리가 있는지 체크, 없으면 만들기
# save_dir = "exc_rate/"
# if not os.path.exists(save_dir):
#     os.mkdir(save_dir)

# file_path = save_dir + fname

# # encoding = 'utf-8-sig' : 엑셀에서 열림
# with open(file_path, "w", newline="", encoding='utf-8-sig') as f:
#   writer = csv.writer(f)
#   writer.writerows(total_data_set)

# # db 연결하기
# conn = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset=charset)
# cur = conn.cursor()

# # 테이블이 존재한다면 삭제
# sql_query ="DROP TABLE IF EXISTS exchange_rate"
# cur.execute(sql_query)

# # cnt_cur 테이블이 존재 하지 않으면 생성
# sql_t1 ="""
# CREATE TABLE IF NOT EXISTS cnt_cur(
# cur_id CHAR(3) NOT NULL PRIMARY KEY, 
# cnt_name VARCHAR(20) NOT NULL
# );
# """
# cur.execute(sql_t1)

# country_datas=[]
# # 2차원 리스트 :  한꺼번에 insert 함
# cur.executemany("INSERT INTO cnt_cur(cur_id, cnt_name) VALUES (%s,%s)", country_datas)

# # exc_rate 테이블이 존재 하지 않으면 생성
# sql_t2 ="""
# CREATE TABLE IF NOT EXISTS exc_rate(
# id int NOT NULL AUTO_INCREMENT PRIMARY KEY,  
# cur_id CHAR(3) NOT NULL, 
# trade_rate FLOAT UNSIGNED NOT NULL,
# cach_buy FLOAT UNSIGNED NOT NULL,
# reg_date VARCHAR(20) NOT NULL,
# FOREIGN KEY (cur_id) references cnt_cur(cur_id)
# );
# """
# cur.execute(sql_t2)

# exchange_rate_datas=[]
# # 2차원 리스트 : exchange_rate_datas 한꺼번에 insert 함
# cur.executemany("INSERT INTO exc_rate(cur_id, trade_rate, cach_buy, reg_date) VALUES (%s,%s,%s,%s)", exchange_rate_datas)

# # db 적용, 트랜젝션 종료
# conn.commit()

# # exc_rate과 cnt_cur을 join해서 조회하기
# # sql_query ="SELECT * FROM exchange_rate_datas"
# # cur.execute(sql_query)
# # print("통화이름\t통화매매률\t현금구매\t날짜")
# # for row in cur.fetchall():
# #    print("{:<5}{:>10.2f}{:>10.2f}{:>24}".format(row[0],row[2],row[3],row[4]))


