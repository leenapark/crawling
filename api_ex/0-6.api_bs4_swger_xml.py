import requests as req
from my_info import *

#  'https://api.odcloud.kr/api/15101505/v1/uddi:76379618-5faa-42c0-9eca-e5ec9c9275df?page=1&perPage=10&returnType=xml&serviceKey=Dibt7eA3UUZSfQH8r2nYBiJPGDUvL9QAs39eO%2FxDRbC3m8QAwLWwLdyEkev7pWYEn52bUgDgUZSTkr4s9xkG0Q%3D%3D' \
url_path = 'https://api.odcloud.kr/api/15101505/v1/uddi:76379618-5faa-42c0-9eca-e5ec9c9275df'
page = 1
perPage = 10
request = "?page=" + str(page) + "&perPage=" + str(perPage) + "&returnType=xml&serviceKey="
url_path = url_path + request
servicekey = 'Dibt7eA3UUZSfQH8r2nYBiJPGDUvL9QAs39eO%2FxDRbC3m8QAwLWwLdyEkev7pWYEn52bUgDgUZSTkr4s9xkG0Q%3D%3D'
url = url_path + servicekey

res = req.get(url)
print(res.text)