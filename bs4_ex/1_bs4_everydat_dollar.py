import requests as req
from bs4 import BeautifulSoup as bs
import datetime
import os

url = "https://finance.naver.com/marketindex/"
res = req.get(url)
soup = bs(res.text, "html.parser")
# urllib : python 내장 library
# res = req.urlopen(url)
# soup = bs(res, "html.parser")

# select : 지정한 태그 값을 모두 가져옴
# 사용 : list 사용법과 같음 변수명[n]
# price = soup.select("div.market1 div.head_info span.value")
# select_one : 첫번째 것을 가져옴
# 사용 : list 형 X 
price = soup.select_one("div.market1 div.head_info span.value") # 'bs4.element.Tag'
price_one = soup.select_one("div.market1 div.head_info span.value").string # .text .string 사용 가능
# print(price.text)
# print(price_one)
# print(type(price)) # 'bs4.element.ResultSet'
price_one = price_one.replace(",", "")
print(price_one)
td = datetime.datetime.today()
td = td.strftime("%Y-%m-%d-%H")


# 문제1 : dollar_data
# 폴더에 파일 저장
if not os.path.exists("dollar_data"):
    os.mkdir("dollar_data")

fname = "dollar_data/" + td + ".csv"
with open(fname, "w", encoding="UTF-8") as file:
    file.write(td + "," + price_one)