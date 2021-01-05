# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from datetime import time

from crawlers.ezadmin import Ezadmin
from secrets import ANUA_EZADMIN_PW, ANUA_EZADMIN_ID, ANUA_EZADMIN_DOMAIN


def start():

    #ANUA
    Ezadmin.get_admin_page(ANUA_EZADMIN_DOMAIN, ANUA_EZADMIN_ID, ANUA_EZADMIN_PW)


if __name__ == '__main__':
    start()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
