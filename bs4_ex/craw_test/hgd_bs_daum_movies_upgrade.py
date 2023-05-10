# 수집할 항목 : 영화 제목, 링크주소, 평점, 예매율, 이미지주소, 개봉일, 입력날짜

import requests as req
from bs4 import BeautifulSoup as bs

import csv
import os
import datetime

import pymysql
from movies_db import *

url = "https://movie.daum.net/ranking/reservation"
res = req.get(url)
soup = bs(res.text, "html.parser")
# print(soup)


def insert():
  sql = """
      INSERT INTO daum_movies VALUES(
              NULL,
              %s,
              %s,
              %s,
              %s,
              %s,
              %s,            
              %s
      );
  """

  cur.executemany(sql, mData)

  conn.commit()

def update(title, grade, res_rate):
  sql = """
      UPDATE daum_movies
      SET title=%s, grade=%s, res_rate=%s
      WHERE title = %s
  """
  result = (title, grade, res_rate, title)
  cur.execute(sql, result)

  conn.commit()

def output():
  sql = """  
  SELECT  title,
          grade,
          res_rate,
          open_date
  FROM daum_movies
  WHERE grade >= 7.0
  ORDER BY grade DESC, res_rate DESC;
  """

  cur.execute(sql)
  print("순서 | 영화제목 | 평점 | 예매율 | 개봉일")
  print("-"*50)
  i = 1
  for row in cur.fetchall():
    #  print(row)
    print(" {:>3} | {:} | {:} | {:}% | {:}".format(i,row[0],row[1],row[2],row[3]))
    i+=1


  


# 시작지점
if __name__ == '__main__':
  conn = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset=charset)
  cur = conn.cursor()


  sql="""
  CREATE TABLE IF NOT EXISTS daum_movies (
    id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    title varchar(60) NOT NULL,
    link_url varchar(50) NOT NULL,
    grade float UNSIGNED,
    res_rate float UNSIGNED,
    img_link varchar(200),
    open_date varchar(10),
    reg_date varchar(20)
  );
  """
  cur.execute(sql)


  reg_date  = datetime.datetime.now()
  reg_date = reg_date.strftime("%Y-%m-%d")

  if not os.path.exists("movies_info"):
      os.mkdir("movies_info")

  fName = "movies_info/daum_" +  reg_date + ".csv"
  file = open(fName, "w", newline="", encoding="UTF-8-sig")


  box = soup.select("div.box_ranking ol.list_movieranking > li > div.item_poster")
  # print(box)
  mData = []



  for movies in box:
      
      # 영화 제목
      mTitle = movies.select_one("div.thumb_cont strong.tit_item a").get_text(strip=True)
      
      # 링크 주소
      link_url = movies.select_one("div.thumb_cont strong.tit_item a").attrs["href"]
      # print(link_url)
      link_url = "https://movie.daum.net" + link_url
      # print(link_url)
      
      # 평점
      grade = movies.select_one("div.thumb_cont span.txt_append span.txt_grade").get_text(strip=True)
      grade = float(grade)
      
      # 예매율
      res_rate = float(movies.select_one("div.thumb_cont span.txt_append span.txt_num").get_text(strip=True).replace("%", ""))
      
      # 이미지 주소
      img_link = movies.select_one("div.poster_movie img").attrs["src"]

      # 개봉 날짜
      open_date = movies.select_one("div.thumb_cont span.txt_info span.txt_num").get_text(strip=True).replace(".", "-")
      # print(open_date)

      # 입력 날짜 = reg_date

      # 2차원 데이터 만들기
      mData.append([mTitle, link_url, grade, res_rate, img_link, open_date, reg_date])
      



  for indata in mData:
    sql = """  
    SELECT  title,
            grade,
            res_rate,
            open_date
    FROM daum_movies
    WHERE title = %s
    """
    title = indata[0]
    grade = indata[2]
    res_rate = indata[3]
    # print(title, grade, res_rate)

    cnt = cur.execute(sql, title)

    if cnt == 0:
      insert()
    elif cnt == 1:
      update(title, grade, res_rate)




  output()
  conn.close()
    

  csv.writer(file).writerows(mData)

