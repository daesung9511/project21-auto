from selenium.webdriver.android.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import logging

import datetime
from openpyxl import Workbook
from openpyxl import load_workbook

import time

import csv
import os
import fnmatch
from bs4 import BeautifulSoup
import re

from utils import Utils, DEFAULT_TIMEOUT_DELAY
from config import RD_FILE


class Ezadmin:

    def run(self, driver, account, days):
        uid = account["id"]
        upw = account["pw"]
        udomain = account["domain"]
        # for day in range(days, 0, -1):
        #     Ezadmin.download_yesterday_revenue(driver, udomain, uid, upw, 3)
        #     Ezadmin.update_rd_data(account["domain"], day)
        Ezadmin.update_rd_data(account["domain"], days)
    
    @staticmethod
    def get_admin_page(driver: WebDriver, domain: str, id: str, password: str) -> WebDriver:
        driver.get("https://www.ezadmin.co.kr/index.html#main")
        WebDriverWait(driver, 3).until(
            expected_conditions.presence_of_all_elements_located((By.ID, "login-popup"))
        )
        driver.find_element_by_css_selector("#header > div.utilWrap > ul > li.login > a").click()

        driver.find_element_by_css_selector("#login-domain").send_keys(domain)
        driver.find_element_by_css_selector("#login-id").send_keys(id)
        pw_element = driver.find_element_by_css_selector("#login-pwd")
        pw_element.clear()
        pw_element.send_keys(password)

        driver.find_element_by_css_selector(
            "#login-popup > div.content-inner > form:nth-child(4) > input.login-btn").click()

        # Login complete
        try:
            keep_password_selector = "#passwd_keep > a:nth-child(6) > img"
            WebDriverWait(driver, DEFAULT_TIMEOUT_DELAY).until(
                expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, keep_password_selector))
            )
            driver.find_element_by_css_selector(keep_password_selector).click()
        except Exception as e:
            logging.warning(e)

        try:
            notice_selector = "#pop_top > span > a > img"
            WebDriverWait(driver, DEFAULT_TIMEOUT_DELAY).until(
                expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, notice_selector))
            )
            driver.find_element_by_css_selector(notice_selector).click()
        except Exception as e:
            logging.warning(e)

        return driver

    @staticmethod
    def download_yesterday_revenue(driver: WebDriver, domain: str, id: str, password: str, day: int) -> WebDriver:
        date = (datetime.datetime.now() + datetime.timedelta(days=-day)).strftime('%Y-%m-%d')

        driver = Ezadmin.get_admin_page(driver, domain, id, password)

        menu_selector = "#mymenu > a"
        driver.find_element_by_css_selector(menu_selector).click()

        for idx in range(1, 11):
            revenue_selector = "#mymenu_list > li:nth-child(" + str(idx) + ") > a"
            WebDriverWait(driver, DEFAULT_TIMEOUT_DELAY).until(
                expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, revenue_selector))
            )
            menu = driver.find_element_by_css_selector(revenue_selector)
            if menu.text == "판매처상품매출통계":
                menu.click()
                break
        time.sleep(3)
        query_type = '#query_type'
        select = Select(driver.find_element_by_css_selector(query_type))
        select.select_by_value('order_date')

        date_selector = 'input.datepicker.hasDatepicker'
        date_inputs = driver.find_elements_by_css_selector(date_selector)
        
        for date_input in date_inputs:
            length = len(date_input.get_attribute('value'))
            date_input.send_keys(length * Keys.BACKSPACE)
            date_input.send_keys(date)

        driver.find_element_by_css_selector('#search').click()

        try:
            query_result_selector = '#table_container > table > tbody > tr:nth-child(2) > td:nth-child(1)'
            WebDriverWait(driver, DEFAULT_TIMEOUT_DELAY).until(
                expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, query_result_selector))
            )

            download = '#download'
            driver.find_element_by_css_selector(download).click()
            WebDriverWait(driver, DEFAULT_TIMEOUT_DELAY).until(
                expected_conditions.alert_is_present()
            )
            driver.switch_to.alert.accept()
            time.sleep(3)
        except Exception as e:
            logging.debug(f"검색결과 없음 {e}")
            raise NameError("검색결과 없음") from e

        return driver

    @staticmethod
    def update_rd_data(domain: str, day: float):
        
        # 매칭테이블 엑셀 파일 로딩 (sales 매칭테이블))
        sales_wb = load_workbook(RD_FILE[domain], data_only=True, read_only=False)

        # TODO: 해당 날짜 시트겹치는 것 체크
        sales_ws = Utils.create_xl_sheet(sales_wb, "RD")

        # Open Ezadmin rd file
        xls_path = Utils.get_recent_file("판매처상품매출통계*.xls") 

        f = open(xls_path, 'r', encoding='UTF8')
        datas = Ezadmin.parse_html_data(f)
        datas.pop(0)
        for data in datas:
            sales_max_row = str(sales_ws.max_row+1)
            matching = data[3] + data[4]
            try:
                sales_ws["B" + sales_max_row].value = data[0]
                sales_ws["E" + sales_max_row].value = Utils.vlookup(sales_wb["매칭테이블"], matching, "상품1")
                sales_ws["F" + sales_max_row].value = data[1]
                sales_ws["G" + sales_max_row].value = matching
                sales_ws["H" + sales_max_row].value = data[6]
                sales_ws["I" + sales_max_row].value = Utils.vlookup(sales_wb["매칭테이블"], matching, "상품2")
                sales_ws["K" + sales_max_row].value = Utils.vlookup(sales_wb["매칭테이블"], matching, "구분(판매가)")
                sales_ws["L" + sales_max_row].value = int(Utils.vlookup(sales_wb["매칭테이블"], matching, "판매가")) * data[6]
                sales_ws["M" + sales_max_row].value = (100-int(Utils.vlookup(sales_wb["매칭테이블"], matching, "수수료").strip("%"))) / 100 * float(Utils.vlookup(sales_wb["매칭테이블"], matching, "판매가")) * data[6]
                sales_ws["N" + sales_max_row].value = int(Utils.vlookup(sales_wb["매칭테이블"], matching, "원가")) * data[6]
                sales_ws["O" + sales_max_row].value = int(Utils.vlookup(sales_wb["매칭테이블"], matching, "판매가")) * data[6] / 1.1
            except Exception:
                print("erre")
        sales_wb.save(RD_FILE[domain])

    @staticmethod
    def update_rd_data_legacy(domain: str, day: float):

        # 매칭테이블 엑셀 파일 로딩 (sales 매칭테이블))
        sales_wb = load_workbook(RD_FILE[domain], data_only=True, read_only=False)

        # TODO: 해당 날짜 시트겹치는 것 체크
        sales_ws = Utils.create_xl_sheet(sales_wb, "RD")

        # Cafe24에서 받은 csv 파일 찾기
        csv_path = Utils.get_recent_file("판매처상품매출통계_*.xls") 

        with open(csv_path, 'r', encoding='UTF8') as f:
            reader = csv.reader(f)
            next(reader)    # 첫행(헤더 셀) 무시

            # 카페24 RD 피벗테이블 작성
            for row in reader:
    
                sales_max_row = str(sales_ws.max_row+1)
                
                # 피벗 테이블 결과를 통한 판매실적 시트 채우기
                sales_ws["A" + sales_max_row].value = row[2] + row[3]
                sales_ws["B" + sales_max_row].value = Utils.get_day(day)
                sales_ws["F" + sales_max_row].value = "프로젝트21 홈페이지"
                sales_ws["I" + sales_max_row].value = '201207'
                sales_ws["H" + sales_max_row].value = row[8]

        sales_wb.save(RD_FILE[domain])

    @staticmethod
    def download_yesterday_revenue_legacy(driver: WebDriver, domain: str, id: str, password: str) -> WebDriver:
        driver = Ezadmin.get_admin_page(driver, domain, id, password)
        menu_selector = "#mymenu > a"
        driver.find_element_by_css_selector(menu_selector).click()

        revenue_selector = "#mymenu_list > li:nth-child(3) > a"
        WebDriverWait(driver, DEFAULT_TIMEOUT_DELAY).until(
            expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, revenue_selector))
        )
        driver.find_element_by_css_selector(revenue_selector).click()

        query_type = '#query_type'
        select = Select(driver.find_element_by_css_selector(query_type))
        select.select_by_value('order_date')

        query_date = '#date_period_sel'
        date_select = Select(driver.find_element_by_css_selector(query_date))
        date_select.select_by_value('2')

        driver.find_element_by_css_selector('#search').click()
        try:
            query_result_selector = '#table_container > table > tbody > tr:nth-child(2) > td:nth-child(1)'
            WebDriverWait(driver, DEFAULT_TIMEOUT_DELAY).until(
                expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, query_result_selector))
            )

            download = '#download'
            driver.find_element_by_css_selector(download).click()
            WebDriverWait(driver, DEFAULT_TIMEOUT_DELAY).until(
                expected_conditions.alert_is_present()
            )
            driver.switch_to.alert.accept()
        except Exception as e:
            logging.debug(f"검색결과 없음 {e}")
            raise NameError("검색결과 없음") from e

        return driver

    @staticmethod
    def wait(self, driver, selector, sec):
        try:
            WebDriverWait(driver, sec).until(
                expected_conditions.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            return True
        except Exception as e:
            return False


    @staticmethod
    def parse_html_data(input):

        soup = BeautifulSoup(input, 'html.parser')
        rows = soup.table.find_all('tr')
        data = []
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            if len(cols) > 5:
                data.append([ele for ele in cols if ele]) # Get rid of empty values
                
        return data
