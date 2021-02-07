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
import sys


def setup_logger():
    parent = os.path.dirname(os.path.abspath(Path(__file__)))
    file_name = f'{Utils.get_today()}.log'
    path = f'{parent}{os.sep}log'
    if not os.path.isdir(path):
        os.mkdir(path)
    logging.basicConfig(filename=path + os.sep + file_name, level=logging.DEBUG)


def run(platform, account, days):

    Utils.kill_proc("chrome*")
    driver = Utils.get_chrome_driver()
    driver.set_window_size(1980, 1080)

    for brand in account["index"]:
        try:
            platform.run(driver, account[brand], days)
            message = f"{platform.__class__} {brand} success."
            logging.info(message)
            print(message)
        except Exception as e:
            logging.error(e)
            print(f"{platform.__class__} {brand} failed.")
    driver.quit()


def start():

    # run(Facebook(), ACCOUNTS["facebook"])
    # run(Naver_shop(), ACCOUNTS["naver_shop"])
    # run(Kakaomoment(), ACCOUNTS["kakaomoment"])
    run(Cafe24(), ACCOUNTS["cafe24"], 1)
    # run(Ezadmin(), ACCOUNTS["ezadmin"])
    # run(Naver_GFA(), ACCOUNTS["naver_gfa"])

    Utils.set_xl_formula()
    
if __name__ == '__main__':
    # setup_logger()

    try:
        command = sys.argv[1]
    except IndexError:
        command = "main"

    if command == "":
        start()
    elif command == "main":
        start()
    elif command == "kakaomoment":
        run(Kakaomoment(), ACCOUNTS["kakaomoment"], 3)
    elif command == "facebook":
        run(Facebook(), ACCOUNTS["facebook"], 3)
    elif command == "naver_shop":
        run(Naver_shop(), ACCOUNTS["naver_shop"], 1)
    elif command == "naver_gfa":
        run(Naver_GFA(), ACCOUNTS["naver_gfa"], 3)
    elif command == "cafe24":
        run(Cafe24(), ACCOUNTS["cafe24"], 3)
    elif command == "ezadmin":
        run(Ezadmin(), ACCOUNTS["ezadmin"], 1)
