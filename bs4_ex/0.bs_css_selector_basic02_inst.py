html = """<!DOCTYPE html>
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
      <label for="tel">전화번호:</label>
      <input type="text" />
      <b>b태그 넣기</b>
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
"""

# import requests as req
from bs4 import BeautifulSoup as bs
import os
import csv

# url = "http://127.0.0.1:5500/0.bs_css_selector_basic02.html"

# res = req.get(url)
# soup = bs(res.text, "html.parser")

soup = bs(html, "html.parser")

# select문
# arr = soup.select("input:enabled") # select("태그:속성") default 값 - enabled
# print(arr)
# print(type(arr)) # 'bs4.element.ResultSet'

# arr = soup.select("input:disabled") # select("태그:속성")
# print(arr) 
# print(type(arr)) # 'bs4.element.ResultSet'

# arr = soup.select_one("input:disabled") # select("태그:속성")
# print(arr[0]) 
# print(type(arr))

# arr1 = soup.select("input:empty")
# arr2 = soup.select("label + input:empty") # + : 바로 밑에 있는
# print("태그:속성", arr1) 
# print("태그:속성 label", arr2) 
# print(type(arr1))
# print(type(arr2))

# first-child
# arr = soup.select("b:first-child")
# print("first-child", arr)
# print(type(arr))

# arr = soup.select("td b:first-child")
# print("first-child", arr)
# print(type(arr))

# arr = soup.select("tbody b:first-of-type")
# print("b:first-of-type", arr)
# print(type(arr))

# arr = soup.select("tbody td:last-of-type")
# print("b:first-of-type", arr)
# print(type(arr))

# arr = soup.select("tbody td:first-of-type b")
# print("b:first-of-type", arr)
# print(type(arr))

# arr = soup.select("tbody td:nth-child(3)")
# print("nth-child", arr)
# print(type(arr))

# for arrText in arr:
#     print(arrText.get_text(strip=True))

arr = soup.select("tbody tr")
# print("tbody", arr)
# print(type(arr))




if not os.path.exists("test_data"):
    os.mkdir("test_data")

os.makedirs("test_mkdir/", exist_ok=True) # == if not os.path.exists("dir명"): 파일 생성 가능

fname = "test_data/" + "test_to_csv.csv"
f = open(fname, "w", newline="", encoding="UTF-8")
for tdS in arr:
    tdList = []
    # print(test.get_text(strip=True))
#     first = tdS.select_one("td:nth-child(1)").string + ","
#     second = tdS.select_one("td:nth-child(2)").string + ","
#     third = tdS.select_one("td:nth-child(3) b").string
#     third = third.replace(",", "")
    # print("{}{}{}".format(first, second, third))

    num = tdS.select_one("td:nth-child(1)").string
    name = tdS.select_one("td:nth-child(2)").string
    price = tdS.select_one("td:nth-child(3) b").string
    price = price.replace(",", "")
    # print("{},{},{}".format(num, name, price))   

    # last = tdS.select_one("td:nth-child(1)").string + ","
    # last = last + tdS.select_one("td:nth-child(2)").string + ","
    # last = last + tdS.select_one("td:nth-child(3) b").string.replace(",", "")
    # print(last)

#     with open(fname, "a", encoding="UTF-8") as fileAdd:
#         fileAdd.write(last + "\n")
# fileAdd.close()
    tdList.append(num)
    tdList.append(name)
    tdList.append(price)
    
    write = csv.writer(f)
    write.writerow(tdList)
f.close()
    # print(tdList)

with open(fname, "r+", encoding="UTF-8") as file:
    print(file.read())
file.close()

# file = open(fname, "r", encoding="UTF-8")
# readCSV = csv.reader(file)
#     # print(type(file))
# for read in readCSV:
#     print(read)
#     # print(file.close()==True)
# file.close()
# print(file.close()==True)

# td > b
# arr = soup.select("td > b")
# print("td > b", arr)
# print(type(arr))

# b
# arr = soup.select("b")
# print("b", arr)
# print(type(arr))