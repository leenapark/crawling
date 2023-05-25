
# sln
# 1 단계 : 검색된 정보 수집
# - 타이틀, 가격 배송료

# 2 단계 : 무한 스크롤 적용해서 수집
# - 1 페이지의 모든 DOM tree 로드 킴
# - 타이틀, 가격, 배송료

# bs4
# 3 단계 : DOM 트리 구성이 완료 됨

# 4 단계 : 광고 제외 시키기
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager # pip install webdriver-manager
from selenium.webdriver.common.keys import Keys
import time
import os
import csv



# chrome webdriver 
options = webdriver.ChromeOptions()
options.add_argument("window-size=1000,1000");  # 브라우저 크기 설정(가로x세로)
options.add_argument("no-sandbox");   # 샌드박스 사용 안하겠다 탭별로 분리하겠다
# options.add_argument("headless")    # 크롬 창 안뜨게 함
# options.add_experimental_option("excludeSwitches", ["enable-logginf"])  # 

chrome_driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)



url = "https://shopping.naver.com/home"

chrome_driver.get(url)

wait = WebDriverWait(chrome_driver, 10)

def find(wait, css_selector):
  return wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, css_selector)))

search = find(wait, "input[class=_searchInput_search_text_3CUDs]")
val = input("검색어를 입력하세요: ")

search.send_keys(val)
search.send_keys(Keys.ENTER)


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

html = chrome_driver.page_source
soup = bs(html, "html.parser")
# print(soup)
typeNone = type(None)


items = soup.select(".basicList_inner__xCM3J")
objList = []
head = ["title", "price", "delivery fee", "total"]
objList.append(head)
for item in items:
  # print(item)
  # shop_dict = {}


  marketing = item.select_one(".ad_ad_stk__Rfw9m")
  marketing = type(marketing)
  if marketing != typeNone:
     continue


  # title = item.select_one(".basicList_link__JLQJf").get_text(strip=True)
  title = item.select_one("a[class^=basicList_link__JLQJf]").get_text(strip=True)
  # print("title", title)
  price = item.select_one(".price_num__S2p_v").get_text(strip=True).replace(",", "").replace("원", "")
  price = int(price)
  # print("price", price)


  d_fee = item.select_one(".price_delivery__yw_We")
  d_fee_type = type(d_fee)
  if d_fee_type == typeNone:
    d_fee = 0
  else:
    d_fee = d_fee.get_text(strip=True).split("비")[1]
    d_fee = d_fee.strip()
    if d_fee == "무료":
       d_fee = 0
    else:
       d_fee = d_fee.replace(",", "").replace("원", "")
       d_fee = int(d_fee)
  
  total = price + d_fee
  # print(total)
  # shop_dict["title"] = title
  # shop_dict["price"] = price
  # shop_dict["d_fee"] = d_fee
  # shop_dict["total"] = total
  objList.append([title, price, d_fee, total])

# print(objList)

time.sleep(1)

chrome_driver.close()


data_dir = "scrap_data/"

if not os.path.exists(data_dir):
    os.mkdir(data_dir)

fname = f"{data_dir}naver_shopping_{val}.csv"
csvFile = open(fname, "w", newline="", encoding="UTF-8-sig")


csv.writer(csvFile).writerows(objList)

# fname = f"{data_dir}naver_shopping_{val}.json"

# with open(fname, "w", encoding="UTF-8-sig") as f:
#    json.dump(objList, f, indent="\t", ensure_ascii=False)
   


