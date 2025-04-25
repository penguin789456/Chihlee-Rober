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

def load_config(config_path='config.ini'):
    """Load configuration from the specified config file."""
    config = configparser.ConfigParser()
    config.read(config_path)
    return config

def get_accounts(config):
    """Extract accounts from the configuration."""
    accounts = {}
    for key in config['Accounts']:
        if key.startswith('account'):
            account_num = key.replace('account', '')
            password_key = f'password{account_num}'
            accounts[config['Accounts'][key]] = config['Accounts'][password_key]
    return accounts

def get_cert_urls(config):
    """Extract certification URLs from the configuration."""
    return [url.strip() for url in config['URLs']['cert_urls'].split('\n')]

def GetFromJSON(fqdn, target):
    """
    Retrieve answers from JSON files based on the target question
    
    :param fqdn: Certification identifier
    :param target: Question text
    :return: List of answers or None
    """
    target = re.sub(r'[^a-zA-Z0-9]', '', target).lower()
    try:
        with open(f"CertAnser\\{fqdn}.json", "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
            for i in data:
                FileText = re.sub(r'[^a-zA-Z0-9]', '', i[0]).lower()
                if target in FileText:
                    return i[1]
    except FileNotFoundError:
        print(f"JSON file for {fqdn} not found.")
        return None
    return None

def AnserSelect(page, fqdn):
    """
    Automatically select answers for a certification test
    
    :param page: Playwright page object
    :param fqdn: Certification identifier
    """
    QuestionCount = 0
    while True:
        page.wait_for_selector(".dcb-course-lesson-submit-bar-controls")
        NextButton = page.locator(".dcb-course-lesson-submit-bar-controls")
        time.sleep(1)
        
        page.wait_for_selector(".dcb-sh-question-content-container")
        target_text = page.locator(".dcb-sh-question-content-container").text_content()
        
        elements = page.locator("lmn-input-radio")
        checkbox = page.locator("lmn-input-checkbox")

        if "Next" not in NextButton.text_content():
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
                # Single select questions
                Anser_text_list = GetFromJSON(fqdn, target_text)
                if(Anser_text_list == "None" or Anser_text_list == "none"):
                    elements.nth(0).click()
                else:
                    for Anser_text in Anser_text_list:
                        print(Anser_text)
                        Anser_text = re.sub(r'[^a-zA-Z0-9]', '', Anser_text)
                        for i in range(elements.count()):
                            if elements.nth(i).text_content() != None:
                                checkText = re.sub(r'[^a-zA-Z0-9]', '', elements.nth(i).text_content())
                                if str(Anser_text).lower() in checkText.lower():
                                    elements.nth(i).click()
                                    found = True
                                    break
                        if not found:
                            elements.nth(0).click()
                NextButton.click()
                time.sleep(5)
            else:
                # Multiple select questions
                Anser_text = GetFromJSON(fqdn, target_text)
                print(Anser_text)
                if(Anser_text == "None" or Anser_text == "none"):
                    checkbox.nth(0).click()
                else:
                    for Box in Anser_text:
                        Box = re.sub(r'[^a-zA-Z0-9]', '', Box)
                        for i in range(checkbox.count()):
                            if checkbox.nth(i).text_content() != None: 
                                checkText = re.sub(r'[^a-zA-Z0-9]', '', checkbox.nth(i).text_content())
                                if Box.lower() == checkText.lower():
                                    checkbox.nth(i).click()  
                                    found = True
                                    break
                    if not found:
                        checkbox.nth(0).click()
                NextButton.click()
                QuestionCount += 1
                time.sleep(5)
        except Exception as e:
            print(f"Exception in AnserSelect: {e}")
            if checkbox.count() <= 1:
                elements.nth(0).click()
            else:
                checkbox.nth(0).click()
                checkbox.nth(1).click()
            NextButton.click()
    time.sleep(10)

def YTMUSIC(page, fqdn):
    """
    Handle YouTube Music certification test
    
    :param page: Playwright page object
    :param fqdn: Certification identifier
    """
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

        try:
            found = False
            if checkbox.count() <= 0:
                # Single select questions
                Anser_text_list = GetFromJSON(fqdn, target_text)
                if(Anser_text_list == "None" or Anser_text_list == "none"):
                    elements.nth(0).click()
                else:
                    for Anser_text in Anser_text_list:
                        for i in range(elements.count()):
                            # Clean and normalize text for comparison
                            Anser_text = str(Anser_text).replace("'","'").replace("'", "'").replace("\n","").replace(" ","").strip().lower()
                            if elements.nth(i).text_content() != None:
                                checkText = str(elements.nth(i).text_content()).replace("'","'").replace("'", "'").replace("\n","").replace(" ","").strip().lower()
                                if Anser_text in checkText:
                                    elements.nth(i).click()  
                                    found = True
                                    break
                        if not found:
                            elements.nth(0).click()
            else:
                # Multiple select questions
                Anser_text = GetFromJSON(fqdn, target_text)
                if(Anser_text == "None" or Anser_text == "none"):
                    elements.nth(0).click()
                else:
                    for Box in Anser_text:
                        print(Box)
                        # Clean and normalize text for comparison
                        Box = str(Box).replace("'","'").replace("'", "'").replace("\n","").replace(" ","").strip().lower()
                        for i in range(elements.count()):
                            if elements.nth(i).text_content() != None: 
                                checkText = str(elements.nth(i).text_content()).replace("'","'").replace("'", "'").replace("\n","").replace(" ","").strip().lower()
                                if Box in checkText:
                                    elements.nth(i).click()  
                                    found = True
                                    break
                        if not found:
                            elements.nth(0).click()
        except Exception as e:
            print(f"Exception in YTMUSIC: {e}")
            if checkbox.count() <= 1:
                elements.nth(0).click()
            else:
                elements.nth(0).click()
                elements.nth(1).click()
        
        NextButton.click()
        index += 1

def  LamListTest(page):
    IndexParent = 0
    IndexChild = 0
    while True:
        IndexChild = 0
        if IndexParent >= 100:
                break
        DomObject = page.locator(f"#lmn-list-{IndexParent}-0")
        if DomObject.count() > 1:
            DomObject = DomObject.nth(0)
        if DomObject.is_visible():
            while True:
                DomObject = page.locator(f"#lmn-list-{IndexParent}-{IndexChild}")
                if DomObject.count() > 1:
                    DomObject = DomObject.nth(0)
                if DomObject.is_visible():
                    DOMTEXT = DomObject.text_content()
                    if "Content type: Test" in DOMTEXT:
                        DomObject.click()
                        return
                else:
                    break
                if IndexChild >= 100:
                    break
                IndexChild += 1
        IndexParent += 1
        
def dcbCourseSyllabus(page):
    FolderCount = 0
    while True:
        if page.locator(f'[aria-labelledby="dcb-course-syllabus-folder-name-{FolderCount}"]').is_visible() or page.locator(f'[aria-labelledby="dcb-course-syllabus-folder-name-{FolderCount+1}"]').is_visible():
            if page.locator(f'[aria-labelledby="dcb-course-syllabus-folder-name-{FolderCount}"]').is_visible():
                page.locator(f'[aria-labelledby="dcb-course-syllabus-folder-name-{FolderCount}"]').click()
            FolderCount+=1
        else:
            break
    time.sleep(3)

def main():
    # Load configuration
    config = load_config()
    
    # Get accounts and URLs from config
    Account_passwords = get_accounts(config)
    AnserUrl = get_cert_urls(config)
    
    # Get other configuration parameters
    webhook_url = config['Webhooks']['discord_webhook']
    lesson_url_csv = config['Paths']['lesson_url_csv']
    
    SkillcertURLDict = dict()
    SkillLeasonUrl = "https://skillshop.docebosaas.com/learn/courses/"
    YTSkillLeasonUrl = "https://skillshop.exceedlms.com/student/path/"

    # Read lesson URLs from CSV
    with open(lesson_url_csv, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            key = row[0]
            value = row[1]
            SkillcertURLDict[key] = value
            
    # Process each account
    for account, password in Account_passwords.items():
        SendContent = ""
        with sync_playwright() as p:
            # Launch browser
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto("https://skillshop.docebosaas.com/learn/signin")
            time.sleep(10)
            
            # Login process
            SignButton = page.locator("#doc-layout-login > div > form > div > ui-button-raised-neutral > ui-button-raised > button")
            SignButton.click()
            
            email_selector = 'input[type="email"]'
            page.fill(email_selector, account)
            page.locator("#identifierNext > div > button").click()
            time.sleep(2)
            
            password_selector = 'input[type="password"]'
            page.fill(password_selector, password)
            page.locator("#passwordNext > div > button").click()
            time.sleep(15)
            
            print(f"Logged in as {account}")
            
            try:
                SendContent += "Send\n"
                
                # Process each certification URL
                for fqdn in AnserUrl:
                    if fqdn in ["youtube-music-rights-management-certification-answers", "youtube-music-assessment-answers"]:
                        page.goto(YTSkillLeasonUrl + SkillcertURLDict[fqdn])
                        input("Press Enter to continue...")
                        YTMUSIC(page, fqdn)
                        time.sleep(5)
                    else:
                        page.goto(SkillLeasonUrl + SkillcertURLDict[fqdn])
                        print(f"Processing {fqdn}")
                        time.sleep(15)
                        
                        # Handle specific course settings
                        growofflineSetting = "#doc-layout-page-content > lrn-course-player > div.lrn-course-player-play-area > dcb-course-player > dialog > div.dcb-course-player-wrapper.ng-star-inserted > dcb-course-lesson-header > div > div.dcb-course-lesson-header-slot-end > button"
                        
                        if fqdn == "grow-offline-sales-certification-answers":
                            if page.locator(growofflineSetting).is_visible():
                                page.locator(growofflineSetting).click()
                            time.sleep(1)
                        
                        # Handle certification renewal
                        REnew = page.locator("#doc-layout-page-content > lrn-course-player > div.lrn-course-player-play-area > dcb-course-player > dcb-course-certification-renewal > lmn-notification > div.lmn-notification-actions > lmn-notification-aside > button > span.lmn-button-interaction-backdrop")
                        if REnew.is_visible():
                            REnew.click()
                            time.sleep(1)
                            page.locator("#lmn-modal-dialog-4 > dcb-course-certification-renewal-dialog > div > div.dcb-course-certification-renewal-dialog-actions > button.lmn-button-theme-accent.lmn-button-shape-squared.lmn-button-size-sm.lmn-ripple.lmn-button-focus-ring-positive").click()
                            time.sleep(5)
                            # page.locator("#doc-layout-page-content > lrn-course-player > div.lrn-course-player-play-area > dcb-course-player > dialog > div.dcb-course-player-wrapper.ng-star-inserted > dcb-course-lesson-header > div > div.dcb-course-lesson-header-slot-end > button").click()
                            # time.sleep(5)
                            
                            if fqdn == "grow-offline-sales-certification-answers":
                                if page.locator(growofflineSetting).is_visible():
                                    page.locator(growofflineSetting).click()
                                time.sleep(1)
                        
                        # Navigate through course content
                        time.sleep(10)

                        dcbCourseSyllabus(page)
                        
                        # Additional specific handling
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

                        LamListTest(page)
                        
                        time.sleep(10)
                        page.locator("#doc-layout-page-content > lrn-course-player > div.lrn-course-player-play-area > dcb-course-player > dialog > div > section > dcb-course-lesson-player-test > div > dcb-course-lesson-player-test-launcher > div.dcb-course-lesson-player-test-launcher-actions > button > span.lmn-button-interaction-backdrop").click()
                        time.sleep(3)
                        page.locator("div.dcb-course-lesson-player-test-launcher-dialog > div.dcb-course-lesson-player-test-launcher-dialog-actions > button.lmn-button-theme-accent.lmn-button-shape-squared.lmn-button-size-sm.lmn-ripple.lmn-button-focus-ring-positive").click()
                        time.sleep(8)
                        
                        # Automatically answer questions
                        AnserSelect(page, fqdn)
                        SendContent += f"Cert {fqdn} user {account}\n"
                
                time.sleep(30)
                browser.close()
            
            except Exception as e:
                print(f"An error occurred: {e}")
            
            # Send notification via webhook
            data = {
                "content": SendContent
            }
            requests.post(webhook_url, json=data)

if __name__ == "__main__":
    main()