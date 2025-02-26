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

def AnserSelect(page,soup):
    final = False
    while True:
        page.wait_for_selector(".ng-star-inserted > .ui-button-raised-primary > .ui-ripple")
        NextButton = page.locator(".ng-star-inserted > .ui-button-raised-primary > .ui-ripple")
        time.sleep(1)
        page.wait_for_selector(".dcb-te-question-title")
        target_text = page.locator(".dcb-te-question-title").text_content()
        elements = page.locator(".dcb-te-answer-option-box")
        checkbox = page.locator(".dcb-ui-input-checkbox")
        if"Next" not in NextButton.text_content():
            elements.nth(0).click()
            NextButton.click()
            break
        try:
            found = False
            if checkbox.count() <= 0:
                Anser_text = extract_links_from_page(soup,target_text,None)
                Anser_text = re.sub(r'[^a-zA-Z0-9]', '', Anser_text) #’ '
                # print(Anser_text)
                if(Anser_text == "None" or Anser_text == "none"):
                    elements.nth(0).click()
                else:
                    for i in range(elements.count()):
                        if elements.nth(i).text_content() != None:
                            checkText =  re.sub(r'[^a-zA-Z0-9]', '', elements.nth(i).text_content())
                            if Anser_text in checkText:
                                elements.nth(i).click()
                                found = True
                                break
                    if not found:
                        elements.nth(0).click()
                NextButton.click()
            else:
                Anser_text = extract_links_from_page(soup,target_text,True)
                if(Anser_text == "None" or Anser_text == "none"):
                    elements.nth(0).click()
                else:
                    for Box in Anser_text:
                        Box = re.sub(r'[^a-zA-Z0-9]', '', Box)
                        # print(Box)
                        for i in range(elements.count()):
                            if elements.nth(i).text_content() != None: 
                                checkText =  re.sub(r'[^a-zA-Z0-9]', '', elements.nth(i).text_content())
                                if Box == checkText:
                                    elements.nth(i).click()  
                                    found = True
                                    break
                    if not found:
                        elements.nth(0).click()
                NextButton.click()
        except:
            input("except Waitting")
            NextButton.click()

def main():
    # 啟動 Playwright
    Anser_host = "https://www.gcertificationcourse.com/"
    AnserUrl = ['google-ads-display-certification-answers','google-ads-search-certification-answers','shopping-advertising-certification-answers','google-ads-measurement-certification-answers','google-ads-apps-assessment-answers','display-video-360-certification-exam-answers','google-ads-creative-exam-answers','grow-offline-sales-certification-answers','google-ads-ai-powered-performance-ads-answers','google-analytics-certification-answers','campaign-manager-certification-answers']
    account = "chenruien501@gmail.com"
    password = "bin45177096!"
    webhook_url = "https://discord.com/api/webhooks/1269207220810289185/VWJ_wDS4YB_hZJJ-Lw2gF6mbyK3ewpbEWwdLzXA_h2I8zhffzn7_f24le5_65s5Ai5x8"

    with sync_playwright() as p:
        # 使用 Chromium 瀏覽器
        browser = p.chromium.launch(headless=False)  # 設定 headless=False 以打開瀏覽器介面
        page = browser.new_page()
        page.goto("https://skillshop.docebosaas.com/learn/signin")
        time.sleep(10)
        SignButton = page.locator("#doc-layout-login > div > form > div > ui-button-raised-neutral > ui-button-raised > button")
        SignButton.click()
        email_selector = 'input[type="email"]'  # 選擇器
        page.fill(email_selector, account)  # 替換為目標電子郵件地址
        page.locator("#identifierNext > div > button").click()
        time.sleep(2)
        password_selector = 'input[type="password"]'  # 選擇器
        page.fill(password_selector, password)  # 替換為目標電子郵件地址
        page.locator("#passwordNext > div > button").click()
        for fqdn in AnserUrl:
            data = {
                "content": "Cert "+fqdn+" user "+account
            }
            response = requests.post(webhook_url, json=data)
            input("Waiting for user")
            response = requests.get(Anser_host+fqdn)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                AnserSelect(page,soup)
        input("Waiting for Close")
        browser.close()


if __name__ == "__main__":
    main()