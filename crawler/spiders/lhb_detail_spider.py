import logging
import re

from scrapy import Spider

from crawler.items.lhb_detail_item import LhbDetailItem
from utils.url_util import start_urls
from utils.time_util import get_current_timestamp
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
        stock_id = re.search(r'stockcode=(\d+)&', response.url).group(1)
        summary_tables = response.css('.tithd-s1.mt')
        summary_table_list = []
        reason_list = []
        for summary_table in summary_tables:
            # 抓上榜原因
            reason = summary_table.css('p')[0].xpath('text()').extract_first()
            reason_list.append(reason)
            # 上榜原因下面的总成交数据
            text = summary_table.css('i').xpath('text()').extract()
            summary_table_list.append(list(map(lambda x: re.sub('[^0-9\.]+', '', x), text)))

        detail_tables = response.css('.table-s1.mt')
        print(len(detail_tables))
        detail_table_lists = []
        i = 0
        for detail_table in detail_tables:
            trs = detail_tables.css('tr')
            detail_tables_list = []
            for tr in trs[2:7]:
                item = LhbDetailItem()
                td_list = tr.css('td').xpath('text()').extract()
                # institution name
                institution_name = tr.css('td.tl').css('a').xpath('text()').extract()
                item['institution_name'] = institution_name
                # trade detail url
                trade_detail_url = tr.css('td.last').css('a::attr(href)').extract()
                item['trade_detail_url'] = trade_detail_url
                row_list = list(map(lambda x: x.encode('utf8'), td_list))[3:8]
                numbers_list = list(map(lambda x: re.sub('[^0-9\.\-]+', '', x.decode('utf8')), row_list))
                # 买入金额
                item['buy_value'] = numbers_list[0]
                # 买入金额/总成交额
                item['buy_over_total_ratio'] = numbers_list[1]
                # 卖出金额
                item['sell_value'] = numbers_list[2]
                # 卖出金额/总成交额
                item['sell_over_total_ratio'] = numbers_list[3]
                # 净买入金额
                item['net_buy_value'] = numbers_list[4]
                #上榜原因
                item['reason'] = reason_list[i]
                # 收盘价
                item['close_price'] = summary_table_list[i][0]
                # 涨跌幅
                item['change_percent'] = summary_table_list[i][1]
                # 总成交量
                item['total_volume'] = summary_table_list[i][2]
                # 总成交金额
                item['total_amount'] = summary_table_list[i][3]
                # 爬取时间
                item['crawl_date'] = get_current_timestamp("Asia/Shanghai")
                yield item
            i += 1
