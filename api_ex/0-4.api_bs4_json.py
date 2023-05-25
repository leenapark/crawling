
import requests
from my_info import *
from bs4 import BeautifulSoup as bs
import json

url = 'http://apis.data.go.kr/B552061/frequentzoneOldman/getRestFrequentzoneOldman'
params ={
    'serviceKey' : ServiceKey,
    'searchYearCd' : '2020',
    'siDo' : '11',
    'guGun' : '320',
    'type' : 'json',
    'numOfRows' : '10',
    'pageNo' : '1'
    }

response = requests.get(url, params=params)
# print(response.content)
soup = bs(response.content, "html.parser")
# print(soup.prettify())

json_data = json.loads(soup.text)
addrs = json_data["items"]["item"]
# print(addrs)
for addr in addrs:
    print(addr['spot_nm'])