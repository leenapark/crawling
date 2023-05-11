# chrome driver 다양한 옵션 살펴보기

from selenium import webdriver
import time

chrome_path = "./chromedriver/chromedriver"

# chrome webdriver 
options = webdriver.ChromeOptions()
options.add_argument("window-size=1000,1000");  # 브라우저 크기 설정(가로x세로)
options.add_argument("no-sandbox");   # 샌드박스 사용 안하겠다 탭별로 분리하겠다
# options.add_argument("headless")    # 크롬 창 안뜨게 함
# options.add_experimental_option("excludeSwitches", ["enable-logginf"])  # 

chrome = webdriver.Chrome(chrome_path, options=options);


url1 = "https://www.naver.com/"
url2 = "https://shopping.naver.com/home"

chrome.get(url1)
chrome.get(url2)
chrome.back()
time.sleep(2)
chrome.forward()
time.sleep(2)

time.sleep(5)
chrome.close()

# 브라우저 전체
# chrome.quit()