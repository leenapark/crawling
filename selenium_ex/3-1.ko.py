# 네이버 쇼핑에서
# "아이폰 케이스" 검색어 입력
# 검색 버튼 클릭


# 2 단계 : 무한 스크롤 적용해서 수집
# - 1 페이지의 모든 DOM tree 로드 킴
# - 타이틀, 가격, 배송료

# 3 단계 : 광고 아이템 제외

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager # pip install webdriver-manager
from selenium.webdriver.common.keys import Keys
import time
import json
import os
import pymongo
from mydb_info import *



# chrome webdriver 
options = webdriver.ChromeOptions()
options.add_argument("window-size=1000,1000");  # 브라우저 크기 설정(가로x세로)
options.add_argument("no-sandbox");   # 샌드박스 사용 안하겠다 탭별로 분리하겠다
# options.add_argument("headless")    # 크롬 창 안뜨게 함
# options.add_experimental_option("excludeSwitches", ["enable-logginf"])  # 

chrome_driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)



url = "https://www.kobis.or.kr/kobis/business/stat/boxs/findRealTicketList.do"

chrome_driver.get(url)


# checkBox = chrome_driver.find_element("input[name=repNationNoKor]")

wait = WebDriverWait(chrome_driver, 10)



# wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "input[id=repNationNoKor]")))


# css_selector = "input[id=repNationNoKor]"
def find(wait, css_selector):
  return wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, css_selector)))

checkBox = find(wait, "label[for=repNationNoKor]")
checkBox.click()
search = find(wait, "button[class=btn_blue]")
search.click()


SCROLL_PAUSE_TIME = 3
last_height = chrome_driver.execute_script("return document.body.scrollHeight")    # Get scroll height

while True:
    # Scroll down to bottom
    chrome_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = chrome_driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

heads = chrome_driver.find_elements(By.CSS_SELECTOR, ".tbl_comm thead tr th")
for head in heads:
  head_t = head.text


body = chrome_driver.find_elements(By.CSS_SELECTOR, "tbody #tr_")
rankList = []
for item in body:
   rank_dic = {}
  #  title = item.find_element(By.CSS_SELECTOR, ".tal span.ellip a").text
  #  print(title)
  #  td = item.find_elements(By.CSS_SELECTOR, "td")
   title = item.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text
   opening_date = item.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text
   reservation = item.find_element(By.CSS_SELECTOR, "td:nth-child(4)").text.replace("%", "")
   sales_money = item.find_element(By.CSS_SELECTOR, "td:nth-child(5)").text.replace(",", "")
  #  print(title, opening_date, float(reservation), int(sales_money))

  #  for m_data in td:
   rank_dic["title"] = title
   rank_dic["opening_date"] = opening_date
   rank_dic["reservation"] = float(reservation)
   rank_dic["sales_money"] = int(sales_money)
   rankList.append(rank_dic)
  
chrome_driver.close()


try:
  conn = pymongo.MongoClient(db_info)

  # movies DB생성
  kobis = conn.kobis

  # obj_info 컬렉션 생성
  kobis_rank = kobis.kobis_rank

  kobis_rank.insert_many(rankList)

except Exception as e:
    result = "DB connect error : " + str(e)
    # return result
else:
    result =  kobis_rank.find()

for info in result:
   print(info)


time.sleep(1)
