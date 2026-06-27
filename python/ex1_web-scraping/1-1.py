import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

urls = ["https://r.gnavi.co.jp/eki/0004718/rs/?fwp=%E5%90%8D%E5%8F%A4%E5%B1%8B&r=1000",
        "https://r.gnavi.co.jp/eki/0004718/rs/?fwp=%E5%90%8D%E5%8F%A4%E5%B1%8B&r=1000&p=2"
]

headers = {
    "User-Agent": "Mozilla/5.0"
}

results = []

for i, url in enumerate(urls):
    response = requests.get(url, headers = headers)
    response.encoding = "utf-8"
    html = response.text
    time.sleep(3)

    soup = BeautifulSoup(response.text, "html.parser")

    items = soup.find_all("h2",class_="style_restaurantNameWrap__sOBYs")


    if i == 0:
        for item in items[:30]:
            a_tag = item.find_parent("a")
            shop_url = a_tag["href"]

            shop_response = requests.get(shop_url, headers = headers)
            shop_response.encoding = "utf-8"
            html = shop_response.text
            time.sleep(3)

            shop_SOUP = BeautifulSoup(shop_response.text, "html.parser")

            shop_items = shop_SOUP.find_all("span", class_="number")

            results.append({
                "名前": item.text,
                "TEL": [shop_item.text for shop_item in shop_items]
            })
            print("B")
    else:
        for item in items[:20]:
            a_tag = item.find_parent("a")
            shop_url = a_tag["href"]

            shop_response = requests.get(shop_url, headers = headers)
            shop_response.encoding = "utf-8"
            html = shop_response.text
            time.sleep(3)

            shop_SOUP = BeautifulSoup(shop_response.text, "html.parser")

            shop_items = shop_SOUP.find_all("span", class_="number")

            results.append({
                "名前": item.text,
                "TEL": [shop_item.text for shop_item in shop_items]
            })

            print("A")

print(results)