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

# 계정 목록
# - 라베나
#   - lavenakorea / lavena21!   / 네이버 아이디 로그인
# - 유즈
#   - yuge / founders21!    / 일반 로그인
# - 아누아
#   - anua / pista1004!     / 일반 로그인
# - 프로젝트21
#   - pista1004 / pista1004!    / 일반 로그인

accounts = {
    "lavena": {
        "id": "lavenakorea",
        "pw": "lavena21!",
        "type": "naver",
    },
    "yuge": {
        "id": "yuge",
        "pw": "founders21!",
        "type": "general",
    },
    "anua": {
        "id": "anua",
        "pw": "pista1004!",
        "type": "general",
    },
    "project21": {
        "id": "pista1004",
        "pw": "pista1004!",
        "type": "general",
    },
}

options = webdriver.ChromeOptions()
# options.add_argument("headless")
# options.add_experimental_option("detach", True)

driver = webdriver.Chrome("chromedriver.exe", options=options)


login_url = "https://searchad.naver.com/"

def close_popup():
    windows = driver.window_handles
    main = windows[0]
    for window in windows:
        if window != main:
            driver.switch_to.window(window)
            driver.close()

    driver.switch_to.window(main)

def get_driver():
    driver.get(login_url)
    
    driver.implicitly_wait(5)
    
    close_popup()

def naver_login(account):
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


def login(account):
    if account["type"] == "naver":
        naver_login(account)
    else:
        # get id form
        id_form = driver.find_element_by_id("uid")
        id_form.send_keys(account["id"])

        # get pw form
        pw_form = driver.find_element_by_id("upw")
        pw_form.send_keys(account["pw"])
        pw_form.send_keys(Keys.RETURN)

def main():
    # account list
    # lavena, yuge, anua, project21
    account = accounts["lavena"]
    get_driver()
    login(account)
    driver.implicitly_wait(5)
    print(driver.current_url)



if __name__ == "__main__":
    main()