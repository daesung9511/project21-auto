from selenium.webdriver.android.webdriver import WebDriver
from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path
import datetime

DEFAULT_TIMEOUT_DELAY = 5


class Utils:

    @staticmethod
    def get_chrome_driver() -> WebDriver:
        options = webdriver.ChromeOptions()
        # https://www.python2.net/questions-80772.htm
        options.add_experimental_option("detach", True)
        options.add_argument("download.default_directory=~/raw_data/")
        return webdriver.Chrome(chrome_options=options)

    @staticmethod
    def get_today() -> str:
        return datetime.date.today().isoformat()

    @staticmethod
    def get_yesterday() -> str:
        date = datetime.date.today() - datetime.timedelta(1)
        return date.isoformat()
