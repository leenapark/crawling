from selenium import webdriver
import time

chrome = webdriver.Chrome("./chromedriver/chromedriver")

url = "https://www.naver.com/"
chrome.get(url)

time.sleep(5)
chrome.close()