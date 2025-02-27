import os
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import requests
import time
import re

UserName = "資料夾名稱"
FolderName = "證照檔\\"+UserName

with sync_playwright() as p:
    acount = "chenruien501@gmail.com"
    password = "Bin45177096!"
    ACURL = "https://www.credential.net"
    itemList = []
    pdf_urlList = []
    browser = p.chromium.launch(headless=True)  # 設定 headless=False 以打開瀏覽器介面
    page = browser.new_page()
    page.goto("https://v2.accounts.accredible.com/login")
    page.fill("#mat-input-0", acount)
    page.fill("#mat-input-1", password)
    page.locator("#main-content > ng-component > acs-panel > accredible-banner-panel > div.content-wrapper > div > div.main-content > div > div.main-panel-content > form > div.btns-container > accredible-button-loading > button > span.mat-button-wrapper").click()
    page.locator("#app-root > mat-sidenav-container > mat-sidenav-content > header > ng-component > accredible-base-header > div > div > div:nth-child(2) > acs-header-menu > accredible-base-header-menu > accredible-responsive-menu > div > a:nth-child(1)").click()
    page.locator("mat-icon").click()
    time.sleep(2)
    print("Download Start")
    html = page.content()
    soup = BeautifulSoup(html, "html.parser")
    for i in range(4, 16):
        item = soup.find(id=f"cdk-drop-list-{i}").find('a', href=True)
        itemList.append(item['href'])
    for item in itemList:
        page.goto(ACURL + item)
        pdf_url = page.locator("a").filter(has_text="pdf").get_attribute("href")
        if pdf_url:
            pdf_urlList.append(pdf_url)
        time.sleep(1)
    if not os.path.exists(FolderName):
        os.makedirs(FolderName)
    for pdf_url in pdf_urlList:
        match = re.search(r'credential_id=(\d+)', pdf_url)
        response = requests.get(pdf_url)
        with open(os.path.join(FolderName, f"{match.group(1)}.pdf"), "wb") as f:
            f.write(response.content)
    browser.close()
    print("Download Complete")