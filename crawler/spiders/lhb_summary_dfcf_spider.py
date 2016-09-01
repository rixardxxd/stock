import json
import logging
import re

from scrapy import Spider

from crawler.items.lhb_summary_dfcf_item import LhbSummaryDfcfItem
from utils.url_dfcf_util import start_urls

logger = logging.getLogger("LhbSummaryDfcfSpider")


class LhbSummaryDfcfSpider(Spider):
    """
    It's the class to crawl cinema info from mtime.com
    """
    name = "lhb_summary_dfcf"
    custom_settings = {
        'ITEM_PIPELINES': {
            'my_scrapy_redis.pipelines.RedisPipeline': 400
        }
    }
    start_urls = start_urls
    # start_urls = [
    #    'http://data.eastmoney.com/DataCenter_V3/stock2016/TradeDetail/pagesize=200,page=1,sortRule=-1,sortType=,startDate=2016-08-31,endDate=2016-08-31,gpfw=0,js=var%20data_tab_1.html?rt=24545276',
    # ]

    def parse(self, response):
        """
        It's the method to pass the lhb info from response object
        Parameters
        ----------
        response

        Returns
        -------

        """
        # get lhb date
        lhb_date = re.search(r'endDate=(\d{4}-\d{2}-\d{2})', response.url).group(1)
        # get response body
        content_str = response.body_as_unicode()
        # remove the unwanted string in the beginning of the file
        content_str = content_str.split("var data_tab_1=", 1)[1]
        try:
            content = json.loads(content_str)
        except json.decoder.JSONDecodeError as err:
            logger.exception(err)
            return

        print(lhb_date)

        if content['pages'] > 1:
            print('当前日期记录数超过1页：{0}'.format(lhb_date))

        for item in content['data']:
            lhb_item = LhbSummaryDfcfItem()
            lhb_item['lhb_date'] = item['Tdate']
            lhb_item['stock_id'] = item['SCode']
            lhb_item['stock_name'] = item['SName']
            lhb_item['close_price'] = item['ClosePrice']
            lhb_item['change_percent'] = item['Chgradio']
            lhb_item['lhb_net_value'] = item['JmMoney']
            lhb_item['lhb_buy_value'] = item['Bmoney']
            lhb_item['lhb_sell_value'] = item['Smoney']
            lhb_item['lhb_total_value'] = item['ZeMoney']
            lhb_item['trade_amount'] = item['Turnover']
            lhb_item['net_value_percent'] = item['JmRate']
            lhb_item['total_value_percent'] = item['ZeRate']
            lhb_item['turnover_ratio'] = item['Dchratio']
            lhb_item['market_value'] = item['Ltsz']
            lhb_item['reason'] = item['Ctypedes']
            yield lhb_item