from crawlers.ezadmin import Ezadmin
from secrets import ANUA_EZADMIN_PW, ANUA_EZADMIN_ID, ANUA_EZADMIN_DOMAIN


def start():

    #ANUA
    Ezadmin.get_admin_page(ANUA_EZADMIN_DOMAIN, ANUA_EZADMIN_ID, ANUA_EZADMIN_PW)

if __name__ == '__main__':
    start()
    # git test
