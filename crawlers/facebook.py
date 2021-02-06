from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adsinsights import AdsInsights
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adaccountuser import AdAccountUser

from openpyxl import load_workbook
from datetime import datetime

from utils import Utils, AD_FEE_FILE

class Facebook:
    def update_ad_fee_data(self, account):
   
        FacebookAdsApi.init(account["id"], account["secret"], account["access_token"])

        me = AdAccountUser('me')
        
        ad_accounts = me.get_ad_accounts()
        
        sales_wb = load_workbook(AD_FEE_FILE, data_only=True, read_only=False)

        ad_fee_ws = Utils.create_xl_sheet(sales_wb, "-광고비")
        # 시트 헤더 고정
        ad_fee_headings = ['','일자', '요일', '미디어', '상품1', '광고비(VAT미포함)']
        for idx, header in enumerate(ad_fee_headings):
            ad_fee_ws.cell(row=1, column=idx + 1).value = header
        ad_fee_ws.freeze_panes = 'A2'
        for ad_account in ad_accounts:
            campaigns = AdAccount(ad_account["id"]).get_campaigns(
                fields=[
                        'id',
                        'name'
                    ]   ,
                params={
                        'effective_status': ['ACTIVE'],
                    },
                )
            for campaign in campaigns:
                insights = Campaign(campaign["id"]).get_insights(
                    params={
                        'date_preset': Campaign.DatePreset.yesterday,
                    }
                )
                
                if not len(insights) == 0:
                    insight = insights[0] 
                    fee_max_row = str(ad_fee_ws.max_row+1)
                    ad_fee_ws.cell(row=int(fee_max_row),column=1).value = campaign["name"]
                    ad_fee_ws.cell(row=int(fee_max_row),column=2).value = datetime.today().strftime("%Y-%m-%d")
                    ad_fee_ws.cell(row=int(fee_max_row),column=4).value = '페이스북'
                    ad_fee_ws.cell(row=int(fee_max_row),column=6).value = insight["spend"]

        sales_wb.save(AD_FEE_FILE)
        
    def run(self, driver, account):
        print(account)
        self.update_ad_fee_data(account)

