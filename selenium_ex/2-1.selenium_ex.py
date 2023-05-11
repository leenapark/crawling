# 네이버 쇼핑에서
# "아이폰 케이스" 검색어 입력
# 검색 버튼 클릭

# 1 단계 : 검색된 정보 수집
# - 타이틀, 가격 배송료

# 2 단계 : 무한 스크롤 적용해서 수집
# - 1 페이지의 모든 DOM tree 로드 킴
# - 타이틀, 가격, 배송료

# 3 단계 : 광고 아이템 제외

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

chrome_driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)




url = "https://shopping.naver.com/home"

chrome_driver.get(url)

wait = WebDriverWait(chrome_driver, 10)

def find(wait, css_selector):
  return wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, css_selector)))

button = find(wait, "input[class=_searchInput_search_text_3CUDs]")
button.send_keys("아이폰 케이스\n") #  이벤트 발생


#### selenium v4
# driver.find_element(By.XPATH, '//button[text()="Some text"]')
# driver.find_element(By.XPATH, '//button')
# driver.find_element(By.ID, 'loginForm')
# driver.find_element(By.LINK_TEXT, 'Continue')
# driver.find_element(By.PARTIAL_LINK_TEXT, 'Conti')
# driver.find_element(By.NAME, 'username')
# driver.find_element(By.TAG_NAME, 'h1')
# 요소 1개 : 텍스트 반환
# driver.find_element(By.CLASS_NAME, 'content')
# 요소 여러개 : 리스트 반환
# driver.find_element(By.CSS_SELECTOR, 'p.content')

#### 다양한 엘리먼트 얻는 방법 : selenium v3
#chrome.find_element_by_css_selector()
#chrome.find_elements_by_css_selector()
#chrome.find_elements_by_class_name()
#chrome.find_element_by_class_name()
#chrome.find_element_by_id()
#chrome.find_elements_by_id()

time.sleep(10)

chrome_driver.close()

# 브라우저 전체
# chrome.quit()