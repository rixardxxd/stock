import json
import logging
import re

from scrapy import Spider

from crawler.items.lhb_summary_item import LhbSummaryItem
from utils.url_util import start_urls

logger = logging.getLogger("LhbDetailSpider")


class LhbDetailSpider(Spider):
    """
    It's the class to crawl lhb detail info from jrj.com
    Examples http://stock.jrj.com.cn/share,000002,lhb2016-08-16.shtml
    """
    name = "lhb_detail"
    custom_settings = {
        'ITEM_PIPELINES': {
            'my_scrapy_redis.pipelines.RedisPipeline': 400
        }
    }
    # start_urls = start_urls
    start_urls = [
        'http://stock.jrj.com.cn/share,000002,lhb2016-08-16.shtml'
    ]

    def parse(self, response):
        """
        It's the method to pass the lhb detail info from response object
        Parameters
        ----------
        response

        Returns
        -------

        """
        summary_tables = response.css('.tithd-s1.mt')
        summary_table_list = []
        for summary_table in summary_tables:
            text = summary_table.css('i').xpath('text()').extract()
            summary_table_list.append(list(map(lambda x: re.sub('[^0-9\.]+', '', x), text)))

        detail_tables = response.css('.table-s1.mt')
        detail_table_lists = []
        for detail_table in detail_tables:
            trs = detail_tables.css('tr')
            for tr in trs[2:6]:
                td_list = tr.css('td').xpath('text()').extract()
                trade_detail_url = tr.css('td.last').css('a::attr(href)').extract()
                print(list(map(lambda x:x.encode('utf8'), td_list)))
                print(trade_detail_url)




