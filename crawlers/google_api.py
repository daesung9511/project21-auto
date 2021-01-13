#coding: utf-8

import time
import io
from googleads import adwords

class Google:

    def run(self):
        # Define output as a string
        output = io.StringIO()

        # Initialize appropriate service.
        adwords_client = adwords.AdWordsClient.LoadFromStorage()

        report_downloader = adwords_client.GetReportDownloader(version='v201809')

        # Create report query.
        report_query = ('''
        select Date, HourOfDay, Clicks
        from ACCOUNT_PERFORMANCE_REPORT
        during LAST_7_DAYS''')

        # Write query result to output file
        report_downloader.DownloadReportWithAwql(
            report_query, 
            'CSV',
            output,
            client_customer_id='636-545-6711', # denotes which adw account to pull from
            skip_report_header=True, 
            skip_column_header=False,
            skip_report_summary=True, 
            include_zero_impressions=False)

        output.seek(0)
        print(output[:100])