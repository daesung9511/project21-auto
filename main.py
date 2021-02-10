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
from openpyxl import load_workbook
from config import RD_FILE
import logging
import sys
import traceback

import time


def setup_logger():
    parent = os.path.dirname(os.path.abspath(Path(__file__)))
    file_name = f'{Utils.get_today()}.log'
    path = f'{parent}{os.sep}log'
    if not os.path.isdir(path):
        os.mkdir(path)
    logging.basicConfig(filename=path + os.sep + file_name, level=logging.DEBUG)


def run(platform, account, days, workbooks):
    Utils.kill_proc("chrome*")
    driver = Utils.get_chrome_driver()
    driver.set_window_size(1980, 1080)

    for brand in account["index"]:
        try:
            platform.run(driver, account[brand], days, workbooks)
            message = f"{platform.__class__} {brand} success."
            logging.info(message)
            print(message)
        except Exception as e:
            print(e)
            logging.error(e)
            print(f"{platform.__class__} {brand} failed.")
    driver.quit()


def start(days: int, wbs: dict):
    Utils.backup_original_files()
    Utils.remove_old_backup_files()
    run(Facebook(), ACCOUNTS["facebook"], days, wbs)
    run(Naver_shop(), ACCOUNTS["naver_shop"], days, wbs)
    run(Kakaomoment(), ACCOUNTS["kakaomoment"], days, wbs)
    run(Cafe24(), ACCOUNTS["cafe24"], days, wbs)
    run(Ezadmin(), ACCOUNTS["ezadmin"], days, wbs)
    run(Naver_GFA(), ACCOUNTS["naver_gfa"], days, wbs)


if __name__ == '__main__':
    # setup_logger()
    
    wbs = {}
    domains = ["lavena", "yuge", "anua", "project21"]
    for domain in domains:
        print("Opening - ", domain )
        wbs[domain] = load_workbook(RD_FILE[domain])

    try:
        command = sys.argv[1]
        days: int = int(sys.argv[2])
    except IndexError or ValueError:
        command = "main"
        days = 1
    if command == "":
        start(days, wbs)
    elif command == "main":
        start(days, wbs)
    elif command == "kakaomoment":
        run(Kakaomoment(), ACCOUNTS["kakaomoment"], days, wbs)
    elif command == "facebook":
        run(Facebook(), ACCOUNTS["facebook"], days, wbs)
    elif command == "naver_shop":
        run(Naver_shop(), ACCOUNTS["naver_shop"], days)
    elif command == "naver_gfa":
        run(Naver_GFA(), ACCOUNTS["naver_gfa"], days, wbs)
    elif command == "cafe24":
        run(Cafe24(), ACCOUNTS["cafe24"], days)
    elif command == "ezadmin":
        run(Ezadmin(), ACCOUNTS["ezadmin"], days, wbs)
    
    for domain in domains:
        wbs[domain].save(RD_FILE[domain])