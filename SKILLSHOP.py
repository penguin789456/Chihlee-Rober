from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import requests
import time
import re
import unicodedata
import csv
import json
import configparser
import os



def GetFromJSON(fqdn,target):
    target = re.sub(r'[^a-zA-Z0-9]', '', target).lower()
    with open(f"CertAnser\\{fqdn}.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        for i in data:
            FileText = re.sub(r'[^a-zA-Z0-9]', '', i[0]).lower()
            if target in FileText:
                return i[1]


def AnserSelect(page,fqdn):
    QuestionCount = 0
    while True:
        page.wait_for_selector(".dcb-course-lesson-submit-bar-controls")
        NextButton = page.locator(".dcb-course-lesson-submit-bar-controls")
        time.sleep(1)
        page.wait_for_selector(".dcb-sh-question-content-container")
        target_text = page.locator(".dcb-sh-question-content-container").text_content()
        elements = page.locator("dcb-ui-input-radio")
        # print(elements.evaluate("node => node.outerHTML"))
        checkbox = page.locator("dcb-ui-input-checkbox")
        # print(checkbox.count())
        if"Next" not in NextButton.text_content():
            if checkbox.count() <= 1:
                elements.nth(0).click()
            else:
                checkbox.nth(0).click()
                checkbox.nth(1).click()
            NextButton.click()
            break
        try:
            found = False
            if checkbox.count() <= 1:
                Anser_text_list = GetFromJSON(fqdn,target_text)
                if(Anser_text_list == "None" or Anser_text_list == "none"):
                    elements.nth(0).click()
                else:
                    for Anser_text in Anser_text_list:
                        print(Anser_text)
                        Anser_text = re.sub(r'[^a-zA-Z0-9]', '', Anser_text)
                        for i in range(elements.count()):
                            if elements.nth(i).text_content() != None:
                                checkText =  re.sub(r'[^a-zA-Z0-9]', '', elements.nth(i).text_content())
                                if str(Anser_text).lower() in checkText.lower():
                                    elements.nth(i).click()
                                    found = True
                                    break
                        if not found:
                            elements.nth(0).click()
                NextButton.click()
                time.sleep(5)
            else:
                Anser_text = GetFromJSON(fqdn,target_text)
                print(Anser_text)
                if(Anser_text == "None" or Anser_text == "none"):
                    checkbox.nth(0).click()
                else:
                    for Box in Anser_text:
                        Box = re.sub(r'[^a-zA-Z0-9]', '', Box)
                        for i in range(checkbox.count()):
                            if checkbox.nth(i).text_content() != None: 
                                checkText =  re.sub(r'[^a-zA-Z0-9]', '', checkbox.nth(i).text_content())
                                if Box.lower() == checkText.lower():
                                    checkbox.nth(i).click()  
                                    found = True
                                    break
                    if not found:
                        checkText.nth(0).click()
                NextButton.click()
                QuestionCount += 1
                time.sleep(5)
        except:
            print("except")
            if checkbox.count() <= 1:
                elements.nth(0).click()
            else:
                checkbox.nth(0).click()
                checkbox.nth(1).click()
            NextButton.click()
    time.sleep(10)

def YTMUSIC(page,fqdn):
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
        # print(elements.all_text_contents())
        try:
            found = False
            if checkbox.count() <= 0:
                Anser_text_list = GetFromJSON(fqdn,target_text)
                if(Anser_text_list == "None" or Anser_text_list == "none"):
                    elements.nth(0).click()
                else:
                    for Anser_text in Anser_text_list:
                        for i in range(elements.count()):
                            Anser_text = str(Anser_text).replace("’","'").replace("‘", "'").replace("\n","").replace(" ","").strip().lower() #’ '
                            if elements.nth(i).text_content() != None:
                                checkText =  str(elements.nth(i).text_content()).replace("’","'").replace("‘", "'").replace("\n","").replace(" ","").strip().lower()
                                if Anser_text in checkText:
                                    elements.nth(i).click()  
                                    found = True
                                    break
                                if not found:
                                    elements.nth(0).click()
            else:
                Anser_text = GetFromJSON(fqdn,target_text)
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
                                    found = True
                                    break
                                if not found:
                                    elements.nth(0).click()
        except:
            print("except")
            if checkbox.count() <= 1:
                elements.nth(0).click()
            else:
                elements.nth(0).click()
                elements.nth(1).click()
        NextButton.click()
        index +=1

def main():
    AnserUrl = ['google-ads-display-certification-answers','google-ads-search-certification-answers','shopping-advertising-certification-answers','google-ads-video-certification-answers']
    Account_passwords  = {"linc50258@gmail.com":"BIN45177096"} 
    webhook_url = "https://discord.com/api/webhooks/1344280252196585503/2HYpHEjgqibjI-aadb7a_Af5lwyWtRulmRzgLaHIOOF_IYNai_BY6rRENz9Tkxhbehse"
    SkillcertURLDict = dict()
    SendContent = ""
    SkillLeasonUrl = "https://skillshop.docebosaas.com/learn/courses/"
    YTSkillLeasonUrl = "https://skillshop.exceedlms.com/student/path/"
    YTnotLogin = False

    with open(r"C:\Users\binho\Downloads\Chihlee-Rober\leasonURL.CSV", mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            key = row[0]
            value = row[1]
            SkillcertURLDict[key] = value
            
    for account, password in Account_passwords.items():
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
            time.sleep(15)
            print("Login")
            try:
                SendContent += "Send\n"
                for fqdn in AnserUrl:
                    if fqdn == "youtube-music-rights-management-certification-answers" or fqdn == "youtube-music-assessment-answers":
                        page.goto(YTSkillLeasonUrl+SkillcertURLDict[fqdn])
                        input("Press Enter to continue...")
                        YTMUSIC(page,fqdn)
                        time.sleep(5)
                        
                    else:
                        page.goto(SkillLeasonUrl+SkillcertURLDict[fqdn])
                        print("Skill")
                        time.sleep(15)
                        growofflineSetting = "#doc-layout-page-content > lrn-course-player > div.lrn-course-player-play-area > dcb-course-player > dialog > div.dcb-course-player-wrapper.ng-star-inserted > dcb-course-lesson-header > div > div.dcb-course-lesson-header-slot-end > button"
                        if fqdn == "grow-offline-sales-certification-answers":
                            if page.locator(growofflineSetting).is_visible():
                                page.locator(growofflineSetting).click()
                            time.sleep(1)
                        REnew = page.locator("#doc-layout-page-content > lrn-course-player > div.lrn-course-player-play-area > dcb-course-player > dcb-course-certification-renewal > dcb-ui-notification > div.dcb-ui-notification-actions > dcb-ui-notification-aside > button > span.dcb-ui-button-interaction-backdrop")
                        if REnew.is_visible():
                            REnew.click()
                            time.sleep(1)
                            page.locator("dcb-course-certification-renewal-dialog > div > div.dcb-course-certification-renewal-dialog-actions > button.dcb-ui-button-focus-ring-negative.dcb-ui-button-theme-accent.dcb-ui-button-shape-squared.dcb-ui-button-size-sm.dcb-ui-ripple").nth(0).click()
                            time.sleep(5)
                            page.locator("#doc-layout-page-content > lrn-course-player > div.lrn-course-player-play-area > dcb-course-player > dialog > div.dcb-course-player-wrapper.ng-star-inserted > dcb-course-lesson-header > div > div.dcb-course-lesson-header-slot-end > button").click()
                            time.sleep(5)
                            if fqdn == "grow-offline-sales-certification-answers":
                                if page.locator(growofflineSetting).is_visible():
                                    page.locator(growofflineSetting).click()
                                time.sleep(1)
                        time.sleep(10)
                        UItextType = page.locator("dcb-ui-accordion").all()
                        for type in UItextType:
                            if fqdn == "grow-offline-sales-certification-answers":
                                if page.locator(growofflineSetting).is_visible():
                                    page.locator(growofflineSetting).click()
                                time.sleep(1)
                            type.click()
                        time.sleep(3)
                        if fqdn == "grow-offline-sales-certification-answers":
                            if page.locator(growofflineSetting).is_visible():
                                page.locator(growofflineSetting).click()
                            time.sleep(1)
                        page.locator("dcb-sh-list-item-content").filter(has_text="Content type: HTML").click()
                        if fqdn == "grow-offline-sales-certification-answers":
                            if page.locator(growofflineSetting).is_visible():
                                page.locator(growofflineSetting).click()
                            time.sleep(1)
                        time.sleep(10)
                        if  fqdn == "google-ads-display-certification-answers" or fqdn == "shopping-advertising-certification-answers" or fqdn == "google-ads-apps-assessment-answers":
                            assessmentDom = page.locator(".dcb-ui-accordion-panel-header").filter(has_text="Pass the assessment and earn a certification")
                        else:
                            assessmentDom = page.locator(".dcb-ui-accordion-panel-header").filter(has_text="certification")
                        assessmentDom = assessmentDom.locator("..")
                        assessmentDom.locator("dcb-sh-list-item-content").filter(has_text="Content type: Test").click()
                        time.sleep(10)
                        page.locator("div.dcb-course-lesson-player-test-launcher-actions > button > span.dcb-ui-button-content > span").click()
                        time.sleep(3)
                        page.locator("div.dcb-course-lesson-player-test-launcher-dialog-actions > button.dcb-ui-button-focus-ring-negative.dcb-ui-button-theme-accent.dcb-ui-button-shape-squared.dcb-ui-button-size-sm.dcb-ui-ripple > span.dcb-ui-button-content").click()
                        time.sleep(8)
                        AnserSelect(page,fqdn)
                        SendContent += "Cert "+fqdn+" user "+account+"\n"
                time.sleep(30)
                browser.close()
            except Exception as e:
                print(e)
            data = {
                "content": SendContent
            }
            requests.post(webhook_url, json=data)



if __name__ == "__main__":
    main()
    