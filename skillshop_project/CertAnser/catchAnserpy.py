from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import requests
import time
import re
import unicodedata
import csv
import json

Anser_host = "https://www.gcertificationcourse.com/"
AnserUrl = ["youtube-music-rights-management-certification-answers","youtube-music-assessment-answers"]
MainList = []

for fqdn in AnserUrl:
    response = requests.get(Anser_host+fqdn)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        all_links = soup.select("div.entry-content ol li a")
        for linkText in all_links:
            ChilList = []
            # print(linkText.get_text())
            ChilList.append(linkText.get_text())
            link_url = linkText.get('href')
            response = requests.get(link_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                strong_texts_in_li = [strong.get_text() for li in soup.find_all('li') for strong in li.find_all('strong')]
                ChilList.append(strong_texts_in_li)
                MainList.append(ChilList)
                # print(MainList)

    with open(f"{fqdn}.json", "w", encoding="utf-8") as file:
        json.dump(MainList, file, ensure_ascii=False, indent=4)

    print(f"{fqdn}.csv Write")
