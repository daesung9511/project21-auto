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


class Naver_GFA:

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
                WebDriverWait(driver, sec).until(
                    expected_conditions.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                break
            except Exception as e:
                print(e)

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
        naver_login_button = """body > div > div.container.bg_white > div > div > div.login_box > ul > li.selected > a"""
        self.wait(driver, naver_login_button, 10)
        
        return driver

    def login(self, driver, account):
        # get naver login button
        naver_login_button = driver.find_element_by_css_selector("""body > div > div.container.bg_white > div > div > div.login_box > ul > li.selected > a > span.platform_name""")
        naver_login_button.click()

        # wait for login popup
        naver_banner = """#log\.login"""
        self.wait(driver, naver_banner, DEFAULT_TIMEOUT_DELAY)

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

    def press_ok(self, driver):
        # wait for ok button after login
        login_ok_button = """#app > div > div.container > div.content > div > div.panel_body > span > div > div > div.ly_content > div.ly_footer.type_border > button"""

        try:
            self.wait(driver, login_ok_button, 2)
            driver.find_element_by_css_selector(login_ok_button).click()
        except:
            pass

    def switch_user(self, driver, domain):
        # click user menu dropdown
        user_menu_dropdown = driver.find_element_by_css_selector("""#app > div > div.header > div > ul > li.user > a""")
        user_menu_dropdown.click()

        # wait for user menu
        user_name = """#app > div > div.header > div > ul > li.user > a > span"""
        self.wait(driver, user_name, DEFAULT_TIMEOUT_DELAY)

        pattern = ""
        if domain == "lavena":
            pattern = "라베나코리아"
        elif domain == "yuge":
            pattern = "유즈"
        else:
            pattern = "더파운더즈"

        user = """#app > div > div.header > div > ul > li.active.user > ul > li:nth-child(3) > div > div.account_list.active > div > div > div > ul > li:nth-child(1) > label > span.account_name"""
        try:
            for i in range(1, 10+1):
                user_name = driver.find_element_by_css_selector(f"""#app > div > div.header > div > ul > li.active.user > ul > li:nth-child(3) > div > div.account_list.active > div > div > div > ul > li:nth-child({i}) > label > span.account_name""")
                if pattern in user_name.text:
                    user = f"""#app > div > div.header > div > ul > li.active.user > ul > li:nth-child(3) > div > div.account_list.active > div > div > div > ul > li:nth-child({i}) > label > span.account_name"""
                    break

        except Exception as e:
            print(e)

        # switch user
        user = driver.find_element_by_css_selector(user)
        user.click()

    def move_page(self, driver, domain):
        # click report button 
        report_button = """#app > div > div.container > div.sidebar.undefined > div > div.menu > ul > li.report > a"""
        self.wait(driver, report_button, DEFAULT_TIMEOUT_DELAY)
        driver.find_element_by_css_selector(report_button).click()

        # wait for report name
        report_name = """#app > div > div.container > div.content > div > div.panel_body > div > div > div > div.ad_content > div > div > div > div > div.table_box > div.table_body > div > table > tbody > tr:nth-child(1) > td:nth-child(1) > a"""
        self.wait(driver, report_name, DEFAULT_TIMEOUT_DELAY)
        
        # find report name
        pattern = "광고비 리포트"
        if domain in ("lavena", "yuge"):
            pattern = "광고비 리포트"
        elif domain == "anua":
            pattern = "성과 리포트"
        
        try:
            for i in range(1, 20+1):
                report_name = driver.find_element_by_css_selector(f"""#app > div > div.container > div.content > div > div.panel_body > div > div > div > div.ad_content > div > div > div > div > div.table_box > div.table_body > div > table > tbody > tr:nth-child({i}) > td:nth-child(1) > a""")
                if pattern in report_name.text:
                    # move to detail page
                    report_name.click()
                    break

        except Exception as e:
            print(e)

    def select_date(self, driver, domain):
        date_form = """#app > div > div.container > div.content > div > div.panel_body > div:nth-child(1) > div > div:nth-child(1) > div:nth-child(2) > div > div > div.mx-input-wrapper.calendar_box > button.button.button_data"""
        yesterday_button = """#app > div > div.container > div.content > div > div.panel_body > div:nth-child(1) > div > div:nth-child(1) > div:nth-child(2) > div > div > div.mx-datepicker-popup > div > div.mx-calendar.mx-shortcuts-wrapper > ul > li:nth-child(2) > button"""
        ok_button = """#app > div > div.container > div.content > div > div.panel_body > div:nth-child(1) > div > div:nth-child(1) > div:nth-child(2) > div > div > div.mx-datepicker-popup > div > div.mx-calendar-division > div.mx-datepicker-footer > div > button.mx-datepicker-btn.mx-datepicker-btn-confirm"""
        confirm_button = """#app > div > div.container > div.content > div > div.panel_body > div:nth-child(1) > div > div.center_button > button"""
        if domain in ("lavena", "yuge"):
            confirm_button = """#app > div > div.container > div.content > div > div.panel_body > div:nth-child(1) > div > div.center_button > button"""
        elif domain == "anua":
            confirm_button = """#app > div > div.container > div.content > div > div.panel_body.report > div:nth-child(1) > div > div.center_button > button"""
            

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

        # click campaign button
        if domain == "anua":
            analysis_level = """#app > div > div.container > div.content > div > div.panel_body.report > div:nth-child(1) > div > div:nth-child(2) > div:nth-child(2) > label:nth-child(4) > span"""
            self.wait(driver, analysis_level, DEFAULT_TIMEOUT_DELAY)
            pattern = "캠페인"
            for i in range(1, 20+1):
                try:
                    analysis_level_name = driver.find_element_by_css_selector(f"""#app > div > div.container > div.content > div > div.panel_body.report > div:nth-child(1) > div > div:nth-child(2) > div:nth-child(2) > label:nth-child({i}) > span""")
                    if pattern == analysis_level_name.text:
                        analysis_level_name.click()
                        break
                        
                except:
                    pass

        # click confirm button
        self.wait(driver, confirm_button, DEFAULT_TIMEOUT_DELAY)
        confirm_button = driver.find_element_by_css_selector(confirm_button)
        confirm_button.click()

        # wait for loading
        time.sleep(2)
        
        #
        # TODO : change 3 days if today is MONDAY
        #

    def download_csv(self, driver, domain):
        if domain == "anua":
            download_button = ("""#app > div > div.container > div.content > div > div.panel_body.report > div:nth-child(2) > div > div > div.ad_title > div > div.inner_right > a > button""")
        else:
            download_button = "#app > div > div.container > div.content > div > div.panel_body > div:nth-child(2) > div > div > div.ad_title > div > div.inner_right > a > button"

        driver.find_element_by_css_selector(download_button).click()

        driver.implicitly_wait(1)

    def run(self, uid, upw, udomain):
        # account list
        # lavena, yuge, anua, project21

        url = "https://auth.glad.naver.com/login?destination=http://gfa.naver.com/adAccount"
        download_path = "C:/Downloads"

        account = {
            "id": uid,
            "pw": upw,
            "domain": udomain
        }
        
        driver = Utils.get_chrome_driver()
        driver.set_window_size(1980, 1080)

        driver = self.init(driver, url)
        # self.close_popup(driver)
        self.login(driver, account)
        self.press_ok(driver)
        self.switch_user(driver, account["domain"])
        self.press_ok(driver)
        self.move_page(driver, account["domain"])
        self.select_date(driver, account["domain"])
        self.download_csv(driver, account["domain"])