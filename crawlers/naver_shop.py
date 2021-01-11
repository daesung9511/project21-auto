#coding: utf-8
#
# Naver Shopping CSV Automation
#
# Date : 2021. 01. 11
# Author : choiys(Yongseon Choi)
# Email : hcy3bkj@gmail.com
#

import time
import selenium
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import ElementNotVisibleException

class Naver_shop:

    def close_popup(self, driver):
        windows = driver.window_handles
        main = windows[0]
        for window in windows:
            if window != main:
                driver.switch_to.window(window)
                driver.close()

        driver.switch_to.window(main)

    def get_driver(self, login_url, download_path):
        options = webdriver.ChromeOptions()
        # options.add_argument("headless")
        # options.add_experimental_option("detach", True)
        base_path = "download.default_directory="
        download_path = base_path + download_path
        options.add_argument("download_path")

        driver = webdriver.Chrome("chromedriver.exe", options=options)

        driver.get(login_url)
        
        driver.implicitly_wait(5)
        
        return driver

    def naver_login(self, driver, account):
        # get naver login button
        naver_login = driver.find_element_by_class_name("naver_login_btn")
        naver_login.click()

        time.sleep(2)

        # switch to popup window
        windows = driver.window_handles
        driver.switch_to.window(windows[-1])

        # get naver id form
        id_form = driver.find_element_by_id("id")
        clip_id = pyperclip.copy(account["id"])
        id_form.click()
        id_form.send_keys(Keys.CONTROL, "v")

        time.sleep(1)

        # get naver pw form
        pw_form = driver.find_element_by_id("pw")
        clip_pw = pyperclip.copy(account["pw"])
        pw_form.click()
        pw_form.send_keys(Keys.CONTROL, "v")

        time.sleep(1)

        # get login button
        login_button = driver.find_element_by_id("log.login")
        login_button.click()

        # return to main window
        driver.switch_to.window(windows[0])

        time.sleep(2)

    def login(self, driver, account):
        if account["type"] == "naver":
            self.naver_login(driver, account)
        else:
            # get id form
            id_form = driver.find_element_by_id("uid")
            id_form.send_keys(account["id"])

            # get pw form
            pw_form = driver.find_element_by_id("upw")
            pw_form.send_keys(account["pw"])
            pw_form.send_keys(Keys.RETURN)

    def move_page(self, driver):
        # click ok button
        ok_button = driver.find_element_by_css_selector("#mat-dialog-0 > naver-login-confirm > mat-dialog-content > div.margin-top-30.button-area-center > button")
        ok_button.click()

        driver.implicitly_wait(1)

        # click AD Management button
        ad_management_button = driver.find_element_by_xpath("//*[@id='container']/my-screen/div/div[1]/div/my-screen-board/div/div[1]/div[1]/board-campaign-type/div[1]/a")
        ad_management_button.click()

        time.sleep(4)

    def select_date(self, driver):
        # switch to report tab
        driver.switch_to.window(driver.window_handles[-1])

        # click date form
        date_form = driver.find_element_by_xpath("//*[@id='root']/div/div[2]/div/div[1]/div/div[2]/div/div/span/div/div")
        date_form.click()

        driver.implicitly_wait(1)

        # click yesterday button
        yesterday_button = driver.find_element_by_xpath("//*[@id='root']/div/div[2]/div/div[1]/div/div[2]/div/div/div/div[1]/div[2]/span")
        yesterday_button.click()

        time.sleep(2)
        
        #
        # TODO : change 3 days if today is MONDAY
        #

    def download_csv(self, driver):
        download_button = driver.find_element_by_xpath("//*[@id='root']/div/div[2]/div/div[3]/div/div[1]/div[1]/div[2]/div/button")
        download_button.click()

        driver.implicitly_wait(5)
        time.sleep(5)

    def run(self, uid, upw, utype):
        # account list
        # lavena, yuge, anua, project21

        login_url = "https://searchad.naver.com/"
        download_path = "C:/Downloads"

        account = {
            "id": uid,
            "pw": upw,
            "type": utype
        }

        driver = self.get_driver(login_url, download_path)
        self.close_popup(driver)

        self.login(driver, account)
        driver.implicitly_wait(2)

        self.move_page(driver)
        driver.implicitly_wait(1)
        self.select_date(driver)

        self.download_csv(driver)