import json
import logging
import re
import datetime
from scrapy import Spider, Request

from crawler.items.lhb_detail_dfcf_item import LhbDetailDfcfItem

logger = logging.getLogger("LhbDetailDfcfSpider")


class LhbDetailDfcfSpider(Spider):
    """
    It's the class to crawl cinema info from mtime.com
    """
    name = "lhb_detail_dfcf"
    custom_settings = {
        'ITEM_PIPELINES': {
            'my_scrapy_redis.pipelines.RedisPipeline': 400
        }
    }
    # start_urls = start_urls
    # start_urls = [
    #     'http://data.eastmoney.com/DataCenter_V3/stock2016/TradeDetail/pagesize=200,page=1,sortRule=-1,sortType=,startDate=2015-07-06,endDate=2015-07-06,gpfw=0,js=var%20data_tab_1.html?rt=24545276',
    # ]

    def __init__(self, start_date=None, end_date=None, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # 若输入参数均为None，则默认爬取当天
        # 若输入的参数仅设置了其中一个值，则爬取该值设定的日期
        # 若输入参数都设置了值，则爬取该区间范围的数据
        if start_date is None and end_date is None:
            today = datetime.date.today().strftime("%Y-%m-%d")
            start_date = today
            end_date = today
        elif start_date is None:
            start_date = end_date
        elif end_date is None:
            end_date = start_date

        #  格式化输入参数
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

        # 爬取参数设定的区间范围的数据
        self.start_urls = []
        url_format = 'http://data.eastmoney.com/DataCenter_V3/stock2016/TradeDetail/pagesize=200,page=1,sortRule=-1,sortType=,' \
                     'startDate={0},endDate={0},gpfw=0,js=var%20data_tab_1.html?rt=24545276'
        target_date = start_date
        while target_date <= end_date:
            self.start_urls.append(url_format.format(target_date.strftime('%Y-%m-%d')))
            target_date = target_date + datetime.timedelta(1)

    def parse(self, response):
        """
        It's the method to pass the lhb info from response object
        Parameters
        ----------
        response

        Returns
        -------

        """
        # get response body
        content_str = response.body_as_unicode()
        # remove the unwanted string in the beginning of the file
        content_str = content_str.split("var data_tab_1=", 1)[1]
        try:
            content = json.loads(content_str)
        except json.decoder.JSONDecodeError as err:
            logger.exception(err)
            return

        # 东方财富接口每次索引最多获取200条记录，如有分页，则生成新的请求URL
        lhb_date = re.search(r'endDate=(\d{4}-\d{2}-\d{2})', response.url).group(1)
        page_index = re.search(r'page=(\d+)', response.url).group(1)
        if content['pages'] > 1 and page_index == '1':
            logger.error('{0}记录数超过1页：{1}'.format(lhb_date, content['pages']))
            page_index = int(page_index) + 1
            while page_index <= content['pages']:
                next_page = "page=" + str(page_index)
                next_page_url = re.sub(r'page=\d+', next_page, response.url)
                page_index += 1
                yield Request(next_page_url, callback=self.parse)

        # 获取当前日期的上榜个股，由于个股当天可能由于不同原因存在多条上榜记录
        # 而每条上榜记录都导向同一个展示页面，所以这里要根据【stock_id，lhb_date】去重
        new_url_set = set()
        detail_url_format = 'http://data.eastmoney.com/stock/lhb,{0},{1}.html'
        for item in content['data']:
            lhb_date = item['Tdate']
            stock_id = item['SCode']
            # 非A股标的，则直接跳过
            if stock_id[0] not in ['0', '3', '6']:
                continue
            # 如果龙虎榜买入金额和卖出金额都为空，则数据无效，直接抛弃
            if item['Bmoney'] == '' and item['Smoney'] == '':
                continue
            # 满足校验则生成新的url，插入集合中
            url = detail_url_format.format(lhb_date, stock_id)
            new_url_set.add(url)

        # 遍历集合每个URL，生成后续访问链接
        for url in new_url_set:
            yield Request(url, callback=self.parse_detail)

    def parse_detail(self, response):
        """
        It's the method to parse the detail lhb info

        Parameters
        ----------
        response

        Returns
        -------

        """
        # 获取日期与股票编号
        group = re.search(r'lhb,(\d{4}-\d{2}-\d{2}),(\d+).html', response.url)
        lhb_date = group.group(1)
        stock_id = group.group(2)

        logger.warn('处理{0}日{1}明细：'.format(lhb_date, stock_id))

        # 获取股票名称
        stock_name = response.xpath("//a[@style='cursor:pointer;']/text()").extract()[0].split(u'(')[0]

        # 上榜原因集合
        div_reason = response.xpath("//div[@class='left con-br']/text()").extract()

        # 买入前5集合，每个元素代表由于特定原因而上榜的买入席位集合
        table_buy = response.xpath("//table[@class='default_tab stock-detail-tab']")

        # 卖出前5集合，每个元素代表由于特定原因而上榜的卖出席位集合
        table_sell = response.xpath("//table[@class='default_tab tab-2']")

        # 按当天上榜次数进行遍历
        index = 0
        while index < len(div_reason):

            # 上榜原因
            reason = div_reason[index].split(u'类型：')[1]

            # 上榜买方席位处理
            buy_list = table_buy[index].xpath(".//tbody/tr")
            for tr in buy_list:
                lhb_detail_item = LhbDetailDfcfItem()
                lhb_detail_item['lhb_date'] = lhb_date
                lhb_detail_item['stock_id'] = stock_id
                lhb_detail_item['stock_name'] = stock_name
                lhb_detail_item['reason'] = reason
                lhb_detail_item['buy_or_sell'] = '0'
                lhb_detail_item['buy_or_sell_order'] = tr.xpath(".//td[1]/text()").extract()[0]
                lhb_detail_item['yyb_name'] = tr.xpath(".//td[2]/div/a/text()").extract()[0]
                lhb_detail_item['buy_value'] = tr.xpath(".//td[3]/text()").extract()[0]
                lhb_detail_item['buy_value_percent'] = tr.xpath(".//td[4]/text()").extract()[0].replace('%', '')
                lhb_detail_item['sell_value'] = tr.xpath(".//td[5]/text()").extract()[0]
                lhb_detail_item['sell_value_percent'] = tr.xpath(".//td[6]/text()").extract()[0].replace('%', '')
                lhb_detail_item['net_value'] = tr.xpath(".//td[7]/text()").extract()[0]
                yield lhb_detail_item

            # 上榜卖方席位处理
            # 注意卖方表格中有一个汇总统计，所以这里抛弃最后一条数据
            sell_list = table_sell[index].xpath(".//tbody/tr")
            sell_list_len = len(sell_list)
            sell_list = sell_list[0:sell_list_len-1]
            for tr in sell_list:
                lhb_detail_item = LhbDetailDfcfItem()
                lhb_detail_item['lhb_date'] = lhb_date
                lhb_detail_item['stock_id'] = stock_id
                lhb_detail_item['stock_name'] = stock_name
                lhb_detail_item['reason'] = reason
                lhb_detail_item['buy_or_sell'] = '1'
                lhb_detail_item['buy_or_sell_order'] = tr.xpath(".//td[1]/text()").extract()[0]
                lhb_detail_item['yyb_name'] = tr.xpath(".//td[2]/div/a/text()").extract()[0]
                lhb_detail_item['buy_value'] = tr.xpath(".//td[3]/text()").extract()[0]
                lhb_detail_item['buy_value_percent'] = tr.xpath(".//td[4]/text()").extract()[0].replace('%', '')
                lhb_detail_item['sell_value'] = tr.xpath(".//td[5]/text()").extract()[0]
                lhb_detail_item['sell_value_percent'] = tr.xpath(".//td[6]/text()").extract()[0].replace('%', '')
                lhb_detail_item['net_value'] = tr.xpath(".//td[7]/text()").extract()[0]
                yield lhb_detail_item

            # 指针自加1
            index += 1
