import json
import logging
import re

from scrapy import Spider

from crawler.items.lhb_item import LhbItem
from utils.url_util import start_urls

logger = logging.getLogger("LhbSpider")


class LhbSpider(Spider):
    """
    It's the class to crawl cinema info from mtime.com
    """
    name = "lhb"
    custom_settings = {
        'ITEM_PIPELINES': {
            'my_scrapy_redis.pipelines.RedisPipeline': 400
        }
    }
    start_urls = start_urls
    #start_urls = [
    #    'http://stock.jrj.com.cn/action/lhb/getStockListDetail.jspa?vname=stockListDetail&stockcode=300033&infoClsType=0&page=1&size=100&order=desc&sort=endDate',
    #]

    def parse(self, response):
        """
        It's the method to pass the lhb info from response object
        Parameters
        ----------
        response

        Returns
        -------

        """
        stock_id = re.search(r'stockcode=(\d+)&', response.url).group(1)
        print(stock_id)
        content_str = response.body_as_unicode()
        # remove the unwanted string in the beginning of the file
        content_str = content_str.split("var stockListDetail=", 1)[1]
        # remove the ";" char in the end of the file
        content_str = content_str.replace(";", "")
        try:
            content = json.loads(content_str)
        except json.decoder.JSONDecodeError as err:
            logger.exception(err)
            return
        print(content)
        for item in content['data']:
            lhb_item = LhbItem()
            lhb_item['stock_id'] = stock_id
            lhb_item['end_date'] = item[0]
            lhb_item['reason'] = item[1]
            lhb_item['change_percent'] = item[2]
            lhb_item['buy_value'] = item[3]
            lhb_item['sell_value'] = item[4]
            lhb_item['net_value'] = item[5]
            yield lhb_item