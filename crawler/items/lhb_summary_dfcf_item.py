
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LhbSummaryDfcfItem(scrapy.Item):
    # define the fields for your item here like:
    lhb_date = scrapy.Field()
    stock_id = scrapy.Field()
    stock_name = scrapy.Field()
    close_price = scrapy.Field()
    change_percent = scrapy.Field()
    lhb_net_value = scrapy.Field()
    lhb_buy_value = scrapy.Field()
    lhb_sell_value = scrapy.Field()
    lhb_total_value = scrapy.Field()
    trade_amount = scrapy.Field()
    net_value_percent = scrapy.Field()       # (lhb_net_value / trade_amount) * 100%
    total_value_percent = scrapy.Field()     # (lhb_total_value / trade_amount) * 100%
    turnover_ratio = scrapy.Field()
    market_value = scrapy.Field()
    reason = scrapy.Field()


