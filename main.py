import os
from pathlib import Path

from crawlers.cafe24 import Cafe24
from crawlers.ezadmin import Ezadmin
from crawlers.naver_shop import Naver_shop
from crawlers.naver_gfa import Naver_GFA
from crawlers.kakaomoment import Kakaomoment
from crawlers.facebook import Facebook
from utils import Utils
from secrets import ACCOUNTS
import logging


def setup_logger():
    parent = os.path.dirname(os.path.abspath(Path(__file__)))
    file_name = f'{Utils.get_today()}.log'
    path = f'{parent}{os.sep}log'
    if not os.path.isdir(path):
        os.mkdir(path)
    logging.basicConfig(filename=path + os.sep + file_name, level=logging.DEBUG)


def run(platform, account):
    driver = Utils.get_chrome_driver()
    driver.set_window_size(1980, 1080)

    for brand in account["index"]:
        try:
            platform.run(driver, account[brand])
            message = f"{platform.__class__} {brand} success."
            logging.info(message)
            print(message)
        except Exception as e:
            logging.error(e)
            print(f"{platform.__class__} {brand} failed.")
    driver.quit()


def start():
    run(Facebook(), ACCOUNTS["facebook"])
    run(Naver_shop(), ACCOUNTS["naver_shop"])
    run(Naver_GFA(), ACCOUNTS["naver_gfa"])
    run(Kakaomoment(), ACCOUNTS["kakaomoment"])
    run(Cafe24, ACCOUNTS["cafe24"])
    run(Ezadmin, ACCOUNTS["ezadmin"])


if __name__ == '__main__':
    setup_logger()
    start()
