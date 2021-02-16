import json
from typing import List

from powernad.API.Campaign import Campaign, CampaignList
from powernad.API.Stat import Stat
from powernad.Object.Campaign.CampaignObject import CampaignObject
from powernad.Object.Stat.StatObject import StatObject
from powernad.Object.AdGroup.AdgroupObject import AdgroupObject


class AsCampaign(Campaign):
    def get_campaign_list_with_customer_id(self, customerId: int) -> CampaignList:
        query = {'customerId': str(customerId)}

        result = self.r.get('/ncc/campaigns', query)

        camp_list = []
        for arr in result:
            camp = CampaignObject(arr)
            camp_list.append(camp)

        return camp_list

    def get_adgroup_list(self, customerId: int, campaignId: str) -> CampaignList:
        query = {'customerId': str(customerId),
                 'nccCampaignId': campaignId }
        result = self.r.get('/ncc/adgroups', query)

        adgroups = []
        for arr in result:
            adgroup = AdgroupObject(arr)
            adgroups.append(adgroup)

        return adgroups


class AsStat(Stat):
    def get_stat_by_ids(self, ids: List[str], fields: str, timeRange: str, datePreset: str = None,
                        timeIncrement: str = None,
                        breakdown: str = None):
        ids_string = ",".join(ids)
        query = {'fields': fields, 'timeIncrement': timeIncrement, 'timeRange': timeRange, 'ids': ids_string}
        result = self.r.get('/stats', query)
        return result
