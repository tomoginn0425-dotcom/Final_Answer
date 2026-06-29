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
    print(i,url)