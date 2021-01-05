from selenium.webdriver.android.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from driver_utils import DriverUtils, DEFAULT_TIMEOUT_DELAY


class Ezadmin:

    @staticmethod
    def get_admin_page(domain: str, id: str, password: str) -> WebDriver:
        driver = DriverUtils.get_chrome_driver()
        driver.get("https://www.ezadmin.co.kr/index.html#main")
        WebDriverWait(driver, DEFAULT_TIMEOUT_DELAY).until(
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

        return driver
