import requests
import json
import csv

ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
headers = {'User-Agent': ua}

columns = ['Category Name','Retail Name','Retail Price']
with open ('Carrefour_top.csv','w', newline='', encoding='ANSI') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(columns)

for i in range(1,70):
    data = {
            'newHomePageId':'376',
            'orderBy': '21',
            'pageIndex': str(i),
            'pageSize': '30',
            }
    res = requests.post('https://online.carrefour.com.tw/ProductShowcase/Catalog/GetNewHomePageTitleProductsJson' ,headers = headers, data = data)
    result = json.loads(res.text)
    for i in range (0,19):
        try:
            product_name = result["content"]["ProductListModel"][i]['Name']
            product_price = result["content"]["ProductListModel"][i]['Price']
            category_name = result["content"]["ProductListModel"][i]['StrCategory']
            print(product_name,product_price+'元' ,sep='  ')
            print(product_price)
            print(category_name)

            insert_data=[category_name,product_name,product_price]
            with open('Carrefour_top.csv', 'a', newline='', encoding='ANSI') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(insert_data)
        except :
            pass
            print("==================end======================")
