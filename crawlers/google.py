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


class Google:

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
        google_login_button = """#identifierNext > div > button > span"""
        self.wait(driver, google_login_button, 10)
        
        return driver

    def login(self, driver, account):
        time.sleep(1)

        # get google id form
        id_form = driver.find_element_by_id("identifierId")
        id_form.send_keys(account["id"])

        time.sleep(1)

        # click next button
        id_next_button = """#identifierNext > div > button"""
        driver.find_element_by_css_selector(id_next_button).click()

        # Wait for password loading
        password_next_button = """#passwordNext > div > button"""
        self.wait(driver, password_next_button, DEFAULT_TIMEOUT_DELAY)

        # get google pw form
        pw_form = """#password > div[1] > div > div[1] > input"""
        pw_form = driver.find_element_by_css_selector(pw_form)
        pw_form.send_keys(account["pw"])

        time.sleep(1)

        # click google login button
        driver.find_element_by_css_selector(password_next_button).click()

        # wait for loading
        dashboard_totem = "body > div:nth-child(6) > root > div > div.awsm-main._ngcontent-awn-AWSM-0 > div > div > div.awsm-content._ngcontent-awn-AWSM-0 > awsm-skinny-nav > div > div > div:nth-child(2) > awsm-skinny-nav-item:nth-child(1) > a > material-ripple"
        self.wait(driver, dashboard_totem, 10)

    def move_dashboard(self, driver, number):
        # click campaign button
        campaign_button = "body > div:nth-child(6) > root > div > div.awsm-main._ngcontent-awn-AWSM-0 > div > div > div.awsm-content._ngcontent-awn-AWSM-0 > awsm-skinny-nav > div > div > div:nth-child(2) > awsm-skinny-nav-item:nth-child(1) > a > material-ripple"
        driver.find_element_by_css_selector(campaign_button).click()

        # wait for loading
        campaign_totem = "#cmExtensionPoint-id > base-root > div > div.header-sticky-container._ngcontent-awn-CM-1 > div > div.datepicker-container._ngcontent-awn-CM-1 > material-date-range-picker > div > div.dropdown-and-comparison._ngcontent-awn-CM-4 > span > dropdown-button"
        self.wait(driver, campaign_totem, DEFAULT_TIMEOUT_DELAY)

    def select_date(self, driver):
        # click dropdown button
        dropdown_button = "#cmExtensionPoint-id > base-root > div > div.header-sticky-container._ngcontent-awn-CM-1 > div > div.datepicker-container._ngcontent-awn-CM-1 > material-date-range-picker > div > div.dropdown-and-comparison._ngcontent-awn-CM-4 > span > dropdown-button"
        driver.find_element_by_css_selector(dropdown_button).click()

        # wait for yesterday button
        yesterday = "material-select-item[2] > span"
        yesterday = driver.find_element_by_css_selector(yesterday)
        yesterday.click()

        print("asdfasdf")

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


    def run(self, uid, upw):
        # account list
        # lavena, yuge, anua, project21

        url = "https://accounts.google.com/signin/v2/identifier?service=adwords&passive=1209600&osid=1&continue=https://ads.google.com/nav/login?subid=ALL-ko-et-g-aw-c-home-awhp_xin1_signin!o2&followup=https://ads.google.com/nav/login?subid=ALL-ko-et-g-aw-c-home-awhp_xin1_signin!o2&flowName=GlifWebSignIn&flowEntry=ServiceLogin"

        account = {
            "id": uid,
            "pw": upw,
        }
        
        driver = Utils.get_firefox_driver()
        driver.set_window_size(1980, 1080)
        self.init(driver, url)
        self.login(driver, account)
        self.move_dashboard(driver, account["number"])
        self.select_date(driver)
        self.download_csv(driver)
        time.sleep(600)