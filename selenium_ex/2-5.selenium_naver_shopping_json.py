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
# input_val = chrome_driver.find_element("._searchInput_search_text_3CUDs")
# val = input_val.get_attribute("value")
search.send_keys(val)
search.send_keys(Keys.ENTER)


# search.send_keys("아이폰 케이스") #  이벤트 발생
# button = find(wait, "button._searchInput_button_search_1nlaw")
# button.click()

#2. driver.implicitly_wait(초) -- 다시 확인 필요
# 웹 페이지의 로딩이 완료될때까지 기다리는 함수, 초:최대 기다리는 시간
# driver.implicitly_wait(5)

time.sleep(1)

# 1 단계 : 검색된 정보 수집
# - 타이틀, 가격 배송료
# item 목록 css selector : .basicList_inner__xCM3J

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
  # titleList = []
  # priceList = []
  # d_feeList = []
  # totalList = []
  try:
    # 3 단계 : 광고 아이템 제외
    marketing = item.find_element(By.CSS_SELECTOR, ".ad_ad_stk__Rfw9m").text
    # print("market", marketing)

  # 2 단계 : 무한 스크롤 적용해서 수집
  # - 1 페이지의 모든 DOM tree 로드 킴
  # - 타이틀, 가격, 배송료
  # link title : .basicList_link__JLQJf , basicList_title__VfX3c a
  # title = item.find_element(By.CSS_SELECTOR, ".basicList_link__JLQJf").text
    continue
  except:
    pass
  title = item.find_element(By.CSS_SELECTOR, ".basicList_title__VfX3c a").text
  # print("title", title)
  price = item.find_element(By.CSS_SELECTOR, ".price_num__S2p_v").text.replace(",", "").replace("원", "")
  # print("price", price)

  try:
    d_fee = item.find_element(By.CSS_SELECTOR, ".price_delivery__yw_We").text.split("\n")[1].replace(",", "").replace("원", "")
    # print("d_fee", d_fee)
    # if "무료" in d_fee:
    if not d_fee.isdigit():
      d_fee = 0
  except:
      d_fee = 0
  
  total = int(price) + int(d_fee)
  # print("total", round(total))
  # objList.append([title, int(price), int(d_fee), total])
  # print("objList", objList)
  # titleList.append(title)
  # priceList.append(price)
  # d_feeList.append(d_fee)
  # totalList.append(total)
  
  # shop_dict["objList"] = objList
  shop_dict["title"] = title
  shop_dict["price"] = price
  shop_dict["d_fee"] = d_fee
  shop_dict["total"] = total
  # shop_dict["title"] = titleList
  # shop_dict["price"] = priceList
  # shop_dict["d_fee"] = d_feeList
  # shop_dict["total"] = totalList
  # shop_dict["objList"] = objList
  objList.append(shop_dict)

# print("dict", shop_dict)
# print("list", objList)
# json_val = json.dumps(objList, ensure_ascii=False)
# print("json", json_val)
# print(type(json_val))

# 요소 1개 : 텍스트 반환
# driver.find_element(By.CLASS_NAME, 'content')
# 요소 여러개 : 리스트 반환
# driver.find_element(By.CSS_SELECTOR, 'p.content')


time.sleep(10)

chrome_driver.close()


   

# 브라우저 전체
# chrome.quit()



