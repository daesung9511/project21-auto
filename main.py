from crawlers.cafe24 import Cafe24
from crawlers.ezadmin import Ezadmin
from secrets import ANUA_EZADMIN_PW, ANUA_EZADMIN_ID, ANUA_EZADMIN_DOMAIN, PROJECT21_EZADMIN_DOMAIN, \
    PROJECT21_EZADMIN_PW, PROJECT21_EZADMIN_ID, PROJECT21_CAFE24_ID, PROJECT21_CAFE24_PW


def start():
    # ANUA
    # Ezadmin.download_yesterday_revenue(ANUA_EZADMIN_DOMAIN, ANUA_EZADMIN_ID, ANUA_EZADMIN_PW)

    # PROJECT21
    # Ezadmin.download_yesterday_revenue(PROJECT21_EZADMIN_DOMAIN, PROJECT21_EZADMIN_ID, PROJECT21_EZADMIN_PW)
    Cafe24.download_lacto_revenue(PROJECT21_CAFE24_ID, PROJECT21_CAFE24_PW)


if __name__ == '__main__':
    start()
    # git test
