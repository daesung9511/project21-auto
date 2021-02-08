# coding: utf-8

import csv
import time
import datetime

from powernad.Object.Campaign.CampaignObject import CampaignObject
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

from utils import Utils, DEFAULT_TIMEOUT_DELAY, RD_FILE

from openpyxl import load_workbook

from utils.naverShop import AsCampaign, AsStat


class Naver_shop:

    def get_n_days_past_data(self, timedelta_days, account):
        id = account["account_id"]
        license = account["license"]
        secret = account["secret"]

        campaign = AsCampaign("https://api.naver.com", license, secret, id)
        c_list: list[CampaignObject] = campaign.get_campaign_list_with_customer_id(customerId=1625878)
        c_ids = list(map(lambda x: x.nccCampaignId, c_list))

        stat = AsStat("https://api.naver.com", license, secret, id)
        start = datetime.datetime.now() - datetime.timedelta(days=timedelta_days)

        date_format = "%Y-%m-%d"

        start_date = start.strftime(date_format)

        end_date = (start - datetime.timedelta(days=1)).strftime(date_format)
        # fields = """[\"clkCnt\",\"impCnt\",\"salesAmt\",\"ctr\",\"cpc\",\"ccnt\",\"crto\",\"convAmt\",\"ror\",\"cpConv\",\"viewCnt\"]"""
        fields = """[\"salesAmt\"]"""
        range = """{\"since\":\"""" + end_date + """\",\"until\":\"""" + start_date + """\"}"""

        stats = stat.get_stat_by_ids(
            ids=c_ids,
            fields=fields,
            timeRange=range,
            timeIncrement="allDays"
        )
        sales_info_list = stats["data"]

        info = []
        for c in c_list:
            for x in sales_info_list:
                sales_info = dict(x)
                if sales_info["id"] == c.nccCampaignId:
                    result = dict({"id": sales_info["id"], "name": c.name, "cost": sales_info["salesAmt"]})
                    info.append(result)
                    break
        return info

    def get_data(self, account, days):
        for n in range(1, days + 1):
            info = self.get_n_days_past_data(n, account)
            print(info)

    def run(self, driver, account, days):
        # account list
        # lavena, yuge, anua, project21

        self.get_data(account, days)

        # file loading
        # self.update_ad_costs(account["id"])
