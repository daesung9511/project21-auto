from selenium.webdriver.android.webdriver import WebDriver
from selenium import webdriver
from chromedriver_py import binary_path

DEFAULT_TIMEOUT_DELAY = 5


class DriverUtils:

    @staticmethod
    def get_chrome_driver() -> WebDriver:
        options = webdriver.ChromeOptions()
        # https://www.python2.net/questions-80772.htm
        options.add_experimental_option("detach", True)
        return webdriver.Chrome(executable_path=binary_path, chrome_options=options)
