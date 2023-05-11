# 네이버 쇼핑에서
# "아이폰 케이스" 검색어 입력
# 검색 버튼 클릭 - 참고 코드
# button = find(wait, "셀렉터")
# button.click()

# 1단계: 검색된 정보 수집
# - 타이틀, 가격, 배송료

# 2단계: 무한스크롤 적용해서 수집
# - 1 페이지의 모든 DOM 트리를 로드킴
# - 타이틀, 가격, 배송료

# 3단계: 광고 아이템은 제외시키기

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time  
import os

options = webdriver.ChromeOptions()             # 옵션 설정 객체 생성
options.add_argument("window-size=1000,800")   # 브라우저 크기 설정(가로 x 세로)
options.add_argument("no-sandbox")              # 샌드박스 사용 안하겠다. 텝별로 분리하겠다. 거리를 두겠다
# options.add_argument("headless")              # 크롬 창을 안뜨게함.
options.add_experimental_option("excludeSwitches", ["enable-logging"]) 

# 다운로드 받은 크롬드라이버 실행
driver_path = "./chromedriver/chromedriver"
driver = webdriver.Chrome(driver_path, options=options)

# 자동으로 브라우저 버전에 맞게 드라이버를 셋팅해줌
# driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

url = "http://shopping.naver.com"
driver.get(url)
wait = WebDriverWait(driver, 10) 

def find(wait, css_selector):
  return wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))

# 사람이 하는 행동 로직을 그대로 재현해서 크롤이하는 방법
search = find(wait, "input[title='검색어 입력']")

key_word = input("검색어를 입력하세요. : ")
# search.send_keys("아이폰 케이스\n")
search.send_keys(key_word)
search.send_keys(Keys.ENTER)
# button = find(wait, "button._searchInput_button_search_1n1aw")
# button.click()

time.sleep(1)

# 네이버쇼핑 검색결과 : 1page가 모두 DOM tree로 만들기 위해서
# 페이지 최하단까지 스크롤
SCROLL_PAUSE_TIME = 3
last_height = driver.execute_script("return document.body.scrollHeight")    # Get scroll height

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height


# 1단계: 검색된 정보 수집
# - 타이틀, 가격, 배송료
# item 목록 css 셀렉터 : .basicList_inner__xCM3J
items = driver.find_elements(By.CSS_SELECTOR, ".basicList_inner__xCM3J")
datas_list = []
for item in items:
  data_dict = {}
  # print(item)
  # print(item.text)

  # 광고 filtering 하기-광고 데이터는 수집 안함
  try:
    # 광고 요소 찾기 : button.ad_ad_stk__Rfw9m
    item.find_element(By.CSS_SELECTOR, "button.ad_ad_stk__Rfw9m")
    continue
  except:
    pass

  # 제목: title
  # .basicList_title__VfX3c a 텍스트
  title = item.find_element(By.CSS_SELECTOR, ".basicList_title__VfX3c a").text
  price = item.find_element(By.CSS_SELECTOR, ".price_price__LEGN7 span.price_num__S2p_v").text
  # 원제거, ','제거
  price = price.replace(",","").rstrip("원")
  # 지정 요소가 없을 경우 selenium은 error(프로그램종료)가 발생하기 때문에 
  # try: ~ except: -> 예외 처리를 해야 종료되지 않음
  try:
    deli_price = item.find_element(By.CSS_SELECTOR, ".price_delivery__yw_We").text
    deli_price = deli_price.split("\n")[-1]
    # 원제거, ','제거
    deli_price = deli_price.replace(",","").rstrip("원")
    # if deli_price == "무료" :
    # 숫자가 아닐경우, 0으로 대체
    if not deli_price.isdigit() :
      deli_price = 0
  except:
     deli_price=0
     pass

  print(title)
  # print(price)
  # print(deli_price)

  # print(f"상품가격 {price}, 배송비 {deli_price}, 총합계 : {int(price) + int(deli_price)}")

  data_dict["항목"] = title
  data_dict["가격"] = price
  data_dict["배송비"] = deli_price
  data_dict["총비용"] = int(price) + int(deli_price)
  print(data_dict)
  print("-"*30)
  datas_list.append(data_dict)

print("="*30)
print(datas_list)

# time.sleep(1)
driver.close()
# json 파일로 데이터 저장
import json
import os

data_dir = "scrap_data/"
if not os.path.exists(data_dir):
   os.mkdir(data_dir)

# file 이름
file_path = f"{data_dir}naver_shopping_{key_word}.json"

with open(file_path, "w", encoding="utf-8") as f:
   json.dump(datas_list, f, indent="\t", ensure_ascii=False)


# 요소 1개 : 텍스트 반환
# driver.find_element(By.CSS_SELECTOR, 'p.content')
# 요소 여러개 : 리스트 반환
# driver.find_elements(By.CSS_SELECTOR, 'p.content')
