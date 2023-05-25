import requests as req
from my_info import *
from bs4 import BeautifulSoup as bs
import os
import csv


url = 'http://apis.data.go.kr/6300000/animalDaejeonService/animalDaejeonList'
servicekey = 'Dibt7eA3UUZSfQH8r2nYBiJPGDUvL9QAs39eO/xDRbC3m8QAwLWwLdyEkev7pWYEn52bUgDgUZSTkr4s9xkG0Q=='
# params ={
#     'serviceKey' : '서비스키',
#     'pageNo' : '1',
#     'numOfRows' : '10',
#     'searchCondition' : '1(개)',
#     'searchCondition2' : '1(동구)',
#     'searchCondition3' : '1(공고중)',
#     'species' : '진도',
#     'memo' : '콧물',
#     'regId' : '123-1',
#     'gubun' : '수,암',
#     'searchKeyword' : '개,콧물감기'
#     }

# params = {
#     'serviceKey' : servicekey,
#     'pageNo' : '1', 
#     'numOfRows' : '10', 
#     'searchCondition' : '2', 
#     'searchCondition2' : '1', 
#     'searchCondition3' : '1', 
#     'species' : '코리안숏헤어', 
#     'memo' : '나이', 
#     'regId' : '1', 
#     'gubun' : '1', 
#     'searchKeyword' : '고양이'
# }
# params = {
#     'serviceKey' : servicekey,
#     'pageNo' : '1', 
#     'numOfRows' : '10', 
#     'searchCondition' : '2', 
#     'searchCondition2' : '2', 
#     'searchCondition3' : '1', 
#     'species' : '코리안숏헤어', 
#     'gubun' : '1', 
#     'searchKeyword' : '고양이'
# }

params = {
    'serviceKey' : servicekey,
    'pageNo' : '1', 
    'numOfRows' : '10', 
    'searchCondition' : '1', 
    'searchCondition2' : '1', 
    'searchCondition3' : '1', 
    'species' : '진도', 
    'memo' : '콧물', 
    'regId' : '123-1', 
    'gubun' : '1', 
    'searchKeyword' : '개'
}

response = req.get(url, params=params)
soup = bs(response.text, "html.parser")
dogs = soup.select("items")
dogList = []
head = ["adoption status", "animal", "age", "gender"]
dogList.append(head)
for dog_info in dogs:
    ado_num = dog_info.select_one("adoptionstatuscd").get_text(strip=True)
    # 1:공고중,2:입양가능,3:입양예정,4:입양완료,7:주인반환
    if ado_num == "1":
        dog_ado = "공고 중"
    elif ado_num == "2":
        dog_ado = "입양 가능"
    elif ado_num == "3":
        dog_ado = "입양 예정"
    elif ado_num == "4":
        dog_ado = "입양 완료"
    else:
        dog_ado = "주인 반환"
    classification = dog_info.select_one("classification").get_text(strip=True)  
    if 	classification == "1":
        classification = "강아지"
    elif classification == "2":
        classification = "고양이"
    else:
        classification = "다른 동물"
    age = dog_info.select_one("age").get_text(strip=True).split("년")[0]
    age = int(age)
    gender = dog_info.select_one("gender").get_text(strip=True)
    if gender == "1":
        gender = "암"
    elif gender == "2":
        gender = "수"
    print(dog_ado, classification, age, gender)
    dogList.append([dog_ado, classification, age, gender])
print(dogList)

data_dir = "data/"

if not os.path.exists(data_dir):
    os.mkdir(data_dir)

fname = data_dir + "유기동물.csv"
csvFile = open(fname, "w", newline="", encoding="UTF-8-sig")


csv.writer(csvFile).writerows(dogList)
# test = soup.get_text(strip=True)
# print("test", test)