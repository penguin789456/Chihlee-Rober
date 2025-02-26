import pytesseract
from PIL import Image
import glob
import re
from datetime import datetime
from playwright.sync_api import sync_playwright
import time
import csv

folder_path = r"C:\Users\binho\Downloads\學校證照rober\證照檔\花蓮偏鄉"

jpg_files = glob.glob(f"{folder_path}/*.jpg")

for i in jpg_files:
    image = Image.open(i)
    text = pytesseract.image_to_string(image, lang="eng")
    match = re.search(r"Issue Date:\s*([A-Za-z]+ \d{1,2}, \d{4})", text)
    YTmatch = re.search(r"on \s*([A-Za-z]+ \d{1,2}, \d{4})", text)
    if YTmatch != None:
        date_str = YTmatch.group(1)  # 擷取日期字串
        date_obj = datetime.strptime(date_str, "%B %d, %Y")
        formatted_date = date_obj.strftime("%Y/%m/%d")
        year, month, day = formatted_date.split("/")
        month = str(int(month))
        print(year)
        print(month)
        print(day)