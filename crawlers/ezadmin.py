from selenium.webdriver.android.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from utils import DriverUtils, DEFAULT_TIMEOUT_DELAY


class Ezadmin:

    @staticmethod
    def get_admin_page(domain: str, id: str, password: str) -> WebDriver:
        driver = DriverUtils.get_chrome_driver()
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
            print(e)

        try:
            notice_selector = "#pop_top > span > a > img"
            WebDriverWait(driver, DEFAULT_TIMEOUT_DELAY).until(
                expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, notice_selector))
            )
            driver.find_element_by_css_selector(notice_selector).click()
        except Exception as e:
            print(e)

        return driver

    @staticmethod
    def download_yesterday_revenue(domain: str, id: str, password: str) -> WebDriver:
        driver = Ezadmin.get_admin_page(domain, id, password)
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
            driver.implicitly_wait(3)
            driver.switch_to.alert.accept()
        except Exception as e:
            print("검색결과 없음")

        return driver
