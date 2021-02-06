from selenium import webdriver

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from utils import Utils

if __name__ == '__main__':
    url = "https://accounts.kakao.com/login/kakaoforbusiness?continue=https://business.kakao.com/dashboard/?sid=kmo&redirect=https://moment.kakao.com/dashboard"
    driver = Utils.get_chrome_driver()
    driver.set_window_size(1980, 1080)
    driver.get(url)
    time.sleep(5)
    el = driver.find_element_by_id("wrap_captcha")
    el.click()