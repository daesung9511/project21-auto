import os
import random
import time

from selenium.webdriver.android.webdriver import WebDriver
from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path
import datetime
from pathlib import Path

from selenium.webdriver.remote.webelement import WebElement

DEFAULT_TIMEOUT_DELAY = 5


class Utils:

    @staticmethod
    def get_chrome_driver() -> WebDriver:
        options = webdriver.ChromeOptions()
        # https://www.python2.net/questions-80772.htm
        options.add_experimental_option("detach", True)

        parent = os.path.dirname(os.path.abspath(Path(__file__).parent))
        path = parent + '\\raw_data'

        if os.path.isdir(path) == False:
            os.mkdir(path)

        prefs = {
            "profile.default_content_settings.popups": 0,
            'download.default_directory': path,
            "directory_upgrade": True
        }
        options.add_experimental_option('prefs', prefs)
        return webdriver.Chrome(chrome_options=options)

    @staticmethod
    def get_today() -> str:
        return datetime.date.today().isoformat()

    @staticmethod
    def get_yesterday() -> str:
        date = datetime.date.today() - datetime.timedelta(1)
        return date.isoformat()

    @staticmethod
    def get_3daysago() -> str:
        date = datetime.date.today() - datetime.timedelta(3)
        return date.isoformat()

    @staticmethod
    def get_weekday() -> str:
        # It's MONDAY when return value is 0
        return datetime.datetime.today().weekday()

    @staticmethod
    def send_keys_delayed(element: WebElement, input: str):
        for char in input:
            element.send_keys(char)
            time.sleep(random.uniform(0.02, 0.1))
