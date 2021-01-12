#coding: utf-8

import time
import pyperclip
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import ElementNotVisibleException
from utils import DEFAULT_TIMEOUT_DELAY


class Naver_shop:

    def switch_popup(self, driver):
        windows = driver.window_handles
        driver.switch_to.window(windows[-1])  
        
    def switch_main(self, driver):
        windows = driver.window_handles
        driver.switch_to.window(windows[0])

    def wait(self, driver, selector, sec):
        try:
            WebDriverWait(driver, sec).until(
                expected_conditions.presence_of_element_located((By.XPATH, selector))
            )
        except:
            pass

    def wait_popup(self, driver, selector, sec):
        while True:
            try:
                self.switch_popup(driver)
                WebDriverWait(driver, sec).until(
                    expected_conditions.presence_of_element_located((By.XPATH, selector))
                )
                break
            except:
                pass

    def close_popup(self, driver):
        windows = driver.window_handles
        main = windows[0]
        for window in windows:
            if window != main:
                driver.switch_to.window(window)
                driver.close()

        driver.switch_to.window(main)

    def get_driver(self, url, download_path):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-fullscreen")
        # options.add_argument("headless")
        # options.add_experimental_option("detach", True)
        base_path = "download.default_directory="
        download_path = base_path + download_path
        options.add_argument(download_path)

        driver = webdriver.Chrome("chromedriver.exe", options=options)

        driver.get(url)
        
        # Wait for browser loading
        naver_login_button = """//*[@id="container"]/main/div/div[1]/home-login/div/div/button/span"""
        self.wait(driver, naver_login_button, 10)
        
        return driver

    def naver_login(self, driver, account):
        # get naver login button
        naver_login = driver.find_element_by_class_name("naver_login_btn")
        naver_login.click()

        # wait for login popup
        naver_banner = """//*[@id="log.naver"]"""
        self.wait_popup(driver, naver_banner, DEFAULT_TIMEOUT_DELAY)

        time.sleep(1)

        # get naver id form
        id_form = driver.find_element_by_id("id")
        clip_id = pyperclip.copy(account["id"])
        id_form.click()
        id_form.send_keys(Keys.CONTROL, "v")

        time.sleep(1)

        # get naver pw form
        pw_form = driver.find_element_by_id("pw")
        clip_pw = pyperclip.copy(account["pw"])
        pw_form.click()
        pw_form.send_keys(Keys.CONTROL, "v")

        time.sleep(1)

        # get login button
        login_button = driver.find_element_by_id("log.login")
        login_button.click()

    def login(self, driver, account):
        if account["type"] == "naver":
            self.naver_login(driver, account)
        else:
            time.sleep(1)

            # get id form
            id_form = driver.find_element_by_id("uid")
            id_form.send_keys(account["id"])

            time.sleep(1)

            # get pw form
            pw_form = driver.find_element_by_id("upw")
            pw_form.send_keys(account["pw"])

            time.sleep(1)
            
            pw_form.send_keys(Keys.RETURN)

    def move_page(self, driver):
        # return to main window
        self.switch_main(driver)

        login_ok_button = """//*[@id="mat-dialog-0"]/naver-login-confirm/mat-dialog-content/div[2]/button/span"""

        try:
            self.wait(driver, login_ok_button, DEFAULT_TIMEOUT_DELAY)
            driver.find_element_by_xpath(login_ok_button).click()
        except:
            pass

        # click AD Management button
        ad_management_button = driver.find_element_by_xpath("""//*[@id="container"]/my-screen/div/div[1]/div/my-screen-board/div/div[1]/div[1]/board-campaign-type/div[1]/a""")
        ad_management_button.click()

        date_button = """//*[@id="root"]/div/div[2]/div/div[1]/div/div[2]/div/div/span/div/div"""
        self.wait_popup(driver, date_button, DEFAULT_TIMEOUT_DELAY)

    def select_date(self, driver, uid):
        if uid != "lavenakorea":
            driver.find_element_by_xpath("""//*[@id="root"]/div/div[1]/div/div[1]/div[2]/div/div/div[1]/ul/li[2]/div/a""").click()
            multi_report = """//*[@id="root"]/div/div[1]/div/div[1]/div[2]/div/div/div[1]/ul/li[2]/div/div/div[1]/a/button"""
            self.wait(driver, multi_report, DEFAULT_TIMEOUT_DELAY)
            driver.find_element_by_xpath(multi_report).click()
            
            try:
                for i in range(1, 20+1):
                    report_name = f"""//*[@id="root"]/div/div[2]/div/div/div[4]/div/div[3]/table/tbody/tr[{i}]/td[2]/a"""
                    self.wait(driver, report_name, DEFAULT_TIMEOUT_DELAY)
                    report_name = driver.find_element_by_xpath(report_name)

                    if uid == "anua":
                        pattern = "광고비"
                    elif uid == "yuge":
                        pattern = "광고비("
                    else:
                        pattern = "광고비매출보고서"

                    if pattern in report_name.text:
                        report_name.click()
                        break
                    
            except Exception as e:
                print(e)

            date_form = """//*[@id="root"]/div/div[2]/div/div/div[2]/div/div/div[2]/div/div[1]/div/div[1]/div[2]/div/div/span/div/div"""
            yesterday_button = """//*[@id="root"]/div/div[2]/div/div/div[2]/div/div/div[2]/div/div[1]/div/div[1]/div[2]/div/div/div/div[1]/div[1]/span"""
        
        else:
            # click date form
            date_form = """//*[@id='root']/div/div[2]/div/div[1]/div/div[2]/div/div/span/div/div"""
            yesterday_button = """//*[@id='root']/div/div[2]/div/div[1]/div/div[2]/div/div/div/div[1]/div[2]/span"""

        self.wait(driver, date_form, DEFAULT_TIMEOUT_DELAY)
        date_form = driver.find_element_by_xpath(date_form)
        date_form.click()

        # click yesterday button
        self.wait(driver, yesterday_button, DEFAULT_TIMEOUT_DELAY)
        yesterday_button = driver.find_element_by_xpath(yesterday_button)
        yesterday_button.click()

        # wait for loading
        time.sleep(2)
        
        #
        # TODO : change 3 days if today is MONDAY
        #

    def download_csv(self, driver, uid):
        if uid == "lavenakorea":
            download_button = driver.find_element_by_xpath("""//*[@id='root']/div/div[2]/div/div[3]/div/div[1]/div[1]/div[2]/div/button""")
        else:
            download_button = driver.find_element_by_xpath("""//*[@id="root"]/div/div[2]/div/div/div[1]/div[2]/button""")

        download_button.click()

        time.sleep(5)

    def run(self, uid, upw, utype):
        # account list
        # lavena, yuge, anua, project21

        url = "https://searchad.naver.com/"
        download_path = "C:/Downloads"

        account = {
            "id": uid,
            "pw": upw,
            "type": utype
        }

        driver = self.get_driver(url, download_path)
        self.close_popup(driver)
        self.login(driver, account)
        self.move_page(driver)
        self.select_date(driver, account["id"])
        self.download_csv(driver, account["id"])