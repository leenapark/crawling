# chrome driver 다양한 옵션 살펴보기

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager # pip install webdriver-manager
import time


# chrome webdriver 
options = webdriver.ChromeOptions()
options.add_argument("window-size=1000,1000");  # 브라우저 크기 설정(가로x세로)
options.add_argument("no-sandbox");   # 샌드박스 사용 안하겠다 탭별로 분리하겠다
# options.add_argument("headless")    # 크롬 창 안뜨게 함
# options.add_experimental_option("excludeSwitches", ["enable-logginf"])  # 

# 실행될 때 인터넷을 통해서 ChromeDriver 설치 및 실행
# brawser 버전은 자동으로 업데이트 되기 때문에 driver 라이브러리 사용
chrome_driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
# chrome = webdriver.Chrome(chrome_path, options=options)


url1 = "https://www.naver.com/"
url2 = "https://shopping.naver.com/home"

chrome_driver.get(url1)
# 1. python 내장 time 라이브러리로 슬립 이용 : time.sleep(초)
# time.sleep(2)

# 2. chrome
# chrome.implicitly_wait()

# time.sleep(5)

# 3. WebDriverWait, expected_conditions 로 원하는 요소가 로딩될 때까지 스마트하게 기다림(delay)
# WebDriverWait(크롬 드라이버 변수, 기다리는 시간).until(EC.presence_of_element_located: 그 위치에 나타날 때까지 기다림((By.CSS_SELECTOR, "input[name-query]")))
# WebDriverWait(chrome, 10).until(ec.presence_of_element_located((By.CSS_SELECTOR, "input[name-query]"))) # (By.CSS_SELECTOR, "input[name-query]") : 튜플 형식으로 만들어서 사용
# search = chrome.find_element(By.CSS_SELECTOR, "형식: tag or css slector")
# search = chrome.find_element(By.CSS_SELECTOR, "input[id=query]")
# search.send_keys("슬램덩크\n")
# time.sleep(5)
# 클릭 이벤트 실행


# 방법2
wait = WebDriverWait(chrome_driver, 10)

def find(wait, css_selector):
  return wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, css_selector)))

search = find(wait, "input[id=query]")
search.send_keys("슬램덩크\n") #  이벤트 발생

time.sleep(5)

chrome_driver.close()

# 브라우저 전체
# chrome.quit()