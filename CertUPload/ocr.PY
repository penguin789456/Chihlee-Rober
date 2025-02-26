import pytesseract
from PIL import Image
import glob
import re
from datetime import datetime
from playwright.sync_api import sync_playwright
import time
import csv

folder_path = r"C:\Users\binho\Downloads\學校證照rober\證照檔\猴子"
account = "11010202"
password = "a153153153"

CSV_path = r"C:\Users\binho\Downloads\學校證照rober\googleCERT.csv"

with open(CSV_path, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)  # 使用 csv.reader 來讀取每一行
    data_list = [row for row in reader]

# 取得所有 .jpg 檔案
jpg_files = glob.glob(f"{folder_path}/*.jpg")
FR = True
RunnCheck = None

with sync_playwright() as p:
    # 使用 Chromium 瀏覽器
    browser = p.chromium.launch(headless=False)  # 設定 headless=False 以打開瀏覽器介面
    page = browser.new_page()
    page.goto("https://e-portfolio.chihlee.edu.tw/login")
    account_selector = 'input[id="account"]'  # 選擇器
    page.fill(account_selector, account)  # 替換為目標電子郵件地址
    password_selector = 'input[type="password"]'  # 選擇器
    page.fill(password_selector, password)  # 替換為目標電子郵件地址
    captcha_selector = 'input[id="checknum"]'  # 選擇器
    capture = input("type capture")
    page.fill(captcha_selector, capture)
    page.locator('button[type="submit"]').click()
    for i in jpg_files:
        InputFile = False
        image = Image.open(i)
        text = pytesseract.image_to_string(image, lang="eng")
        match = re.search(r"Issue Date:\s*([A-Za-z]+ \d{1,2}, \d{4})", text)
        YTmatch = re.search(r"on \s*([A-Za-z]+ \d{1,2}, \d{4})", text)
        if match:
            date_str = match.group(1)  # 擷取日期字串
            date_obj = datetime.strptime(date_str, "%B %d, %Y")
            formatted_date = date_obj.strftime("%Y/%m/%d")
            year, month, day = formatted_date.split("/")
            month = str(int(month))
            if RunnCheck != formatted_date:
                RunnCheck = formatted_date
                page.goto("https://e-portfolio.chihlee.edu.tw/certificate/record/stu_add")
                page.select_option('select[name="eff_year"]', value=year)
                page.select_option('select[name="eff_month"]', value=month)
                page.select_option('select[name="eff_day"]', value=day)
                page.locator('button[type="submit"]').click()
                for CertInfor in data_list:
                    CertInforName = re.sub(r'[^a-zA-Z0-9]', '', CertInfor[1]).lower()
                    text = re.sub(r'[^a-zA-Z0-9]', '', text).lower()
                    if CertInforName in text:
                        CertSet_sel = 'input[name="certificate_code"]'
                        page.fill(CertSet_sel, CertInfor[0])
                        page.locator('input[type="file"][name="file1"]').set_input_files(i)
                        page.locator('button[type="submit"]').click()
                        InputFile = True
                        break
                if not InputFile:
                    print(text)
            else:
                RunnCheck = formatted_date
                for CertInfor in data_list:
                    CertInforName = re.sub(r'[^a-zA-Z0-9]', '', CertInfor[1]).lower()
                    text = re.sub(r'[^a-zA-Z0-9]', '', text).lower()
                    if CertInforName in text:
                        CertSet_sel = 'input[name="certificate_code"]'
                        page.fill(CertSet_sel, CertInfor[0])
                        page.locator('input[type="file"][name="file1"]').set_input_files(i)
                        page.locator('button[type="submit"]').click()
                        InputFile = True
                        break
                if not InputFile:
                    print(text)
        elif YTmatch != None:
            date_str = YTmatch.group(1)  # 擷取日期字串
            date_obj = datetime.strptime(date_str, "%B %d, %Y")
            formatted_date = date_obj.strftime("%Y/%m/%d")
            year, month, day = formatted_date.split("/")
            month = str(int(month))
            if RunnCheck != formatted_date:
                RunnCheck = formatted_date
                page.goto("https://e-portfolio.chihlee.edu.tw/certificate/record/stu_add")
                page.select_option('select[name="eff_year"]', value=year)
                page.select_option('select[name="eff_month"]', value=month)
                page.select_option('select[name="eff_day"]', value=day)
                page.locator('button[type="submit"]').click()
                for CertInfor in data_list:
                    CertInforName = re.sub(r'[^a-zA-Z0-9]', '', CertInfor[1]).lower()
                    text = re.sub(r'[^a-zA-Z0-9]', '', text).lower()
                    if CertInforName in text:
                        CertSet_sel = 'input[name="certificate_code"]'
                        page.fill(CertSet_sel, CertInfor[0])
                        page.locator('input[type="file"][name="file1"]').set_input_files(i)
                        page.locator('button[type="submit"]').click()
                        InputFile = True
                        break
                if not InputFile:
                    print(text)
            else:
                RunnCheck = formatted_date
                for CertInfor in data_list:
                    CertInforName = re.sub(r'[^a-zA-Z0-9]', '', CertInfor[1]).lower()
                    text = re.sub(r'[^a-zA-Z0-9]', '', text).lower()
                    if CertInforName in text:
                        CertSet_sel = 'input[name="certificate_code"]'
                        page.fill(CertSet_sel, CertInfor[0])
                        page.locator('input[type="file"][name="file1"]').set_input_files(i)
                        page.locator('button[type="submit"]').click()
                        InputFile = True
                        break
                if not InputFile:
                    print(text)
        else:
            print("None file")
            input("waiting close")
            browser.close()
        time.sleep(1)
print("file Done")