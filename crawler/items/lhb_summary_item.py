# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LhbSummaryItem(scrapy.Item):
    # define the fields for your item here like:
    stock_id = scrapy.Field()
    end_date = scrapy.Field()
    reason = scrapy.Field()
    change_percent = scrapy.Field()
    buy_value = scrapy.Field()
    sell_value = scrapy.Field()
    net_value = scrapy.Field()
