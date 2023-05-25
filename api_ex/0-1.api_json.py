
import requests
from my_info import *

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
print(response.content)