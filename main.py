from crawlers.cafe24 import Cafe24
from crawlers.ezadmin import Ezadmin
from crawlers.naver_shop import Naver_shop
from crawlers.naver_gfa import Naver_GFA
from crawlers.kakaomoment import Kakaomoment
from crawlers.facebook import Facebook
from utils import Utils
from secrets import ANUA_EZADMIN_PW, ANUA_EZADMIN_ID, ANUA_EZADMIN_DOMAIN, PROJECT21_EZADMIN_DOMAIN, \
    PROJECT21_EZADMIN_PW, PROJECT21_EZADMIN_ID, PROJECT21_CAFE24_ID, PROJECT21_CAFE24_PW, \
    PROJECT21_EZADMIN_PW, PROJECT21_EZADMIN_ID, \
    PROJECT21_NAVERSHOP_ID, PROJECT21_NAVERSHOP_PW, PROJECT21_NAVERSHOP_TYPE, \
    ANUA_NAVERSHOP_ID, ANUA_NAVERSHOP_PW, ANUA_NAVERSHOP_TYPE, \
    LAVENA_NAVERSHOP_ID, LAVENA_NAVERSHOP_PW, LAVENA_NAVERSHOP_TYPE, \
    YUGE_NAVERSHOP_ID, YUGE_NAVERSHOP_PW, YUGE_NAVERSHOP_TYPE, \
    ANUA_NAVERGFA_ID, ANUA_NAVERGFA_PW, ANUA_NAVERGFA_DOMAIN, \
    LAVENA_NAVERGFA_ID, LAVENA_NAVERGFA_PW, LAVENA_NAVERGFA_DOMAIN, \
    YUGE_NAVERGFA_ID, YUGE_NAVERGFA_PW, YUGE_NAVERGFA_DOMAIN, \
    ANUA_KAKAOMOMENT_ID, ANUA_KAKAOMOMENT_PW, ANUA_KAKAOMOMENT_DOMAIN, ANUA_KAKAOMOMENT_NUMBER, \
    YUGE_KAKAOMOMENT_ID, YUGE_KAKAOMOMENT_PW, YUGE_KAKAOMOMENT_DOMAIN, YUGE_KAKAOMOMENT_NUMBER, \
    PROJECT21_FACEBOOK_ID, PROJECT21_FACEBOOK_PW, PROJECT21_FACEBOOK_NUMBER, \
    ANUA_FACEBOOK_ID, ANUA_FACEBOOK_PW, ANUA_FACEBOOK_NUMBER, \
    YUGE_FACEBOOK_ID, YUGE_FACEBOOK_PW, YUGE_FACEBOOK_NUMBER, \
    LAVENA_FACEBOOK_ID, LAVENA_FACEBOOK_PW, LAVENA_FACEBOOK_NUMBER, \
    ANUA_GOOGLE_ID, ANUA_GOOGLE_PW, \
    ACCOUNTS
def run_ezadmin(account):
    for brand in account["index"]:
        uid = account[brand]["id"]
        upw = account[brand]["pw"]
        udomain = account[brand]["domain"]

        Ezadmin.download_yesterday_revenue(udomain, uid, upw)

def run_cafe24(account):
    for brand in account["index"]:
        uid = account[brand]["id"]
        upw = account[brand]["pw"]

        Cafe24.download_lacto_revenue(uid, upw)

def run(platform, account):
    driver = Utils.get_chrome_driver()
    driver.set_window_size(1980, 1080)

    for brand in account["index"]:
        platform.run(driver, account[brand])

    driver.quit()

def start():
    # run_ezadmin(ACCOUNTS["ezadmin"])
    # run_cafe24(ACCOUNTS["cafe24"])
    run(Naver_shop(), ACCOUNTS["naver_shop"])
    run(Naver_GFA(), ACCOUNTS["naver_gfa"])
    run(Kakaomoment(), ACCOUNTS["kakaomoment"])
    run(Facebook(), ACCOUNTS["facebook"])

    # Ezadmin
    # Ezadmin.download_yesterday_revenue(ANUA_EZADMIN_DOMAIN, ANUA_EZADMIN_ID, ANUA_EZADMIN_PW)
    # Ezadmin.download_yesterday_revenue(PROJECT21_EZADMIN_DOMAIN, PROJECT21_EZADMIN_ID, PROJECT21_EZADMIN_PW)

    # Cafe24
    # Cafe24.download_lacto_revenue(PROJECT21_CAFE24_ID, PROJECT21_CAFE24_PW)

    # naver_shop
    # naver_shop.run(LAVENA_NAVERSHOP_ID, LAVENA_NAVERSHOP_PW, LAVENA_NAVERSHOP_TYPE)
    # naver_shop.run(ANUA_NAVERSHOP_ID, ANUA_NAVERSHOP_PW, ANUA_NAVERSHOP_TYPE)
    # naver_shop.run(YUGE_NAVERSHOP_ID, YUGE_NAVERSHOP_PW, YUGE_NAVERSHOP_TYPE)
    # naver_shop.run(PROJECT21_NAVERSHOP_ID, PROJECT21_NAVERSHOP_PW, PROJECT21_NAVERSHOP_TYPE)    
    
    # naver_gfa
    # naver_gfa.run(LAVENA_NAVERGFA_ID, LAVENA_NAVERGFA_PW, LAVENA_NAVERGFA_DOMAIN)
    # naver_gfa.run(ANUA_NAVERGFA_ID, ANUA_NAVERGFA_PW, ANUA_NAVERGFA_DOMAIN)
    # naver_gfa.run(YUGE_NAVERGFA_ID, YUGE_NAVERGFA_PW, YUGE_NAVERGFA_DOMAIN)

    # kakaomoment
    # kakaomoment.run(ANUA_KAKAOMOMENT_ID, ANUA_KAKAOMOMENT_PW, ANUA_KAKAOMOMENT_DOMAIN, ANUA_KAKAOMOMENT_NUMBER)
    # kakaomoment.run(YUGE_KAKAOMOMENT_ID, YUGE_KAKAOMOMENT_PW, YUGE_KAKAOMOMENT_DOMAIN, YUGE_KAKAOMOMENT_NUMBER)    

    # facebook
    # facebook.run(LAVENA_FACEBOOK_ID, LAVENA_FACEBOOK_PW, LAVENA_FACEBOOK_NUMBER)
    # facebook.run(ANUA_FACEBOOK_ID, ANUA_FACEBOOK_PW, ANUA_FACEBOOK_NUMBER)
    # facebook.run(YUGE_FACEBOOK_ID, YUGE_FACEBOOK_PW, YUGE_FACEBOOK_NUMBER)
    # facebook.run(PROJECT21_FACEBOOK_ID, PROJECT21_FACEBOOK_PW, PROJECT21_FACEBOOK_NUMBER)

if __name__ == '__main__':
    start()
    # git test
