from selenium.webdriver.android.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from utils import Utils, DEFAULT_TIMEOUT_DELAY


class Cafe24:

    @staticmethod
    def get_admin_page(id: str, password: str) -> WebDriver:
        driver = Utils.get_chrome_driver()
        driver.set_window_size(1980, 1080)
        driver.get("https://eclogin.cafe24.com/Shop/")
        id_selector = "#mall_id"
        WebDriverWait(driver, 5).until(
            expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, id_selector))
        )
        driver.find_element_by_css_selector(id_selector).send_keys(id)
        driver.find_element_by_css_selector("#userpasswd").send_keys(password)
        driver.find_element_by_css_selector(
            "#tabAdmin > div > fieldset > p.gButton > a").click()

        # Login complete
        return driver

    @staticmethod
    def download_lacto_revenue(id: str, password: str) -> WebDriver:
        driver = Cafe24.get_admin_page(id, password)
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
                    print("File is not ready retry download")
                    driver.implicitly_wait(1)  # wait for some delay

                driver.close()
            else:
                print("First excel sheet is not correct")
                # Stop download loop because something wrong happend
                download_done = True
            driver.switch_to.window(original_window)

        return driver
