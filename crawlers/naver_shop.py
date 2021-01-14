#coding: utf-8

import time
import datetime
import pyperclip
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import ElementNotVisibleException
from utils import Utils, DEFAULT_TIMEOUT_DELAY


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
                expected_conditions.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            return True
        except Exception as e:
            return False

    def wait_xpath(self, driver, selector, sec):
        try:
            WebDriverWait(driver, sec).until(
                expected_conditions.presence_of_element_located((By.XPATH, selector))
            )
            return True
        except Exception as e:
            return False

    def wait_popup(self, driver, selector, sec):
        while True:
            try:
                self.switch_popup(driver)
                WebDriverWait(driver, 1).until(
                    expected_conditions.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                break
            except:
                print("[*] Didn't find a login popup!")

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
        naver_login_button = "#container > main > div > div.spot > home-login > div > div > button"
        self.wait(driver, naver_login_button, 10)
        
        return driver

    def naver_login(self, driver, account):
        # get naver login button
        naver_login = driver.find_element_by_class_name("naver_login_btn")
        naver_login.click()

        # wait for login popup
        naver_banner = "#log\.login"
        self.wait_popup(driver, naver_banner, DEFAULT_TIMEOUT_DELAY)

        # get naver id form
        id_form = driver.find_element_by_id("id")
        clip_id = pyperclip.copy(account["id"])
        id_form.click()
        id_form.send_keys(Keys.CONTROL, "v")

        # get naver pw form
        pw_form = driver.find_element_by_id("pw")
        clip_pw = pyperclip.copy(account["pw"])
        pw_form.click()
        pw_form.send_keys(Keys.CONTROL, "v")

        # get login button
        login_button = driver.find_element_by_id("log.login")
        login_button.click()

    def login(self, driver, account):
        if account["type"] == "naver":
            self.naver_login(driver, account)

        else:
            # get id form
            id_form = driver.find_element_by_id("uid")
            id_form.send_keys(account["id"])

            # get pw form
            pw_form = driver.find_element_by_id("upw")
            pw_form.send_keys(account["pw"])

            pw_form.send_keys(Keys.RETURN)

    def move_page(self, driver, utype):
        # return to main window
        self.switch_main(driver)

        # close welcome popup
        login_ok_button = "#mat-dialog-0 > naver-login-confirm > mat-dialog-content > div.margin-top-30.button-area-center > button > span"
        if utype == "naver":
            self.wait(driver, login_ok_button, DEFAULT_TIMEOUT_DELAY)
            driver.find_element_by_css_selector(login_ok_button).click()

        # click AD Management button
        ad_management_button = "#container > my-screen > div > div.spot > div > my-screen-board > div > div.top > div.b_sec01 > board-campaign-type > div.sec_top > a"
        self.wait(driver, ad_management_button, DEFAULT_TIMEOUT_DELAY)
        driver.find_element_by_css_selector(ad_management_button).click()

        date_button = ".inner-right > div > div > span > div > div"
        self.wait_popup(driver, date_button, DEFAULT_TIMEOUT_DELAY)

    def calc_date(self):
        today = datetime.date.today()
        token = datetime.timedelta(1)

        d1 = today - token
        d2 = d1 - token
        d3 = d2 - token

        stat = 0
        # 1 days ago : prev month
        if d1.day < 0:
            start = d3.day
            end = d1.day
            stat = 1
        
        # 2 days ago : prev month
        elif d2.day < 0:
            start = d2.day
            stat = 2
        
        # 3 days ago : prev month
        elif d3.day < 0:
            start = d1.day
            stat = 3

        else:
            stat = 0
            start = d3.day
            end = d1.day

        return stat, start, end

    def select_date(self, driver, uid):
        if uid != "lavenakorea":
            driver.find_element_by_css_selector("#root > div > div.header > div > div:nth-child(1) > div.header-second-row > div > div > div:nth-child(1) > ul > li:nth-child(2) > div > a").click()
            multi_report = "#root > div > div.header > div > div:nth-child(1) > div.header-second-row > div > div > div:nth-child(1) > ul > li.nav-item.active > div > div > div:nth-child(1) > a > button"
            self.wait(driver, multi_report, DEFAULT_TIMEOUT_DELAY)
            driver.find_element_by_css_selector(multi_report).click()
            
            try:
                for i in range(1, 20+1):
                    # #root > div > div.sc-pTIqm.hbMQAb > div > div > div.sc-ptDSg.eYGQDi > div > div.sc-fzpdyU.bpAxtW > table > tbody > tr:nth-child(1) > td:nth-child(2) > a
                    report_name = f".data-table-tbody > tr:nth-child({i}) > td:nth-child(2) > a"
                    self.wait(driver, report_name, DEFAULT_TIMEOUT_DELAY)
                    report_name = driver.find_element_by_css_selector(report_name)

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

            date_form = ".right-side > div:nth-child(1) > div > div:nth-child(1) > div.right > div > div > span > div > div"
            yesterday_button = ".right-side > div:nth-child(1) > div > div:nth-child(1) > div.right > div > div > div > div:nth-child(1) > div:nth-child(1)"
            ok_button = ".right-side > div:nth-child(1) > div > div:nth-child(1) > div.right > div > div > div > div:nth-child(3) > div:nth-child(2) > button:nth-child(1)"
        
        else:
            # click date form
            date_form = ".inner-right > div > div > span > div > div"
            yesterday_button = ".inner-right > div > div > div > div:nth-child(1) > div:nth-child(2)"
            ok_button = ".inner-right > div > div > div > div:nth-child(3) > div:nth-child(2) > button:nth-child(1)"

        # click date form
        self.wait(driver, date_form, DEFAULT_TIMEOUT_DELAY)
        driver.find_element_by_css_selector(date_form).click()
        driver.implicitly_wait(1)

        # wait yesterday button
        # self.wait(driver, yesterday_button, DEFAULT_TIMEOUT_DELAY)

        if Utils.get_weekday() == 0:
        # if True:
            stat = 0
            stat, start, end = self.calc_date()

            if uid != "lavenakorea":
                if uid == "yuge":
                    this_week_button = ".right-side > div:nth-child(1) > div > div:nth-child(1) > div.right > div > div > div > div:nth-child(1) > div:nth-child(5)"
                    driver.find_element_by_css_selector(this_week_button).click()
                    driver.implicitly_wait(1)
                    
                    driver.find_element_by_css_selector(date_form).click()
                    driver.implicitly_wait(1)

                # get calendar elements
                left = driver.find_element_by_css_selector(".right-side > div:nth-child(1) > div > div:nth-child(1) > div.right > div > div > div > div:nth-child(2) > div:nth-child(1)")
                right = driver.find_element_by_css_selector(".right-side > div:nth-child(1) > div > div:nth-child(1) > div.right > div > div > div > div:nth-child(2) > div:nth-child(2)")

                days = "div:nth-child(2) > div:nth-child(3) > ul span"
                start_days = left.find_elements_by_css_selector(days)
                end_days = right.find_elements_by_css_selector(days)

                left_prev_button = left.find_element_by_css_selector("div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div > button:nth-child(2)")
                right_prev_button = right.find_element_by_css_selector("div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div > button:nth-child(2)")
                    
            else:
                # get calendar elements
                left = driver.find_element_by_css_selector(".inner-right > div > div > div > div:nth-child(2) > div:nth-child(1)")
                right = driver.find_element_by_css_selector(".inner-right > div > div > div > div:nth-child(2) > div:nth-child(2)")

                days = "div:nth-child(2) > div:nth-child(3) > ul span"
                start_days = left.find_elements_by_css_selector(days)
                end_days = right.find_elements_by_css_selector(days)

                left_prev_button = left.find_element_by_css_selector("div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div > button:nth-child(2)")
                right_prev_button = right.find_element_by_css_selector("div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div > button:nth-child(2)")
            
            # stat 0 : start-right, end-right
            if stat == 0:
                pass

            # stat 1 : start-left, end-left
            elif stat == 1:
                # click prev month(start, end)
                left_prev_button.click()
                driver.implicitly_wait(1)
                right_prev_button.click()
                driver.implicitly_wait(1)

            # stat 2 : start-left, end-right
            # stat 3 : start-left, end-right
            else:
                # click prev month(start)
                left_prev_button.click()
                driver.implicitly_wait(1)

            flag = False
            for start_day in start_days:
                if start_day.text == "1" and flag == False:
                    flag = True

                if flag and start_day.text == str(start):
                    start_day.click()
                    driver.implicitly_wait(1)
                    break
            
            flag = False
            for end_day in end_days:
                if end_day.text == "1" and flag == False:
                    flag = True

                if flag and end_day.text == str(end):
                    end_day.click()
                    driver.implicitly_wait(1)
                    break

            self.wait(driver, ok_button, DEFAULT_TIMEOUT_DELAY)
            driver.find_element_by_css_selector(ok_button).click()

        else:
            yesterdaybutton_ = driver.find_element_by_css_selector(yesterday_button)
            yesterdaybutton_.click()

        driver.implicitly_wait(1)

    def download_csv(self, driver, uid):
        if uid == "lavenakorea":
            download_button = driver.find_element_by_css_selector("#root > div > div:nth-child(2) > div > div:nth-child(3) > div > div:nth-child(1) > div:nth-child(1) > div.right > div > button")
        else:
            download_button = driver.find_element_by_css_selector("#root > div > div:nth-child(2) > div > div > div:nth-child(1) > div:nth-child(3) > button")

        download_button.click()
        
        driver.implicitly_wait(1)
        time.sleep(2)

    def logout(self, driver, uid):
        logout_button = "#root > div > div:nth-child(1) > div > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > ul > li:nth-child(1) > span"
        driver.find_element_by_css_selector(logout_button).click()
        
        if uid == "lavenakorea":
            real_logout_button = "#container > div > div > div > div > div > button.mat-button-md.mat-raised-button.mat-button-base.mat-primary > span"
            self.wait(driver, real_logout_button, DEFAULT_TIMEOUT_DELAY)
            driver.find_element_by_css_selector(real_logout_button).click()

    def clear_tabs(self, driver):
        windows = driver.window_handles
        main = windows[-1]
        for window in windows:
            if window != main:
                driver.switch_to.window(window)
                driver.close()

        driver.switch_to.window(main)

    def run(self, driver, account):
        # account list
        # lavena, yuge, anua, project21

        url = "https://searchad.naver.com/"

        self.init(driver, url)
        self.close_popup(driver)
        self.switch_main(driver)
        self.login(driver, account)
        self.move_page(driver, account["type"])
        self.select_date(driver, account["id"])
        self.download_csv(driver, account["id"])
        self.logout(driver, account["id"])
        self.clear_tabs(driver)
        driver.delete_all_cookies()