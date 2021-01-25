#coding: utf-8

import datetime
import csv
import os
import fnmatch

from openpyxl import load_workbook
from datetime import datetime

from selenium import webdriver

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from utils import Utils, DEFAULT_TIMEOUT_DELAY


class Kakaomoment:

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
        # get kakao id form
        id_form = driver.find_element_by_id("id_email_2")
        id_form.send_keys(account["id"])

        # get kakao pw form
        pw_form = driver.find_element_by_id("id_password_3")
        pw_form.send_keys(account["pw"])

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

        self.wait(driver, yesterday_button, DEFAULT_TIMEOUT_DELAY)

        if Utils.get_weekday() == 0:
            stat = 0
            stat, start, end = self.calc_date()

            # get calendar elements
            calendar = driver.find_elements_by_css_selector("div.area_calendar")
            left = calendar[0]
            right = calendar[1]

            days = ".inner_link_day"
            prev_days = left.find_elements_by_css_selector(days)
            current_days = right.find_elements_by_css_selector(days)

            # stat 0 : start-right, end-right
            if stat == 0:
                cnt = 0
                for current_day in current_days:
                    if current_day.text in (str(start), str(end)):
                        current_day.click()
                        cnt += 1
                        if cnt == 2:
                            break

                        driver.implicitly_wait(1)

            # stat 1 : start-left, end-left
            elif stat == 1:
                cnt = 0
                for prev_day in prev_days:
                    if prev_day.text in (str(start), str(end)):
                        prev_day.click()
                        cnt += 1
                        if cnt == 2:
                            break

                        driver.implicitly_wait(1)

            # stat 2 : start-left, end-right
            # stat 3 : start-left, end-right
            else:
                for prev_day in prev_days:
                    if prev_day.text == str(start):
                        prev_day.click()
                        driver.implicitly_wait(1)
                        break

                for current_day in current_days:
                    if current_day.text == str(end):
                        current_day.click()
                        break

        else:
            # click yesterday button
            yesterday_button = driver.find_element_by_css_selector(yesterday_button)
            yesterday_button.click()

        # click ok button
        self.wait(driver, ok_button, DEFAULT_TIMEOUT_DELAY)
        ok_button = driver.find_element_by_css_selector(ok_button)
        ok_button.click()

        # wait for loading
        time.sleep(2)

    def download_csv(self, driver, domain):
        if domain == "anua":
            download_button = """#mArticle > div > div.set_table > div.set_head > div.f_right > div:nth-child(4) > a > span > span"""
        if domain == "yuge":
            download_button = """div.set_head > div.f_right > div:nth-child(3) > a > span > span"""

        self.wait(driver, download_button, DEFAULT_TIMEOUT_DELAY)
        download_button = driver.find_element_by_css_selector(download_button)
        download_button.click()

        driver.implicitly_wait(1)
        time.sleep(2)

    def logout(self, driver):
        driver.get("https://accounts.kakao.com/logout?continue=https://accounts.kakao.com/login/kakaoforbusiness?continue=https://business.kakao.com/dashboard/?sid=kmo&redirect=https://moment.kakao.com/dashboard")

    def update_ad_costs(self):
        
        # 엑셀 샘플 파일
        xl_file_path = "kakaomoment_sample.xlsx"

        # RD 엑셀 파일 로딩
        sales_wb = load_workbook(xl_file_path, data_only=True, read_only=False)

        ad_fee_ws = Utils.create_xl_sheet(sales_wb, "-광고비")

        # 시트 헤더 고정
        ad_fee_headings = ['','일자', '요일', '미디어', '상품1', '광고비']
        for idx, header in enumerate(ad_fee_headings):
            ad_fee_ws.cell(row=1, column=idx + 1).value = header
        ad_fee_ws.freeze_panes = 'A2'

        # 카카오모먼트에서 받은 가장 최근 csv 파일 찾기
        # TODO: 다른 모듈에서도 같은로직 반복시 Util 메소드로 변경
        dir_path = "./raw_data/"
        anua_path = ""
        ctime=0
        for file_name in os.listdir(dir_path):
            if fnmatch.fnmatch(file_name, "프로젝트21_맞춤보고서_*.csv"):
                if ctime < os.path.getmtime(dir_path + file_name):
                    ctime = os.path.getmtime(dir_path + file_name)
                    anua_path = file_name
        anua_path = dir_path + anua_path

        with open(anua_path, 'r', encoding='utf-16') as f:
            reader = csv.reader(f, delimiter = "\t")
            next(reader)
            # 광고비 시트에 rd 대입
            for row in reader:
                
                # TODO: 파일에 아누아가 아닌 제품이 있을시 무시
                # 해당 부분이 필요할지 조정
                if not fnmatch.fnmatch(row[1], "아누아_*"):
                    continue
                
                fee_max_row = str(ad_fee_ws.max_row+1)
                
                ad_fee_ws.cell(row=int(fee_max_row),column=1).value = row[1]
                ad_fee_ws.cell(row=int(fee_max_row),column=2).value = datetime.today().strftime("%Y-%m-%d")
                ad_fee_ws.cell(row=int(fee_max_row),column=3).value = '=TEXT(B' + fee_max_row + ',"aaa")'
                ad_fee_ws.cell(row=int(fee_max_row),column=4).value = '카카오광고'
                ad_fee_ws.cell(row=int(fee_max_row),column=5).value = '=VLOOKUP(A' + fee_max_row + ',매칭테이블!B:D,3,0)'
                ad_fee_ws.cell(row=int(fee_max_row),column=6).value = float(row[4])/1.1

        # TODO: 다른 모듈에서도 같은로직 반복시 Util 메소드로 변경
        # 가장최근 yuge csv 파일
        yuge_path = ""
        ctime=0
        for file_name in os.listdir(dir_path):
            if fnmatch.fnmatch(file_name, "유즈_*.csv"):
                if ctime < os.path.getmtime(dir_path + file_name):
                    ctime = os.path.getmtime(dir_path + file_name)
                    yuge_path = file_name
        yuge_path = dir_path + yuge_path

        with open(yuge_path, 'r', encoding='utf-16') as f:
            reader = csv.reader(f, delimiter = "\t")
            next(reader)
            # 광고비 시트에 rd 대입
            for row in reader:
                
                # "집행 중" 상태인 캠페인만 통계
                if not row[1] == "집행 중":
                    continue
                
                fee_max_row = str(ad_fee_ws.max_row+1)
                
                ad_fee_ws.cell(row=int(fee_max_row),column=1).value = row[0]
                ad_fee_ws.cell(row=int(fee_max_row),column=2).value = datetime.today().strftime("%Y-%m-%d")
                ad_fee_ws.cell(row=int(fee_max_row),column=3).value = '=TEXT(B' + fee_max_row + ',"aaa")'
                ad_fee_ws.cell(row=int(fee_max_row),column=4).value = '카카오광고'
                ad_fee_ws.cell(row=int(fee_max_row),column=5).value = '=VLOOKUP(A' + fee_max_row + ',매칭테이블!B:D,3,0)'
                ad_fee_ws.cell(row=int(fee_max_row),column=6).value = float(row[3])/1.1
        
        download_path = 'ad_fee_data.xlsx'
        sales_wb.save(download_path)

    def run(self, driver, account):
        # account list
        # lavena, yuge, anua, project21

        url = "https://accounts.kakao.com/login/kakaoforbusiness?continue=https://business.kakao.com/dashboard/?sid=kmo&redirect=https://moment.kakao.com/dashboard"

        if self.flag:
            self.init(driver, url)
            self.login(driver, account)

        if account["domain"] == "anua":
            self.move_dashboard_anua(driver, account["number"])
        elif account["domain"] == "yuge":
            self.move_dashboard_yuge(driver, account["number"])
        self.select_date(driver, account["domain"])
        self.download_csv(driver, account["domain"])
        self.flag = False

        self.update_ad_costs()