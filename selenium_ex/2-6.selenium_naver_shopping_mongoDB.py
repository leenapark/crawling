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
options.add_experimental_option("excludeSwitches", ["enable-logginf"])  # 

driver_path = "./chromedriver/chromedriver"
chrome_driver = webdriver.Chrome(driver_path, options=options)
# chrome_driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)



url = "https://shopping.naver.com/home"

chrome_driver.get(url)

wait = WebDriverWait(chrome_driver, 10)

def find(wait, css_selector):
  return wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, css_selector)))

search = find(wait, "input[class=_searchInput_search_text_3CUDs]")
val = input("검색어를 입력하세요: ")

search.send_keys(val)
search.send_keys(Keys.ENTER)

# driver.implicitly_wait(5)

time.sleep(1)


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


items = chrome_driver.find_elements(By.CSS_SELECTOR, ".basicList_inner__xCM3J")
objList = []
for item in items:
  shop_dict = {}
  # print(item)
  # error = item.find_element(By.CSS_SELECTOR, "button.ad_ad_stk__Rfw9m")
  # print(error)
  try:
    item.find_element(By.CSS_SELECTOR, "button.ad_ad_stk__Rfw9m")
    continue
  except Exception as e:
    # print("error!!!!", e)
    pass

  title = item.find_element(By.CSS_SELECTOR, ".basicList_title__VfX3c a").text
  # print("title", title)
  price = item.find_element(By.CSS_SELECTOR, ".price_num__S2p_v").text.replace(",", "").replace("원", "")
  # print("price", price)

  try:
    d_fee = item.find_element(By.CSS_SELECTOR, ".price_delivery__yw_We").text.split("\n")[1].replace(",", "").replace("원", "")
    if not d_fee.isdigit():
      d_fee = 0
  except:
      d_fee = 0
      pass
  
  total = int(price) + int(d_fee)
  shop_dict["title"] = title
  shop_dict["price"] = price
  shop_dict["d_fee"] = d_fee
  shop_dict["total"] = total
  objList.append(shop_dict)


# time.sleep(10)

chrome_driver.close()

data_dir = "scrap_data/"

if not os.path.exists(data_dir):
    os.mkdir(data_dir)

fname = f"{data_dir}naver_shopping_{val}.json"

with open(fname, "w", encoding="UTF-8-sig") as f:
   json.dump(objList, f, indent="\t", ensure_ascii=False)
   


# mongoDB

try:
  conn = pymongo.MongoClient(db_info)

  # naver_shop DB생성
  naver_shop = conn.naver_shop

  # obj_info 컬렉션 생성
  obj_info = naver_shop.obj_info

  obj_info.insert_many(objList)

except Exception as e:
    result = "DB connect error : " + str(e)
    # return result
else:
    result =  obj_info.find()

for info in result:
   print(info)
