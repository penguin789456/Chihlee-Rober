import os
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import requests
import time
import re
from pdf2image import convert_from_path
import os
import configparser


def Catch_PDF(acount, StartIndex, EndIndex, UserName):
    FolderName = "C:\\Users\\binho\\Downloads\\Chihlee-Rober\\證照檔\\"+UserName 
    password = "Bin45177096!"
    ACURL = "https://www.credential.net"
    itemList = []
    pdf_urlList = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # 設定 headless=False 以打開瀏覽器介面
        page = browser.new_page()
        page.goto("https://v2.accounts.accredible.com/login")
        page.fill("#mat-input-0", acount)
        page.fill("#mat-input-1", password)
        page.locator("#main-content > ng-component > acs-panel > accredible-banner-panel > div.content-wrapper > div > div.main-content > div > div.main-panel-content > form > div.btns-container > accredible-button-loading > button > span.mat-button-wrapper").click()
        page.locator("#app-root > mat-sidenav-container > mat-sidenav-content > header > ng-component > accredible-base-header > div > div > div:nth-child(2) > acs-header-menu > accredible-base-header-menu > accredible-responsive-menu > div > a:nth-child(1)").click()
        if page.locator("mat-icon").is_visible():
            page.locator("mat-icon").click()
        time.sleep(7)
        print("Download Start")
        html = page.content()
        soup = BeautifulSoup(html, "html.parser")
        for i in range(StartIndex, EndIndex):
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

def pdf_to_jpg(UserName):
    pdf_folder = "C:\\Users\\binho\\Downloads\\Chihlee-Rober\\證照檔\\"+UserName 
    output_folder = pdf_folder
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for pdf_file in os.listdir(pdf_folder):
        if pdf_file.lower().endswith(".pdf"): 
            pdf_path = os.path.join(pdf_folder, pdf_file)
            pdf_name = os.path.splitext(pdf_file)[0]  
            pdf_output_folder = os.path.join(output_folder)

            try:
                # 轉換 PDF 為圖片
                images = convert_from_path(pdf_path)
                for i, image in enumerate(images):
                    # 將每一頁存成 JPG
                    output_file = os.path.join(pdf_output_folder, f"{pdf_name}.jpg")
                    image.save(output_file, 'JPEG')
                    print(f"已儲存: {output_file}")
            except Exception as e:
                print(f"轉換 {pdf_file} 時發生錯誤: {e}")

def parse_account_section_with_configparser(file_path = "DLconfig.ini"):
    config = configparser.ConfigParser()
    config.read(file_path, encoding="utf-8")

    if "Account" not in config:
        raise ValueError("The [Account] section is missing in the file.")

    account_dict = dict(config["Account"])
    return account_dict

def Page_parameter_Set_with_configparser(file_path = "DLconfig.ini"):
    config = configparser.ConfigParser()
    config.read(file_path, encoding="utf-8")

    Page_parameter_Set = dict(config["Page"])
    return Page_parameter_Set

if __name__ == "__main__":
    acountList =parse_account_section_with_configparser()
    UserName = "陳威誠"
    PageParmeter = Page_parameter_Set_with_configparser()
    for name, email in acountList.items():
        Catch_PDF(email, int(PageParmeter["startindex"]), int(PageParmeter["endindex"]), name)
        pdf_to_jpg(name)
        print(f"{name} 轉換完成")
    print("轉換全部完成")