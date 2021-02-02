# coding: utf-8

import datetime
import time

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from openpyxl import load_workbook
import os
import fnmatch
import csv

from utils import Utils, DEFAULT_TIMEOUT_DELAY, AD_FEE_FILE

class Naver_GFA:
    flag = True

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
        naver_login_button = driver.find_element_by_css_selector(
            """body > div > div.container.bg_white > div > div > div.login_box > ul > li.selected > a > span.platform_name""")
        naver_login_button.click()

        # wait for login popup
        naver_banner = """#log\.login"""
        self.wait(driver, naver_banner, DEFAULT_TIMEOUT_DELAY)

        # get naver id form
        id_form = driver.find_element_by_id("id")
        Utils.send_keys_delayed(id_form, account["id"])

        # get naver pw form
        pw_form = driver.find_element_by_id("pw")
        Utils.send_keys_delayed(pw_form, account["pw"])

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

    def switch_user(self, driver: WebDriver, domain):
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

        def get_user_query_selector(index: int) -> str:
            return f"#app > div > div.header > div > ul > li.active.user > ul > li:nth-child(3) > div > div.account_list.active > div > div > div > ul > li:nth-child({index}) > label > span.account_name"

        user_index = 1
        for i in range(1, 20 + 1):
            try:
                user_name = driver.find_element_by_css_selector(get_user_query_selector(i))
                if pattern in user_name.text:
                    user_index = i  # found user
                    break
            except:
                pass

        user_query_selector = get_user_query_selector(user_index)  # set default value

        # switch user
        user = driver.find_element_by_css_selector(user_query_selector)
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
            for i in range(1, 20 + 1):
                report_name = driver.find_element_by_css_selector(
                    f"""#app > div > div.container > div.content > div > div.panel_body > div > div > div > div.ad_content > div > div > div > div > div.table_box > div.table_body > div > table > tbody > tr:nth-child({i}) > td:nth-child(1) > a""")
                if pattern in report_name.text:
                    # move to detail page
                    report_name.click()
                    break

        except Exception as e:
            print(e)

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

    def select_date(self, driver, domain):
        date_form = """#app > div > div.container > div.content > div > div.panel_body > div:nth-child(1) > div > div:nth-child(1) > div:nth-child(2) > div > div > div.mx-input-wrapper.calendar_box > button.button.button_data"""
        ok_button = """#app > div > div.container > div.content > div > div.panel_body > div:nth-child(1) > div > div:nth-child(1) > div:nth-child(2) > div > div > div.mx-datepicker-popup > div > div.mx-calendar-division > div.mx-datepicker-footer > div > button.mx-datepicker-btn.mx-datepicker-btn-confirm"""
        confirm_button = """#app > div > div.container > div.content > div > div.panel_body > div:nth-child(1) > div > div.center_button > button"""
        if domain in ("lavena", "yuge"):
            yesterday_button = """#app > div > div.container > div.content > div > div.panel_body > div:nth-child(1) > div > div:nth-child(1) > div:nth-child(2) > div > div > div.mx-datepicker-popup > div > div.mx-calendar.mx-shortcuts-wrapper > ul > li:nth-child(2) > button"""
            confirm_button = """#app > div > div.container > div.content > div > div.panel_body > div:nth-child(1) > div > div.center_button > button"""
        elif domain == "anua":
            yesterday_button = "#app > div > div.container > div.content > div > div.panel_body.report > div:nth-child(1) > div > div:nth-child(1) > div:nth-child(2) > div > div > div.mx-datepicker-popup > div > div.mx-calendar.mx-shortcuts-wrapper > ul > li:nth-child(2) > button"
            confirm_button = """#app > div > div.container > div.content > div > div.panel_body.report > div:nth-child(1) > div > div.center_button > button"""

        # click date form
        self.wait(driver, date_form, DEFAULT_TIMEOUT_DELAY)
        date_form = driver.find_element_by_css_selector(date_form)
        date_form.click()

        # wait yesterday button
        self.wait(driver, yesterday_button, DEFAULT_TIMEOUT_DELAY)

        if Utils.get_weekday() == 0:
            # if True:
            stat = 0
            stat, start, end = self.calc_date()

            # get calendar elements
            left = driver.find_element_by_css_selector(".mx-calendar-start-date")
            right = driver.find_element_by_css_selector(".mx-calendar-end-date")

            days = ".mx-calendar-content td"
            start_days = left.find_elements_by_css_selector(days)
            end_days = right.find_elements_by_css_selector(days)

            left_prev_button = left.find_element_by_css_selector(".mx-calendar-header > a")
            right_prev_button = right.find_element_by_css_selector(".mx-calendar-header > a")

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

        else:
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
            for i in range(1, 20 + 1):
                try:
                    analysis_level_name = driver.find_element_by_css_selector(
                        f"""#app > div > div.container > div.content > div > div.panel_body.report > div:nth-child(1) > div > div:nth-child(2) > div:nth-child(2) > label:nth-child({i}) > span""")
                    if pattern == analysis_level_name.text:
                        analysis_level_name.click()
                        break

                except:
                    pass

        # click confirm button
        self.wait(driver, confirm_button, DEFAULT_TIMEOUT_DELAY)
        confirm_button = driver.find_element_by_css_selector(confirm_button)
        confirm_button.click()

    def download_csv(self, driver, domain):
        if domain == "anua":
            download_button = "#app > div > div.container > div.content > div > div.panel_body.report > div:nth-child(2) > div > div > div.ad_title > div > div.inner_right > a > button"
        else:
            download_button = "#app > div > div.container > div.content > div > div.panel_body > div:nth-child(2) > div > div > div.ad_title > div > div.inner_right > a > button"

        driver.find_element_by_css_selector(download_button).click()

        driver.implicitly_wait(1)
        time.sleep(2)

    def logout(self, driver):
        logout_button = "li.logout > a"
        driver.find_element_by_css_selector(logout_button).click()

    def clear_tabs(self, driver):
        windows = driver.window_handles
        main = windows[-1]
        for window in windows:
            if window != main:
                driver.switch_to.window(window)
                driver.close()

        driver.switch_to.window(main)

    def update_ad_costs(self, domain):
    
        # RD 엑셀 파일 로딩
        sales_wb = load_workbook(AD_FEE_FILE, data_only=True, read_only=False)

        ad_fee_ws = Utils.create_xl_sheet(sales_wb, "-광고비")

        # 시트 헤더 고정
        ad_fee_headings = ['','일자', '요일', '미디어', '상품1', '광고비(VAT미포함)']
        for idx, header in enumerate(ad_fee_headings):
            ad_fee_ws.cell(row=1, column=idx + 1).value = header
        ad_fee_ws.freeze_panes = 'A2'

        if domain == "yuge":

            # 유즈 csv 파일 찾기
            yuge_path = Utils.get_recent_file("유즈_광고비리포트_*.csv")

            with open(yuge_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter = ",")
                next(reader)
                # 광고비 시트에 rd 대입
                for row in reader:
                    
                    fee_max_row = str(ad_fee_ws.max_row+1)
                    
                    ad_fee_ws.cell(row=int(fee_max_row),column=1).value = row[0]
                    ad_fee_ws.cell(row=int(fee_max_row),column=2).value = datetime.datetime.today().strftime("%Y-%m-%d")
                    ad_fee_ws.cell(row=int(fee_max_row),column=3).value = '=TEXT(B' + fee_max_row + ',"aaa")'
                    ad_fee_ws.cell(row=int(fee_max_row),column=4).value = '네이버 GFA'
                    ad_fee_ws.cell(row=int(fee_max_row),column=5).value = '=VLOOKUP(A' + fee_max_row + ',매칭테이블!B:D,3,0)'
                    ad_fee_ws.cell(row=int(fee_max_row),column=6).value = float(row[3])/1.1
        
        elif domain == "anua":
        
            anua_path = Utils.get_recent_file("더파운더즈_성과리포트_*.csv")

            with open(anua_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter = ",")
                next(reader)
                # 광고비 시트에 rd 대입
                for row in reader:
                    
                    fee_max_row = str(ad_fee_ws.max_row+1)
                    
                    ad_fee_ws.cell(row=int(fee_max_row),column=1).value = row[0]
                    ad_fee_ws.cell(row=int(fee_max_row),column=2).value = datetime.datetime.today().strftime("%Y-%m-%d")
                    ad_fee_ws.cell(row=int(fee_max_row),column=3).value = '=TEXT(B' + fee_max_row + ',"aaa")'
                    ad_fee_ws.cell(row=int(fee_max_row),column=4).value = '네이버 GFA'
                    ad_fee_ws.cell(row=int(fee_max_row),column=5).value = '=VLOOKUP(A' + fee_max_row + ',매칭테이블!B:D,3,0)'
                    ad_fee_ws.cell(row=int(fee_max_row),column=6).value = float(row[12])/1.1
            
        elif domain == "lavena":

            lavena_path = Utils.get_recent_file("라베나코리아_광고비리포트_*.csv")

            with open(lavena_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter = ",")
                next(reader)
                # 광고비 시트에 rd 대입
                for row in reader:
                    
                    fee_max_row = str(ad_fee_ws.max_row+1)
                    
                    ad_fee_ws.cell(row=int(fee_max_row),column=1).value = row[0]
                    ad_fee_ws.cell(row=int(fee_max_row),column=2).value = datetime.datetime.today().strftime("%Y-%m-%d")
                    ad_fee_ws.cell(row=int(fee_max_row),column=4).value = '네이버 GFA'
                    ad_fee_ws.cell(row=int(fee_max_row),column=6).value = float(row[3])/1.1
            
        sales_wb.save(AD_FEE_FILE)


    def run(self, driver, account):
        # account list
        # lavena, yuge, anua, project21

        url = "https://auth.glad.naver.com/login?destination=http://gfa.naver.com/adAccount"

        # if self.flag:
        #     self.init(driver, url)
        #     # self.close_popup(driver)
        #     self.login(driver, account)
        
        self.init(driver, url)
        naver_login_button = driver.find_element_by_css_selector(
            """body > div > div.container.bg_white > div > div > div.login_box > ul > li.selected > a > span.platform_name""")
        
        naver_login_button.click()
        time.sleep(5)
        self.switch_user(driver, account["domain"])
        self.press_ok(driver)
        self.move_page(driver, account["domain"])
        self.select_date(driver, account["domain"])
        self.download_csv(driver, account["domain"])
        self.clear_tabs(driver)
        self.flag = False
        self.update_ad_costs()
