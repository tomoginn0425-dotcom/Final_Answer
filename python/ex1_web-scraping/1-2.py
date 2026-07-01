from selenium import webdriver
import pandas as pd
import re
import time
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

url = "https://r.gnavi.co.jp/eki/0004718/rs/?fwp=%E5%90%8D%E5%8F%A4%E5%B1%8B&r=1000"

driver.get(url)
time.sleep(3)

shops = driver.find_elements(By.CLASS_NAME, "style_restaurantNameWrap__sOBYs")
shop1_urls = [shop.find_element(By.XPATH, "..").get_attribute("href") for shop in shops]

next_button = driver.find_element(By.CLASS_NAME, "style_nextIcon__Ad_pH")
next_button.click()
time.sleep(3)

shops2 = driver.find_elements(By.CLASS_NAME, "style_restaurantNameWrap__sOBYs")
shop2_urls = [shop2.find_element(By.XPATH, "..").get_attribute("href") for shop2 in shops2]

shop_urls = shop1_urls + shop2_urls

print(len(shop_urls))

results = []

for shop_url in shop_urls:
    driver.get(shop_url)
    time.sleep(3)

    shop_name = driver.find_element(By.ID, "info-name").text

    tel = driver.find_element(By.CLASS_NAME, "number").text
    address = driver.find_element(By.CLASS_NAME, "region").text
    pattern = r"(..?[都道府県])(.*?[市区町村])(.*)"
    match = re.match(pattern, address)

    if match:
        prefecture = match.group(1)
        city = match.group(2)
        street = match.group(3)

    try:
        locality = driver.find_element(By.CLASS_NAME, "locality").text
    except:
        locality = ""

    url_tag = driver.current_url

    ssl = url_tag.startswith("https://")

    try:
        url_tag = driver.find_element(By.CSS_SELECTOR, "a.sv-of.double")
        real_url = url_tag.get_attribute("href")
        time.sleep(3)
    except:
        real_url = ""

    results.append({
                "店舗名": shop_name,
                "電話番号": tel if tel else "",
                "メールアドレス":"",#メールアドレスなかったです
                "都道府県":prefecture,
                "市区町村":city,
                "番地":street,
                "建物名":locality if locality else "",
                "URL":real_url,
                "SSL":ssl,
            })

print(results)

df = pd.DataFrame(results)
df = df.drop_duplicates(subset ="店舗名")
df = df.head(50)

df.to_csv("1-2.csv", index=False, encoding="utf-8-sig")