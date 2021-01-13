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

    def close_popup_facebook(self, driver):
        try:
            accessible_elems = driver.find_elements_by_class_name("accessible_elem")
            for accessible_elem in accessible_elems:
                if accessible_elem.text == "닫기":
                    return accessible_elem
                    break

        except Exception as e:
            return False
        

    def init(self, driver, url):
        driver.get(url)
        
        # Wait for browser loading
        facebook_login_button = """#loginbutton"""
        self.wait(driver, facebook_login_button, 10)
        
        return driver

    def login(self, driver, account):
        time.sleep(1)

        # get facebook id form
        id_form = driver.find_element_by_id("email")
        id_form.send_keys(account["id"])

        time.sleep(1)

        # get facebook pw form
        pw_form = driver.find_element_by_id("pass")
        pw_form.send_keys(account["pw"])

        time.sleep(1)

        # get facebook login button
        facebook_login_button = driver.find_element_by_css_selector("""#loginbutton""")
        facebook_login_button.click()

        # wait for 2fa
        facebook_continue_button = "#checkpointSubmitButton"
        self.wait(driver, facebook_continue_button, DEFAULT_TIMEOUT_DELAY)

        # wait for dashboard in 180 seconds
        facebook_banner = "#global_nav_app_name_id > div > span"
        if self.wait(driver, facebook_banner, DEFAULT_TIMEOUT_DELAY) == False:
            self.wait(driver, facebook_banner, 60)


    def move_dashboard(self, driver, number):
        start = Utils.get_yesterday()
        end = Utils.get_today()
        # when today is MONDAY
        if Utils.get_weekday() == 0:
            start = Utils.get_3daysago()

        url = f"https://business.facebook.com/adsmanager/manage/campaigns?business_id=346749235781856&act={number}&date={start}_{end}&time_breakdown=days_1"
        driver.get(url)

        dashboard_totem = "#pe_toolbar > div > div > div > div:nth-child(1) > div > div:nth-child(1) > div"
        self.wait(driver, dashboard_totem, 10)

        # close popup with agree button
        agree_button = """body > div._10._d2i.uiLayer._4-hy._3qw > div._59s7._9l2g > div > div > div > div > div > div > div._4iyh._2pia._2pi4 > span._4iyi > div > div > button"""
        if self.wait(driver, agree_button, 2):
            driver.find_element_by_css_selector(agree_button).click()

        for _ in range(2):
            time.sleep(0.5)
            accessible_elem = self.close_popup_facebook(driver)
            if accessible_elem:
                accessible_elem.click()

        # wait popup delay
        time.sleep(1)

    def download_csv(self, driver):
        # click report button
        report_button = "#pe_toolbar > div > div > div > div:nth-child(3) > span:nth-child(4)"
        self.wait(driver, report_button, DEFAULT_TIMEOUT_DELAY)
        driver.find_element_by_css_selector(report_button).click()

        # wait for menu
        time.sleep(1)

        # find with xpath
        for i in range(1, 20):
            download_button = f"""//*[@id="facebook"]/body/div[{i}]/div[1]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div/div/div/div/div"""
            try:
                download_button = driver.find_element_by_xpath(download_button)
                if "테이블 데이터 내보내기" in download_button.text:
                    print("Found download!")
                    download_button.click()
                    # wait for menu
                    time.sleep(2)
                    for j in range(1, 20):
                        export_button = f"""//*[@id="facebook"]/body/div[{j}]/div[2]/div/div/div/div/div[1]/div/div[3]/div[2]/div[3]/div[1]/span/div/div/div"""
                        try:
                            export_button = driver.find_element_by_xpath(export_button)
                            if export_button.text == "내보내기":
                                print("Found export!")
                                export_button.click()
                                break
                        except:
                            pass
            except:
                pass

        
        # wait for download
        driver.implicitly_wait(5)
        time.sleep(10)


    def run(self, uid, upw, unumber):
        # account list
        # lavena, yuge, anua, project21

        url = "https://business.facebook.com/login/?next=https://business.facebook.com"

        account = {
            "id": uid,
            "pw": upw,
            "number": unumber
        }
        
        driver = Utils.get_chrome_driver()
        driver.set_window_size(1980, 1080)
        self.init(driver, url)
        self.login(driver, account)
        self.move_dashboard(driver, account["number"])
        self.download_csv(driver)