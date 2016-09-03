
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LhbDetailDfcfItem(scrapy.Item):
    # 上榜日期
    lhb_date = scrapy.Field()
    # 股票编号
    stock_id = scrapy.Field()
    # 股票名称
    stock_name = scrapy.Field()
    # 上榜原因
    reason = scrapy.Field()
    # 营业部名称
    yyb_name = scrapy.Field()
    # 龙虎榜买卖席位（买：0，卖：1）
    buy_or_sell = scrapy.Field()
    # 龙虎榜买卖名次（1~5，序号越低，买入/卖出金额越大）
    buy_or_sell_order = scrapy.Field()
    # 营业部买入金额
    buy_value = scrapy.Field()
    # 买入金额占总成交额比例
    buy_value_percent = scrapy.Field()
    # 营业部卖出金额
    sell_value = scrapy.Field()
    # 卖出今日占总成交额比例
    sell_value_percent = scrapy.Field()
    # 营业部买入净额
    net_value = scrapy.Field()



