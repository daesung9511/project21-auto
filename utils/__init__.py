import os
import random
import time
import psutil

from selenium.webdriver.android.webdriver import WebDriver
from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path
import datetime
from pathlib import Path
from dataclasses import dataclass

from selenium.webdriver.remote.webelement import WebElement

from config import CHROME_USER_DATA_PATH, CHROME_PROFILE_NAME, CHROME_GFA_PROFILE_NAME, KEY_SHEET_FILE_PATH, RAW_FILE_PATH

from openpyxl import Workbook, worksheet, load_workbook
import fnmatch

DEFAULT_TIMEOUT_DELAY = 5

# 매칭테이블 포함 데이터 엑셀 파일
RD_FILE = {  "lavena": "lavena_rd_data.xlsx",
                "anua": "anua_rd_data.xlsx",
                "yuge": "yuge_rd_data.xlsx",
                "project21": "project21_rd_data.xlsx", 
            }


@dataclass
class UserConfig:
    user_data_path: str
    profile_name: str
    gfa_profile_name: str
    download_path: str
    


class Utils:

    @staticmethod
    def get_chrome_driver() -> WebDriver:
        
        options = webdriver.ChromeOptions()
        # https://www.python2.net/questions-80772.htm
        options.add_experimental_option("detach", True)
        user_config = Utils._get_config()
        print("down")
        print(user_config.download_path)
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
    def get_chrome_driver_gfa() -> WebDriver:
        
        options = webdriver.ChromeOptions()
        # https://www.python2.net/questions-80772.htm
        options.add_experimental_option("detach", True)
        user_config = Utils._get_config()
        print("down")
        print(user_config.download_path)
        prefs = {
            "profile.default_content_settings.popups": 0,
            f'download.default_directory': user_config.download_path,
            "directory_upgrade": True
        }
        options.add_experimental_option('prefs', prefs)
        options.add_argument(f'--user-data-dir={user_config.user_data_path}')
        options.add_argument(f'--profile-directory={user_config.gfa_profile_name}')

        return webdriver.Chrome(chrome_options=options)
        

    @staticmethod
    def _get_config() -> UserConfig:
        # path
        path = RAW_FILE_PATH if RAW_FILE_PATH != "" else f'{os.path.dirname(os.path.abspath(Path(__file__).parent))}{os.sep}raw_data'
        if not os.path.isdir(path):
            os.mkdir(path)

        # user_data_path
        user_data_path = CHROME_USER_DATA_PATH if CHROME_USER_DATA_PATH != "" else "/Users/qualson/Library/Application Support/Google/Chrome/Profile 2"
        profile_name = CHROME_PROFILE_NAME if CHROME_PROFILE_NAME != "" else "Profile 2"
        gfa_profile_name = CHROME_GFA_PROFILE_NAME if CHROME_GFA_PROFILE_NAME != "" else "Profile 3"

        return UserConfig(user_data_path=user_data_path, profile_name=profile_name, gfa_profile_name=gfa_profile_name, download_path=path)

    @staticmethod
    def get_day(ago: float) -> str:
        date = datetime.date.today() - datetime.timedelta(ago)
        return date.isoformat()

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
    def kill_proc(proc_exp: str):
        for proc in psutil.process_iter():
            if fnmatch.fnmatch(proc.name(), proc_exp):
                proc.kill()
    
    @staticmethod
    def create_xl_sheet(wb: Workbook, sheet_name: str) -> worksheet:
        rd_ws_name = sheet_name
        ws = None
        if rd_ws_name in wb.sheetnames:
            ws = wb[rd_ws_name]
        else:
            ws = wb.create_sheet(rd_ws_name)
        return ws

    @staticmethod
    def get_recent_file(expression: str) -> str:
        dir_path = "." + os.sep + "raw_data" + os.sep
        file_path = ""
        ctime = 0
        for file_name in os.listdir(dir_path):
            if fnmatch.fnmatch(file_name, expression):
                if ctime < os.path.getmtime(dir_path + file_name):
                    ctime = os.path.getmtime(dir_path + file_name)
                    file_path = file_name
        return dir_path + file_path

    @staticmethod
    def set_xl_formula() -> str:
        for domain, file in RD_FILE.items():
            wb = load_workbook(file, data_only=True, read_only=False)

            ws = Utils.create_xl_sheet(wb, "RD")

            max_row = ws.max_row
            for rd_row in range(2, max_row + 1):
                rd_row = str(rd_row)
                ws["C" + rd_row] = '=TEXT(B' + rd_row + ',"aaa")'
                ws["E" + rd_row] = '=VLOOKUP(G' + rd_row + ',매칭테이블!D:E,2,0)'
                ws["K" + rd_row] = '=VLOOKUP($N' + rd_row + ',매칭테이블!$G:$J,2,0)*H' + rd_row
                ws["L" + rd_row] = '=K' + rd_row + '-VLOOKUP($N' + rd_row + ',매칭테이블!$G:$J,3,0)*K' + rd_row
                ws["M" + rd_row] = '=VLOOKUP($N' + rd_row + ',매칭테이블!$G:$J,4,0)*H' + rd_row
                ws["N" + rd_row] = '=F' + rd_row + '&E' + rd_row + '&G' + rd_row + '&I' + rd_row
                ws["G" + rd_row] = "=VLOOKUP(A" + rd_row + ",'카페24 매칭'!B:C,2,0)"

            wb.save(file)

