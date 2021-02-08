import ast
from pprint import pprint

from powernad.API.AdGroup import AdGroup
from powernad.API.Campaign import Campaign, CampaignList
from powernad.API.Stat import Stat
from powernad.Object.Campaign.CampaignObject import CampaignObject
from powernad.Object.AdGroup.AdgroupObject import AdgroupObject
from selenium import webdriver
from datetime import datetime, timedelta

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from crawlers.naver_shop import Naver_shop
from utils import Utils
from utils.naverShop import AsCampaign, AsStat

# if __name__ == '__main__':
    # print(Naver_shop.calc_date())
