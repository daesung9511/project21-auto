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


class Kakaomoment:

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
        kakao_login_button = """//*[@id="login-form"]/fieldset/div[8]/button[1]"""
        self.wait(driver, kakao_login_button, 10)
        
        return driver

    def login(self, driver, account):
        time.sleep(1)

        # get kakao id form
        id_form = driver.find_element_by_id("id_email_2")
        clip_id = pyperclip.copy(account["id"])
        id_form.click()
        id_form.send_keys(Keys.CONTROL, "v")

        time.sleep(1)

        # get kakao pw form
        pw_form = driver.find_element_by_id("id_password_3")
        clip_pw = pyperclip.copy(account["pw"])
        pw_form.click()
        pw_form.send_keys(Keys.CONTROL, "v")

        time.sleep(1)

        # get kakao login button
        kakao_login_button = driver.find_element_by_xpath("""//*[@id="login-form"]/fieldset/div[8]/button[1]""")
        kakao_login_button.click()

        # wait for login
        dashboard = """//*[@id="kakaoContent"]/div[1]/ul/li[1]/a"""

        try:
            self.wait(driver, dashboard, DEFAULT_TIMEOUT_DELAY)
        except:
            time.sleep(1)

    def move_dashboard(self, driver, url):
        # move to dashboard
        dashboard_url = f"https://moment.kakao.com/{domain}/report/customreport/all"
        driver.get(dashboard_url)

        report_name = """//*[@id="mArticle"]/div/div[2]/div[2]/table/tbody/tr[1]/td[2]/div/a"""
        self.wait(driver, report_name, DEFAULT_TIMEOUT_DELAY)
        

    def press_ok(self, driver):
        # wait for ok button after login
        login_ok_button = """//*[@id="app"]/div/div[2]/div[2]/div/div[2]/span/div/div/div[2]/div[3]/button"""

        try:
            self.wait(driver, login_ok_button, DEFAULT_TIMEOUT_DELAY)
            driver.find_element_by_xpath(login_ok_button).click()
        except:
            pass

    def switch_user(self, driver, domain):
        # click user menu dropdown
        user_menu_dropdown = driver.find_element_by_xpath("""//*[@id="app"]/div/div[1]/div/ul/li[1]/a""")
        user_menu_dropdown.click()

        # wait for user menu
        user_name = """//*[@id="app"]/div/div[1]/div/ul/li[1]/ul/li[3]/div/div[3]/div/div/div/ul/li[1]/label/span[2]"""
        self.wait(driver, user_name, DEFAULT_TIMEOUT_DELAY)

        # time.sleep(1)

        pattern = ""
        if domain == "lavena":
            pattern = "라베나코리아"
        elif domain == "yuge":
            pattern = "유즈"
        else:
            pattern = "더파운더즈"

        user = """//*[@id="app"]/div/div[1]/div/ul/li[1]/ul/li[3]/div/div[3]/div/div/div/ul/li[1]/label/span[1]"""
        try:
            for i in range(1, 10+1):
                user_name = driver.find_element_by_xpath(f"""//*[@id="app"]/div/div[1]/div/ul/li[1]/ul/li[3]/div/div[3]/div/div/div/ul/li[{i}]/label/span[2]""")
                if pattern in user_name.text:
                    user = f"""//*[@id="app"]/div/div[1]/div/ul/li[1]/ul/li[3]/div/div[3]/div/div/div/ul/li[{i}]/label/span[1]"""
                    break

        except Exception as e:
            print(e)

        # switch user
        user = driver.find_element_by_xpath(user)
        user.click()

    def move_page(self, driver, domain):
        # click report button 
        report_button = """//*[@id="app"]/div/div[2]/div[1]/div/div[2]/ul/li[2]/a"""
        self.wait(driver, report_button, DEFAULT_TIMEOUT_DELAY)
        driver.find_element_by_xpath(report_button).click()

        # wait for report name
        report_name = """//*[@id="app"]/div/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div/div/div/div[1]/div[2]/div/table/tbody/tr[1]/td[1]/a"""
        self.wait(driver, report_name, DEFAULT_TIMEOUT_DELAY)
        
        # find report name
        pattern = "광고비 리포트"
        if domain in ("lavena", "yuge"):
            pattern = "광고비 리포트"
        elif domain == "anua":
            pattern = "성과 리포트"
        
        try:
            for i in range(1, 20+1):
                report_name = driver.find_element_by_xpath(f"""//*[@id="app"]/div/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/div/div/div/div[1]/div[2]/div/table/tbody/tr[{i}]/td[1]/a""")
                if pattern in report_name.text:
                    # move to detail page
                    report_name.click()
                    break

        except Exception as e:
            print(e)

    def select_date(self, driver, domain):
        date_form = """//*[@id="app"]/div/div[2]/div[2]/div/div[2]/div[1]/div/div[1]/div[2]/div/div/div[1]/button[2]"""
        yesterday_button = """//*[@id="app"]/div/div[2]/div[2]/div/div[2]/div[1]/div/div[1]/div[2]/div/div/div[2]/div/div[1]/ul/li[2]/button"""
        ok_button = """//*[@id="app"]/div/div[2]/div[2]/div/div[2]/div[1]/div/div[1]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/button[2]"""
        confirm_button = """//*[@id="app"]/div/div[2]/div[2]/div/div[2]/div[1]/div/div[4]/button"""
        if domain in ("lavena", "yuge"):
            confirm_button = """//*[@id="app"]/div/div[2]/div[2]/div/div[2]/div[1]/div/div[4]/button"""
        elif domain == "anua":
            confirm_button = """//*[@id="app"]/div/div[2]/div[2]/div/div[2]/div[1]/div/div[6]/button"""
            

        # click date form
        self.wait(driver, date_form, DEFAULT_TIMEOUT_DELAY)
        date_form = driver.find_element_by_xpath(date_form)
        date_form.click()

        # click yesterday button
        self.wait(driver, yesterday_button, DEFAULT_TIMEOUT_DELAY)
        yesterday_button = driver.find_element_by_xpath(yesterday_button)
        yesterday_button.click()

        # click ok button
        self.wait(driver, ok_button, DEFAULT_TIMEOUT_DELAY)
        ok_button = driver.find_element_by_xpath(ok_button)
        ok_button.click()

        # click campaign button
        if domain == "anua":
            analysis_level = """//*[@id="app"]/div/div[2]/div[2]/div/div[2]/div[1]/div/div[2]/div[2]/label[2]/span"""
            self.wait(driver, analysis_level, DEFAULT_TIMEOUT_DELAY)
            pattern = "캠페인"
            try:
                for i in range(1, 10+1):
                    analysis_level_name = driver.find_element_by_xpath(f"""//*[@id="app"]/div/div[2]/div[2]/div/div[2]/div[1]/div/div[2]/div[2]/label[{i}]/span""")
                    if pattern == analysis_level_name.text:
                        analysis_level_name.click()
                        break
                        
            except Exception as e:
                print(e)

        # click confirm button
        self.wait(driver, confirm_button, DEFAULT_TIMEOUT_DELAY)
        confirm_button = driver.find_element_by_xpath(confirm_button)
        confirm_button.click()

        # wait for loading
        time.sleep(2)
        
        #
        # TODO : change 3 days if today is MONDAY
        #

    def download_csv(self, driver, domain):
        download_button = driver.find_element_by_xpath("""//*[@id="app"]/div/div[2]/div[2]/div/div[2]/div[2]/div/div/div[1]/div/div[2]/a/button""")
        download_button.click()

        time.sleep(5)

    def run(self, uid, upw, udomain):
        # account list
        # lavena, yuge, anua, project21

        url = "https://accounts.kakao.com/login/kakaoforbusiness?continue=https://business.kakao.com/dashboard/?sid=kmo&redirect=https://moment.kakao.com/dashboard"
        download_path = "C:/Downloads"

        account = {
            "id": uid,
            "pw": upw,
            "domain": udomain
        }

        driver = self.get_driver(url, download_path)
        # self.close_popup(driver)
        self.login(driver, account)
        self.move_dashboard(driver, account["domain"])
        # self.press_ok(driver)
        # self.switch_user(driver, account["domain"])
        # self.press_ok(driver)
        # self.move_page(driver, account["domain"])
        # self.select_date(driver, account["domain"])
        # self.download_csv(driver, account["domain"])