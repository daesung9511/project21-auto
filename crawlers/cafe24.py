from selenium.webdriver.android.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import logging

from openpyxl.styles import PatternFill, Color
from openpyxl import Workbook
from openpyxl import load_workbook

from datetime import datetime
import csv
import os
import fnmatch


from utils import Utils, DEFAULT_TIMEOUT_DELAY, SALES_FILE


class Cafe24:
    def run(self, driver, account):
        uid = account["id"]
        upw = account["pw"]
        Cafe24.download_lacto_revenue(driver, uid, upw)
        Cafe24.update_rd_data()

    @staticmethod
    def get_admin_page(driver: WebDriver, id: str, password: str) -> WebDriver:
        
        driver.get("https://eclogin.cafe24.com/Shop/")
        id_selector = "#mall_id"
        WebDriverWait(driver, 5).until(
            expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, id_selector))
        )
        driver.find_element_by_css_selector(id_selector).send_keys(id)
        driver.find_element_by_css_selector("#userpasswd").send_keys(password)
        driver.find_element_by_css_selector(
            "#frm_user > div.tabCont > div.mButton > button").click()

        # Login complete
        return driver

    @staticmethod
    def download_lacto_revenue(driver:WebDriver, id: str, password: str) -> WebDriver:
        
        driver = Cafe24.get_admin_page(driver, id, password)
        driver.get("https://project21.cafe24.com/disp/admin/shop1/report/ProductPrdchart")

        report_base_url = "https://project21.cafe24.com/disp/admin/shop1/report/ProductPrdchart"
        product_name = "유산균"
        start_date = Utils.get_yesterday()
        end_date = Utils.get_yesterday()
        report_query = f"?searchDateRange=7&eOrderProductCode=&eOrderProductNo=&eOrderProductTag=&rows=10&sOrderBy=sale_cnt&sType=item&excel_public_auth=T&start_date={start_date}&end_date={end_date}&sCategory-1=&eProductSearchType=product_name&eOrderProductText={product_name}&sManufacturerCode=&sTrendCode=&sBrandCode=&sSupplierCode=&sClassificationCode=&iStartProductPrice=0&iEndProductPrice=0&sMobileFlag=ALL&sOverseaFlag=ALL"

        driver.get(f"{report_base_url}{report_query}")

        original_window = driver.current_window_handle

        request_excel_selector = "#QA_product3 > div.mState > div.gRight > div > a > span"
        WebDriverWait(driver, DEFAULT_TIMEOUT_DELAY).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, request_excel_selector))
        )
        driver.find_element_by_css_selector(request_excel_selector).click()

        excel_download_selector = "#eExcelDownloadButton"
        WebDriverWait(driver, DEFAULT_TIMEOUT_DELAY).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, excel_download_selector))
        )
        driver.find_element_by_css_selector(excel_download_selector).click()

        WebDriverWait(driver, DEFAULT_TIMEOUT_DELAY).until(
            expected_conditions.alert_is_present()
        )
        driver.switch_to.alert.dismiss()

        download_done = False

        while not download_done:

            # open download popup
            driver.find_element_by_css_selector("#eExcelDownloadPopup > span").click()

            for handle in driver.window_handles:
                driver.switch_to.window(handle)

            first_date = driver.find_element_by_css_selector("#eFileListBody > tr:nth-child(1) > td:nth-child(1)").text
            if first_date == f"{start_date} ~ {end_date}":
                first_date_selector = "#eFileListBody > tr:nth-child(1) > td:nth-child(4)"
                if driver.find_element_by_css_selector(first_date_selector).text == "엑셀다운로드":
                    driver.find_element_by_css_selector(
                        "#eFileListBody > tr:nth-child(1) > td:nth-child(4) > a > span").click()
                    download_done = True
                else:
                    logging.debug("File is not ready retry download")
                    driver.implicitly_wait(1)  # wait for some delay

                driver.close()
            else:
                logging.debug("First excel sheet is not correct")
                # Stop download loop because something wrong happend
                download_done = True
            driver.switch_to.window(original_window)

        return driver

    @staticmethod
    def update_rd_data():

        # 매칭테이블 엑셀 파일 로딩 (sales 매칭테이블))
        sales_wb = load_workbook(SALES_FILE, data_only=True, read_only=False)

        # TODO: 해당 날짜 시트없을 시 처리해줘야함
        rd_ws = Utils.create_xl_sheet(sales_wb, "-카페24 RD")

        # 시트 헤더 고정
        rd_headings = ['날짜', '매칭', '<분류>', '순위', '상품코드', '상품명',
                       '옵션', '판매가', '재고', '결제수량', '환불수량', '판매수량', '판매합계']
        for idx, header in enumerate(rd_headings):
            rd_ws.cell(row=1, column=idx + 1).value = header
        rd_ws.freeze_panes = 'A2'

        # TODO: 해당 날짜 시트겹치는 것 체크
        sales_ws = Utils.create_xl_sheet(sales_wb, "-판매실적")

        # 시트 헤더 고정
        sales_headings = ['', '일자', '요일', '미디어', '상품1', '채널', '상품2', '판매수량',
                          '구분(판매가)', '광고비(VAT미포함)', '판매액', '판매액(수수료제외)', '원가', '구분값']
        for idx, header in enumerate(sales_headings):
            sales_ws.cell(row = 1, column = idx + 1).value = header
        sales_ws.freeze_panes = 'A2'

        # Cafe24에서 받은 csv 파일 찾기
        csv_path = Utils.get_recent_file("*_ProductPrdchart.csv") 

        with open(csv_path, 'r', encoding='UTF8') as f:
            reader = csv.reader(f)
            next(reader)    # 첫행(헤더 셀) 무시

            # 카페24 RD 피벗테이블 작성
            for row in reader:

                rd_max_row = str(rd_ws.max_row+1)
                sales_max_row = str(sales_ws.max_row+1)

                # B, C 열 함수 설정 및 A열 값 채우기
                rd_ws["A" + rd_max_row].value = datetime.today().strftime("%Y-%m-%d")
                rd_ws["B" + rd_max_row] = "=F" + rd_max_row + "&G" + rd_max_row
                rd_ws["C" + rd_max_row] = "=VLOOKUP(B" + rd_max_row + ",'카페24 매칭'!B:C,2,0)"

                # 셀 스타일 세팅
                rd_ws["C" + rd_max_row].fill = rd_ws["B" + rd_max_row].fill = PatternFill(
                    start_color='fff2cc', end_color='fff2cc', fill_type='solid')

                for idx, data in enumerate(row):
                    # 카페24 RD 피벗테이블에 데이터 대입
                    rd_ws.cell(row=int(rd_max_row),
                               column=idx + 4).value = data

                # 피벗 테이블 결과를 통한 판매실적 시트 채우기
                sales_ws["B" + sales_max_row].value = datetime.today().strftime("%Y-%m-%d")
                sales_ws["C" + sales_max_row] = '=TEXT(B' + sales_max_row + ',"aaa")'
                sales_ws["E" + sales_max_row] = '=VLOOKUP(G' + sales_max_row + ',매칭테이블!D:E,2,0)'
                sales_ws["F" + sales_max_row].value = "프로젝트21 홈페이지"
                sales_ws["I" + sales_max_row].value = '201207'
                sales_ws["K" + sales_max_row] = '=VLOOKUP($N' + sales_max_row + ',매칭테이블!$G:$J,2,0)*H' + sales_max_row
                sales_ws["L" + sales_max_row] = '=K' + sales_max_row + '-VLOOKUP($N' + sales_max_row + ',매칭테이블!$G:$J,3,0)*K' + sales_max_row
                sales_ws["M" + sales_max_row] = '=VLOOKUP($N' + sales_max_row + ',매칭테이블!$G:$J,4,0)*H' + sales_max_row
                sales_ws["N" + sales_max_row] = '=F' + sales_max_row + '&E' + sales_max_row + '&G' + sales_max_row + '&I' + sales_max_row
                sales_ws["G" + sales_max_row] = "='" + datetime.today().strftime("%Y-%m-%d") + "-카페24 RD" + "'!C" + rd_max_row
                sales_ws["H" + sales_max_row].value = rd_ws["L" + rd_max_row].value

                # 셀 스타일 세팅
                color_cells = ["C", "E", "I", "J", "K", "L", "M", "N"]
                for cell in color_cells:
                    sales_ws[cell + sales_max_row].fill = PatternFill(start_color='fff2cc', end_color='fff2cc', fill_type='solid')

        sales_wb.save(SALES_FILE)
