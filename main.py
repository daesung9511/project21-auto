from crawlers.cafe24 import Cafe24
from crawlers.ezadmin import Ezadmin
from crawlers.naver_shop import Naver_shop
from secrets import ANUA_EZADMIN_PW, ANUA_EZADMIN_ID, ANUA_EZADMIN_DOMAIN, PROJECT21_EZADMIN_DOMAIN, \
    PROJECT21_EZADMIN_PW, PROJECT21_EZADMIN_ID, PROJECT21_CAFE24_ID, PROJECT21_CAFE24_PW, \
    PROJECT21_EZADMIN_PW, PROJECT21_EZADMIN_ID, \
    PROJECT21_NAVERSHOP_ID, PROJECT21_NAVERSHOP_PW, PROJECT21_NAVERSHOP_TYPE, \
    ANUA_NAVERSHOP_ID, ANUA_NAVERSHOP_PW, ANUA_NAVERSHOP_TYPE, \
    LAVENA_NAVERSHOP_ID, LAVENA_NAVERSHOP_PW, LAVENA_NAVERSHOP_TYPE, \
    YUGE_NAVERSHOP_ID, YUGE_NAVERSHOP_PW, YUGE_NAVERSHOP_TYPE


def start():
    # ANUA
    # Ezadmin.download_yesterday_revenue(ANUA_EZADMIN_DOMAIN, ANUA_EZADMIN_ID, ANUA_EZADMIN_PW)

    # PROJECT21
    # Ezadmin.download_yesterday_revenue(PROJECT21_EZADMIN_DOMAIN, PROJECT21_EZADMIN_ID, PROJECT21_EZADMIN_PW)
    # Cafe24.download_lacto_revenue(PROJECT21_CAFE24_ID, PROJECT21_CAFE24_PW)

    # naver_shop
    naver_shop = Naver_shop()

    # LAVENA[naver_shop]
    naver_shop.run(LAVENA_NAVERSHOP_ID, LAVENA_NAVERSHOP_PW, LAVENA_NAVERSHOP_TYPE)

    # ANUA[naver_shop]
    # naver_shop.run(ANUA_NAVERSHOP_ID, ANUA_NAVERSHOP_PW, ANUA_NAVERSHOP_TYPE)

    # # YUGE[naver_shop]
    # naver_shop.run(YUGE_NAVERSHOP_ID, YUGE_NAVERSHOP_PW, YUGE_NAVERSHOP_TYPE)

    # # PROJECT21[naver_shop]
    # naver_shop.run(PROJECT21_NAVERSHOP_ID, PROJECT21_NAVERSHOP_PW, PROJECT21_NAVERSHOP_TYPE)


if __name__ == '__main__':
    start()
    # git test
