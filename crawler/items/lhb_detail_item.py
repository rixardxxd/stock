# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LhbDetailItem(scrapy.Item):
    # define the fields for your item here like:
    stock_id = scrapy.Field()
    # 营业部名称
    institution_name = scrapy.Field()
    # 买入金额
    buy_value = scrapy.Field()
    # 买入金额/总成交额
    buy_over_total_ratio = scrapy.Field()
    # 卖出金额
    sell_value = scrapy.Field()
    # 卖出金额/总成交额
    sell_over_total_ratio = scrapy.Field()
    # 净买入金额
    net_buy_value = scrapy.Field()
    # 交易详情
    trade_detail_url = scrapy.Field()
    # 上榜原因
    reason = scrapy.Field()
    # 收盘价
    close_price = scrapy.Field()
    # 涨跌幅
    change_percent = scrapy.Field()
    # 总成交量
    total_volume = scrapy.Field()
    # 总成交金额
    total_amount = scrapy.Field()
    # 爬取时间
    crawl_date = scrapy.Field()
