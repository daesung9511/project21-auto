import os
import random
import time

from selenium.webdriver.android.webdriver import WebDriver
from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path
import datetime
from pathlib import Path
from dataclasses import dataclass

from selenium.webdriver.remote.webelement import WebElement

from config import CHROME_USER_DATA_PATH, CHROME_PROFILE_NAME, KEY_SHEET_FILE_PATH, RAW_FILE_PATH

from openpyxl import Workbook, worksheet

DEFAULT_TIMEOUT_DELAY = 5


@dataclass
class UserConfig:
    user_data_path: str
    profile_name: str
    download_path: str


class Utils:

    @staticmethod
    def get_chrome_driver() -> WebDriver:
        options = webdriver.ChromeOptions()
        # https://www.python2.net/questions-80772.htm
        options.add_experimental_option("detach", True)
        user_config = Utils._get_config()

        prefs = {
            "profile.default_content_settings.popups": 0,
            f'download.default_directory': user_config.download_path,
            "directory_upgrade": True
        }
        options.add_experimental_option('prefs', prefs)
        options.add_argument(f'--user-data-dir={user_config.user_data_path}')
        options.add_argument(f'--profile-directory={user_config.profile_name}')

        return webdriver.Chrome(chrome_options=options)

    @staticmethod
    def _get_config() -> UserConfig:
        # path
        path = RAW_FILE_PATH if RAW_FILE_PATH != "" else f'{os.path.dirname(os.path.abspath(Path(__file__).parent))}{os.sep}raw_data'
        if not os.path.isdir(path):
            os.mkdir(path)

        # user_data_path
        user_data_path = CHROME_USER_DATA_PATH if CHROME_USER_DATA_PATH != "" else "/Users/qualson/Library/Application Support/Google/Chrome/"
        profile_name = CHROME_PROFILE_NAME if CHROME_PROFILE_NAME != "" else "Profile 2"

        return UserConfig(user_data_path=user_data_path, profile_name=profile_name, download_path=path)

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
    def get_weekday() -> int:
        # It's MONDAY when return value is 0
        return datetime.datetime.today().weekday()

    @staticmethod
    def send_keys_delayed(element: WebElement, input: str):
        for char in input:
            element.send_keys(char)
            time.sleep(random.uniform(0.02, 0.1))

    @staticmethod
    def create_xl_sheet(wb:Workbook, sheet_name: str) -> worksheet:
        rd_ws_name = datetime.datetime.today().strftime("%Y-%m-%d") + sheet_name
        return wb.create_sheet(title=rd_ws_name)
