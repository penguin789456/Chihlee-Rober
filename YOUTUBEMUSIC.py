from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import requests
import time
import re
import unicodedata


def extract_links_from_page(soup,target,CheckBox):
    all_links = soup.select("ol li a")
    target = re.sub(r'\s*\n\s*', ' ', target).strip().replace("’","'").replace("‘", "'").lower()

    for link in all_links:
        link_text = re.sub(r'\s*\n\s*', ' ', link.get_text(strip=True)).strip().replace("’","'").replace("‘", "'").lower()
        if target in link_text:
            link_url = link.get('href')  # 提取 href 屬性
            response = requests.get(link_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                strong_texts_in_li = [strong.get_text() for li in soup.find_all('li') for strong in li.find_all('strong')]
                if CheckBox:
                    return strong_texts_in_li
                else:
                    return strong_texts_in_li[0]

def Running(page,soup):
    index = 0
    while True:
        page.wait_for_selector("#assessment-response-submit")
        NextButton = page.locator("#assessment-response-submit")
        NextButtonContent = NextButton.text_content()
        time.sleep(1)
        page.wait_for_selector(".question__question")
        target_text = page.locator(".question__question").text_content()
        elements = page.locator(".question__choicesitem")
        checkbox = page.locator(".dcb-ui-input-checkbox")
        if "Next" not in NextButtonContent:
            elements.nth(0).click()
            NextButton.click()
            break
        print(elements.all_text_contents())
        try:
            if checkbox.count() <= 0:
                Anser_text = extract_links_from_page(soup,target_text,None)
                Anser_text = str(Anser_text).replace("’","'").replace("‘", "'").replace("\n","").replace(" ","").strip().lower() #’ '
                if(Anser_text == "None" or Anser_text == "none"):
                    elements.nth(0).click()
                else:
                    for i in range(elements.count()):
                        if elements.nth(i).text_content() != None:
                            checkText =  str(elements.nth(i).text_content()).replace("’","'").replace("‘", "'").replace("\n","").replace(" ","").strip().lower()
                            if Anser_text in checkText:
                                elements.nth(i).click()  
                                break
            else:
                Anser_text = extract_links_from_page(soup,target_text,True)
                if(Anser_text == "None" or Anser_text == "none"):
                    elements.nth(0).click()
                else:
                    for Box in Anser_text:
                        print(Box)
                        Box = str(Box).replace("’","'").replace("‘", "'").replace("\n","").replace(" ","").strip().lower()
                        for i in range(elements.count()):
                            if elements.nth(i).text_content() != None: 
                                checkText =  str(elements.nth(i).text_content()).replace("’","'").replace("‘", "'").replace("\n","").replace(" ","").strip().lower()
                                if Box in checkText:
                                    elements.nth(i).click()  
                                    break
        except:
            input("in user Check")
        # input("Watting For user Check and Next")
        NextButton.click()
        index +=1


def main():
    # 啟動 Playwright
    Anser_host = "https://www.gcertificationcourse.com/"
    AnserUrl = ["youtube-music-rights-management-certification-answers","youtube-music-assessment-answers"]
    account = "chenruien501@gmail.com"
    password = "bin45177096"
    webhook_url = "https://discord.com/api/webhooks/1269207220810289185/VWJ_wDS4YB_hZJJ-Lw2gF6mbyK3ewpbEWwdLzXA_h2I8zhffzn7_f24le5_65s5Ai5x8"
    with sync_playwright() as p:
        # 使用 Chromium 瀏覽器
        browser = p.chromium.launch(headless=False)  # 設定 headless=False 以打開瀏覽器介面
        page = browser.new_page()
        page.goto("https://skillshop.exceedlms.com/student/path/73995-youtube-music-rights-management-certification")
        input("watting input account and password")
        email_selector = 'input[type="email"]'  # 選擇器
        page.fill(email_selector, account)  # 替換為目標電子郵件地址
        page.locator("button:has(span:has-text('下一步'))").click
        time.sleep(2)
        password_selector = 'input[type="password"]'  # 選擇器
        page.fill(password_selector, password)  # 替換為目標電子郵件地址
        page.locator("button:has(span:has-text('下一步'))").click
        input("Waiting for user")
        for fqdn in AnserUrl:
            data = {
                "content": "Cert "+fqdn+" user "+account
            }
            response = requests.post(webhook_url, json=data)
            input("Waiting for user")
            response = requests.get(Anser_host+fqdn)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                Running(page,soup)
        input("Waiting for close")
        browser.close()

if __name__ == "__main__":
    main()