import requests as req
from bs4 import BeautifulSoup as bs
import datetime
import os
import csv

url = "https://finance.naver.com/marketindex/exchangeList.naver"
res = req.get(url)
soup = bs(res.text, "html.parser")
# print(soup)
td = datetime.datetime.today()
td = td.strftime("%Y-%m-%d-%H")
# country = soup.select("body wrap div#container div#content div.section_exchange iframe#frame_ex1 div#section_ex1 table.tbl_exchange tbody tr td.tit")
# country = soup.select("body .tbl_area table.tbl_exchange tbody tr td.tit a")
# print(country)
# currency = soup.select("body table.tbl_exchange tbody tr td.sale")
# print(currency)
if not os.path.exists("exchange_rate"):
    os.mkdir("Exchange_Rate")

fName = "exchange_rate/" + td + ".csv"
file = open(fName, "w", newline="", encoding="UTF-8-sig")

arr = soup.select("body table.tbl_exchange tbody tr")



for curName in arr:
    data = []
    # cur = curName.select_one("td:nth-child(2)").get_text(strip=True).replace(",", "")
    # cName = curNam=e.select_one("td:nth-child(1)").get_text(strip=True) + ","
    # cName = cName + cur
    # print(cName)

    cName = curName.select_one("td:nth-child(1)").get_text(strip=True)
    cur = curName.select_one("td:nth-child(2)").get_text(strip=True).replace(",", "")
    data.append(cName)
    data.append(cur)

    write = csv.writer(file)
    write.writerow(data)
file.close()

# for cName in country:
#     ctName = cName.get_text(strip=True)

# for cur in currency:
#     curr = cur.get_text(strip=True).replace(",", "")
    # print(curr)
