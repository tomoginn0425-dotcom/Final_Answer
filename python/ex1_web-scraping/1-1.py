import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

urls = ["https://r.gnavi.co.jp/eki/0004718/rs/?fwp=%E5%90%8D%E5%8F%A4%E5%B1%8B&r=1000",
        "https://r.gnavi.co.jp/eki/0004718/rs/?fwp=%E5%90%8D%E5%8F%A4%E5%B1%8B&r=1000&p=2",
        "https://r.gnavi.co.jp/eki/0004718/rs/?fwp=%E5%90%8D%E5%8F%A4%E5%B1%8B&r=1000&p=3",
]

headers = {
    "User-Agent": "Mozilla/5.0"
}

results = []

for i, url in enumerate(urls):
    response = requests.get(url, headers = headers)
    response.encoding = "utf-8"
    html = response.text
    time.sleep(1)

    soup = BeautifulSoup(response.text, "html.parser")

    items = soup.find_all("h2",class_="style_restaurantNameWrap__sOBYs")


    if i == 0:
        for item in items[:30]:
            a_tag = item.find_parent("a")
            shop_url = a_tag["href"]


            shop_response = requests.get(shop_url, headers = headers)#urlに入って情報を取ってくる
            shop_response.encoding = "utf-8"
            html = shop_response.text

            time.sleep(1)

            shop_SOUP = BeautifulSoup(html, "html.parser")

            tel = shop_SOUP.find("span", class_="number")
            address = shop_SOUP.find("span", class_="region").text

            pattern = r"(..?[都道府県])(.*?[市区町村])(.*)"
            match = re.match(pattern, address)

            if match:
                prefecture = match.group(1)
                city = match.group(2)
                street = match.group(3)

            locality = shop_SOUP.find("span",class_="locality")

            url_tag = shop_SOUP.find("a", class_="sv-of double")
            if url_tag:
                homepage_url = url_tag["href"]
            else:
                homepage_url = ""

            ssl = homepage_url.startswith("https://") if homepage_url else ""


            results.append({
                "店舗名": item.text,
                "電話番号": tel.text if tel else "",
                "メールアドレス":"",#メールアドレスなかったです
                "都道府県":prefecture,
                "市区町村":city,
                "番地":street,
                "建物名":locality.text if locality else "",
                "URL":homepage_url,
                "SSL":ssl,
            })
            print("B")

    else:
        for item in items[:30]:
            a_tag = item.find_parent("a")
            shop_url = a_tag["href"]

            shop_response = requests.get(shop_url, headers = headers)
            shop_response.encoding = "utf-8"
            html = shop_response.text
            time.sleep(1)

            shop_SOUP = BeautifulSoup(shop_response.text, "html.parser")

            tel = shop_SOUP.find("span", class_="number")
            address = shop_SOUP.find("span", class_="region").text

            pattern = r"(..?[都道府県])(.*?[市区町村])(.*)"
            match = re.match(pattern, address)

            if match:
                prefecture = match.group(1)
                city = match.group(2)
                street = match.group(3)

            locality = shop_SOUP.find("span",class_="locality")

            url_tag = shop_SOUP.find("a", class_="sv-of double")
            if url_tag:
                homepage_url = url_tag["href"]
            else:
                homepage_url = ""

            ssl = homepage_url.startswith("https://") if homepage_url else ""

            results.append({
                "店舗名": item.text,
                "電話番号": tel.text if tel else "",
                "メールアドレス":"",
                "都道府県":prefecture,
                "市区町村":city,
                "番地":street,
                "建物名":locality.text if locality else "",
                "URL":homepage_url,
                "SSL":ssl,
            })

            print("C")

df = pd.DataFrame(results)
df = df.drop_duplicates(subset ="店舗名")
df = df.head(50)

df.to_csv("1-1.csv", index=False, encoding="utf-8-sig")