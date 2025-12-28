import requests
import pandas as pd
from bs4 import BeautifulSoup

keyword = "nintendo-switch"

url = f"https://lista.mercadolivre.com.br/{keyword}"

headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" }

response = requests.get(url, headers=headers)

if response.status_code == 200:


    soup = BeautifulSoup(response.text, "html.parser")

    search_result = soup.find_all("div", class_="ui-search-result__wrapper")

    data = []

    for result in search_result:
        link = result.find("a", class_="poly-component__title")
        title = result.find("a", class_="poly-component__title").text.strip()
        price = result.find("span", class_="andes-money-amount__fraction").text.strip()
        brand = result.find("span", class_="ui-search-item_title")

        if link:
            link = link.get("href")

        data.append({
            "title": title,
            "price": price,
            "link": link
        })

    print(data)

else:
    print("Error")