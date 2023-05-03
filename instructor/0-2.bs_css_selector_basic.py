html = '''<!DOCTYPE html>
<html lang="en">
<head>
  <style>
    table{
      border-collapse: collapse;
      border:1px solid black;
    }
    table td, table th{
      border: 1px solid black;
    }
    table tr:first-child th{
      border-top: 0;
    }
    table tr:last-child td {
      border-bottom: 0;
    }
    table tr td:first-child,
    table tr th:first-child{
      border-left: 0;
    }
    table tr td:last-child,
    table tr th:last-child{
      border-right: 0;
    }
  </style>

</head>
<body>
  <div style="max-width: 960px; margin: auto; padding-top:20px;">
    <h1>호텔 예약 확인</h1>
    <input type="checkbox" />
    <span>이용 약관을 충분히 숙지하였으며 이에 동의합니다.</span>
    <br>
    <input type="checkbox" checked />
    <span> 14세 이상 보호자 동행에 동의합니다.</span>
    <br>
    <input type="checkbox" disabled />
    <span>5인 이상 단체 예약입니다.</span>
    <br>
    <div>
      <b>김경하</b>
      <label for="tel">전화번호:</label>
      <input type="text" />
    </div>
    <br>
    <table>
      <thead>
        <tr>
          <th>번호</th>
          <th>이름</th>
          <th>가격</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>1</td>
          <td>김철수</td>
          <td>
            <b>120,000</b>
          </td>
        </tr>
        <tr>
          <td>2</td>
          <td>이영희</td>
          <td>
            <b>200,000</b>
          </td>
        </tr>
        <tr>
          <td>3</td>
          <td>김서영</td>
          <td>
            <b>250,000</b>
          </td>
        </tr>
        <tr>
          <td>4</td>
          <td>서정희</td>
          <td>
            <b>300,000</b>
          </td>
        </tr>
      </tbody>
    </table>
    <h3>총 가격</h3>
    <div>
      <b>KRW : </b>
      <b>850,000</b>
    </div>
  </div>
</body>
</html>
'''
from bs4 import BeautifulSoup as BS
url = "http://127.0.0.1:5500/0-2.bs_css_selector_basic02.html"

# import requests as req
# res = req.get(url)
# soup = BS(res.text, "html.parser")

soup = BS(html, "html.parser")
# 셀렉터 태그:속성
# 셀렉터 input:enabled
# arr = soup.select("input:enabled")
# print("태그:속성1", arr)

#disabled
# arr = soup.select("input:disabled")
# print("태그:속성2",arr[0])

#checked
# arr = soup.select("input:checked")
# print("태그:속성3",arr)

#empty
# arr1 = soup.select("input:empty")
# arr2 = soup.select("label + input:empty")
# print("태그:속성4", arr1)
# print("태그:속성5", arr2)

#first-child
arr = soup.select("td b:first-child")
# print("태그:첫번째요소", arr)

#first-of-type
# arr = soup.select("td b:first-of-type")
# print(arr)

# arr = soup.select("tbody td:first-of-type")
# print(arr)

# arr = soup.select("tbody td:last-of-type b")
# print(arr)

# nth-child()
# arr = soup.select("tbody td:nth-child(3)")
# print(arr)

# text만 추출
# arr = soup.select("tbody td:nth-child(3)")
# print(arr.text)

# 문제1 : 번호, 이름, 가격을 따로 추출하기
# select를 어떻게 지정해야할까?
arrs = soup.select("tbody tr")
import csv 
import os

fname = "test2.csv"
save_dir = "test-data/"
if not os.path.exists(save_dir):
    os.mkdir(save_dir)
# 파일 저장 위치 + 파일 이름
file_path = save_dir + fname

# newline="" : windows에서 csv 파일에 공백라인 생성 문제 해결하기
f = open(file_path, "w", newline="", encoding = 'utf8')
for arr in arrs:
  # print(arr)
  data = []
  num = arr.select_one("td:nth-child(1)").text
  name = arr.select_one("td:nth-child(2)").text
  price = arr.select_one("td:nth-child(3) b").text
  price = price.replace(",", "")
  # print(f"{num}, {name}, {price}")
    
  f.write(f"{num}, {name}, {price}\n")
f.close()
# print(arr.text)
# 출력형태
# 1, 김철수, 120000
# 2, 이영희, 200000
# ==================
# file저장하기
# csv 파일로 저장
# 폴더이름 : test_data/
# 파일이름 : test.csv




