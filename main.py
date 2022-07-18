import os
import time
from pathlib import Path
from typing import List

from crawlers.cafe24 import Cafe24
from crawlers.ezadmin import Ezadmin
from crawlers.naver_shop import Naver_shop
from crawlers.naver_gfa import Naver_GFA
from crawlers.kakaomoment import Kakaomoment
from crawlers.facebook import Facebook
from crawlers.google import Google
from utils import Utils
from secrets import ACCOUNTS
from openpyxl import load_workbook
from config import RD_FILE
import logging
import sys
import traceback



def setup_logger():
    parent = os.path.dirname(os.path.abspath(Path(__file__)))
    file_name = f'{Utils.get_today()}.log'
    path = f'{parent}{os.sep}log'
    if not os.path.isdir(path):
        os.mkdir(path)
    logging.basicConfig(filename=path + os.sep + file_name, level=logging.DEBUG)


def run(platform, account, days, workbooks, domains):
    Utils.kill_proc("chrome*")
    driver = Utils.get_chrome_driver()
    driver.maximize_window()

    for brand in account["index"]:
        try:
            if brand in domains:
                platform.run(driver, account[brand], days, workbooks)
                message = f"{platform.__class__} {brand} success."
                logging.info(message)
                print(message)
        except Exception as e:
            print(traceback.format_exc())
            logging.error(e)
            print(f"{platform.__class__} {brand} failed.")
    driver.quit()


def start(days: int, wbs: dict, domains: List[str]):
    Utils.backup_original_files()
    Utils.remove_old_backup_files()
    run(Facebook(), ACCOUNTS["facebook"], days, wbs, domains)
    # run(Google(), ACCOUNTS["google"], days, wbs, domains)
    run(Naver_shop(), ACCOUNTS["naver_shop"], days, wbs, domains)
    run(Kakaomoment(), ACCOUNTS["kakaomoment"], days, wbs, domains)
    # run(Cafe24(), ACCOUNTS["cafe24"], days, wbs, domains)
    run(Ezadmin(), ACCOUNTS["ezadmin"], days, wbs, domains)
    run(Naver_GFA(), ACCOUNTS["naver_gfa"], days, wbs, domains)


if __name__ == '__main__':
    setup_logger()
    brands = ["lavena", "yuge", "anua", "project21"]
    wbs = {}
    if len(sys.argv) < 4:
        domains = ["lavena", "yuge", "anua", "project21"]
    else:
        domains = sys.argv[3:]
    for domain in domains:
        if domain not in brands:
            raise Exception(f'올바르지 않은 브랜드 명입니다 다시확인해주세요! {domains}')

    for domain in domains:
        print("Opening - ", domain)
        wbs[domain] = load_workbook(Utils._get_raw_file_path(RD_FILE[domain]))
        print("Opened - ", domain)
    try:
        try:
            command = sys.argv[1]
            days: int = int(sys.argv[2])
        except IndexError or ValueError:
            command = "main"
            days = 1
        if command == "":
            start(days, wbs, domains)
        elif command == "main":
            start(days, wbs, domains)
        elif command == "kakaomoment":
            run(Kakaomoment(), ACCOUNTS["kakaomoment"], days, wbs, domains)
        elif command == "facebook":
            run(Facebook(), ACCOUNTS["facebook"], days, wbs, domains)
        elif command == "naver_shop":
            run(Naver_shop(), ACCOUNTS["naver_shop"], days, wbs, domains)
        elif command == "naver_gfa":
            run(Naver_GFA(), ACCOUNTS["naver_gfa"], days, wbs, domains)
        elif command == "cafe24":
            run(Cafe24(), ACCOUNTS["cafe24"], days, wbs, domains)
        elif command == "ezadmin":
            run(Ezadmin(), ACCOUNTS["ezadmin"], days, wbs, domains)
        elif command == "google":
            run(Google(), ACCOUNTS["google"], days, wbs, domains)
    finally:
        for domain, wb in wbs.items():
            print("Closing - ", domain)
            wbs[domain].save(Utils._get_raw_file_path(RD_FILE[domain]))
            wb.close()
            print("Closed - ", domain)
