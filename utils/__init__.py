from selenium.webdriver.android.webdriver import WebDriver
from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path

DEFAULT_TIMEOUT_DELAY = 5


class DriverUtils:

    @staticmethod
    def get_chrome_driver() -> WebDriver:
        options = webdriver.ChromeOptions()
        # https://www.python2.net/questions-80772.htm
        options.add_experimental_option("detach", True)
        options.add_argument("download.default_directory=C:/raw_data/")
        return webdriver.Chrome(chrome_options=options)
