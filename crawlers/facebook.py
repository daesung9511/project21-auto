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
from utils import Utils, DEFAULT_TIMEOUT_DELAY


class Facebook:

    def switch_popup(self, driver):
        windows = driver.window_handles
        driver.switch_to.window(windows[-1])  
        
    def switch_main(self, driver):
        windows = driver.window_handles
        driver.switch_to.window(windows[0])

    def wait(self, driver, selector, sec):
        try:
            WebDriverWait(driver, sec).until(
                expected_conditions.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
        except:
            pass

    def wait_popup(self, driver, selector, sec):
        while True:
            try:
                self.switch_popup(driver)
                WebDriverWait(driver, sec).until(
                    expected_conditions.presence_of_element_located((By.CSS_SELECTOR, selector))
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

    def init(self, driver, url):
        driver.get(url)
        
        # Wait for browser loading
        kakao_login_button = """#login-form > fieldset > div.wrap_btn > button.btn_g.btn_confirm.submit"""
        self.wait(driver, kakao_login_button, 10)
        
        return driver

    def login(self, driver, account):
        time.sleep(1)

        # get kakao id form
        id_form = driver.find_element_by_id("id_email_2")
        id_form.send_keys(account["id"])

        time.sleep(1)

        # get kakao pw form
        pw_form = driver.find_element_by_id("id_password_3")
        pw_form.send_keys(account["pw"])

        time.sleep(1)

        # get kakao login button
        kakao_login_button = driver.find_element_by_css_selector("""#login-form > fieldset > div.wrap_btn > button.btn_g.btn_confirm.submit""")
        kakao_login_button.click()

        # wait for login
        dashboard = """#kakaoContent > div.cont_feature > ul > li.on > a"""

        try:
            self.wait(driver, dashboard, DEFAULT_TIMEOUT_DELAY)
        except:
            time.sleep(1)

    def move_dashboard_anua(self, driver, number):
        # dashboard url 
        dashboard_url = f"https://moment.kakao.com/{number}/report/customreport/all"

        #move to dashboard
        driver.get(dashboard_url)
        
        # find report name
        report_name = """#mArticle > div > div.ad_managebox > div.tblg2_wrap > table > tbody > tr:nth-child(1) > td:nth-child(2) > div > a"""
        self.wait(driver, report_name, DEFAULT_TIMEOUT_DELAY)

        pattern = "광고비"
        try:
            for i in range(1, 10+1):
                report_name = f"""#mArticle > div > div.ad_managebox > div.tblg2_wrap > table > tbody > tr:nth-child({i}) > td:nth-child(2) > div > a"""
                report_name_element = driver.find_element_by_css_selector(report_name)
                if pattern == report_name_element.text:
                    report_name_element.click()
                    break
        except Exception as e:
            print(e)

        date_form = """#mArticle > div > div.set_table > div.set_head > div.f_right > div:nth-child(3) > div > div.btn_gm.gm_calendar > a"""
        self.wait(driver, date_form, DEFAULT_TIMEOUT_DELAY)

    def move_dashboard_yuge(self, driver, number):
        # dashboard url 
        dashboard_url = f"https://moment.kakao.com/dashboard/{number}"

        # move to dashboard
        driver.get(dashboard_url)

        # click ok button on alert
        ok_button = """#app > section > div:nth-child(4) > div > div > div > div.layer_foot > div > button > span"""
        try:
            self.wait(driver, ok_button, DEFAULT_TIMEOUT_DELAY)
            driver.find_element_by_css_selector(ok_button).click()
        except Exception as e:
            print(e)

        date_form = """#mArticle > div > div.dashboard_check > div.f_right > div:nth-child(1) > div > div.btn_gm.gm_calendar > a"""
        self.wait(driver, date_form, DEFAULT_TIMEOUT_DELAY)

    def select_date(self, driver, domain):
        if domain == "anua":
            date_form = """#mArticle > div > div.set_table > div.set_head > div.f_right > div:nth-child(3) > div > div.btn_gm.gm_calendar > a"""
            yesterday_button = """#mArticle > div > div.set_table > div.set_head > div.f_right > div:nth-child(3) > div > div.btn_gm.gm_calendar.open > div > div > div.layer_body > ul > li.on > a"""
            ok_button = """#mArticle > div > div.set_table > div.set_head > div.f_right > div:nth-child(3) > div > div.btn_gm.gm_calendar.open > div > div > div.layer_body > div > div.btn_wrap > button.btn_gm.gm_bl > span"""
        elif domain == "yuge":
            date_form = """#mArticle > div > div.dashboard_check > div.f_right > div:nth-child(1) > div > div.btn_gm.gm_calendar > a"""
            yesterday_button = """#mArticle > div > div.dashboard_check > div.f_right > div:nth-child(1) > div > div.btn_gm.gm_calendar.open > div > div > div.layer_body > ul > li:nth-child(2) > a"""
            ok_button = """#mArticle > div > div.dashboard_check > div.f_right > div:nth-child(1) > div > div.btn_gm.gm_calendar.open > div > div > div.layer_body > div > div.btn_wrap > button.btn_gm.gm_bl > span"""

        # click date form
        self.wait(driver, date_form, DEFAULT_TIMEOUT_DELAY)
        date_form = driver.find_element_by_css_selector(date_form)
        date_form.click()

        # click yesterday button
        self.wait(driver, yesterday_button, DEFAULT_TIMEOUT_DELAY)
        yesterday_button = driver.find_element_by_css_selector(yesterday_button)
        yesterday_button.click()

        # click ok button
        self.wait(driver, ok_button, DEFAULT_TIMEOUT_DELAY)
        ok_button = driver.find_element_by_css_selector(ok_button)
        ok_button.click()

        # wait for loading
        time.sleep(2)
        
        #
        # TODO : change 3 days if today is MONDAY
        #

    def download_csv(self, driver, domain):
        if domain == "anua":
            download_button = """#mArticle > div > div.set_table > div.set_head > div.f_right > div:nth-child(4) > a > span > span"""
        if domain == "yuge":
            download_button = """div.set_head > div.f_right > div:nth-child(3) > a > span > span"""

        self.wait(driver, download_button, DEFAULT_TIMEOUT_DELAY)
        download_button = driver.find_element_by_css_selector(download_button)
        download_button.click()

        time.sleep(5)

    def run(self, uid, upw, udomain, unumber):
        # account list
        # lavena, yuge, anua, project21

        url = "https://accounts.kakao.com/login/kakaoforbusiness?continue=https://business.kakao.com/dashboard/?sid=kmo&redirect=https://moment.kakao.com/dashboard"

        account = {
            "id": uid,
            "pw": upw,
            "domain": udomain,
            "number": unumber
        }
        
        driver = Utils.get_chrome_driver()
        driver.set_window_size(1980, 1080)
        self.init(driver, url)
        self.login(driver, account)
        if account["domain"] == "anua":
            self.move_dashboard_anua(driver, account["number"])
        elif account["domain"] == "yuge":
            self.move_dashboard_yuge(driver, account["number"])
        self.select_date(driver, account["domain"])
        self.download_csv(driver, account["domain"])