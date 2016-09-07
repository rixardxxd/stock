# -*- coding: utf-8 -*-
"""A script to process items from a redis queue and store them into MySQL."""

from __future__ import print_function, unicode_literals

import decimal
import time

import mysql
from processor.lhb.lhb_db_operation import LhbDB
from processor.processor import Processor
from utils.logger_util import get_logger
from utils.time_util import get_current_timestamp


class LhbDfcfProcessor(Processor):
    def __init__(self):
        super().__init__()
        self.parse_config()
        self.logger = get_logger('lhb_dfcf_processor.log')

    def parse_config(self):
        """
        This method parses config from env.cfg
        Returns
        -------
        None
        """
        super().parse_config()
        self.redis_key = self.config_parser.get("lhb", "LHB_DFCF_REDIS_KEY")
        self.mysql_database = self.config_parser.get("lhb", "MYSQL_DATABASE")

    def insert_lhb_table(self, items):
        """
        This method inserts a list of items into table cinema_info
        Parameters
        ----------
        items: list of cinema items to insert

        Returns
        -------
        None
        """
        for item in items:
            detail_row = (item['lhb_date'],
                          item['stock_id'],
                          item['stock_name'],
                          item['reason'].encode('utf-8'),
                          item['yyb_name'].encode('utf-8'),
                          item['buy_or_sell'],
                          item['buy_or_sell_order'],
                          item['buy_value'] if item['buy_value'] != '-' else 0,
                          item['buy_value_percent'] if item['buy_value_percent'] != '-' else 0,
                          item['sell_value'] if item['sell_value'] != '-' else 0,
                          item['sell_value_percent'] if item['sell_value_percent'] != '-' else 0,
                          item['net_value'],
                          get_current_timestamp("Asia/Shanghai"))
            summary_item = item['summary_item']
            summary_row = (summary_item['lhb_date'],
                           summary_item['stock_id'],
                           summary_item['stock_name'],
                           summary_item['close_price'] if summary_item['close_price'] != '' else -1,
                           decimal.Decimal("%.2f" % float(summary_item['change_percent'])) if summary_item[
                                                                                                  'change_percent'] != '' else -10000,
                           summary_item['lhb_net_value'] if summary_item['lhb_net_value'] != '' else 0,
                           summary_item['lhb_buy_value'] if summary_item['lhb_buy_value'] != '' else 0,
                           summary_item['lhb_sell_value'] if summary_item['lhb_sell_value'] != '' else 0,
                           summary_item['lhb_total_value'] if summary_item['lhb_total_value'] != '' else 0,
                           summary_item['trade_amount'] if summary_item['trade_amount'] != '' else -1,
                           decimal.Decimal("%.2f" % float(summary_item['net_value_percent'])) if summary_item[
                                                                                                     'net_value_percent'] != '' else -1,
                           decimal.Decimal("%.2f" % float(summary_item['total_value_percent'])) if summary_item[
                                                                                                       'total_value_percent'] != '' else -1,
                           decimal.Decimal("%.2f" % float(summary_item['turnover_ratio'])) if summary_item[
                                                                                                  'turnover_ratio'] != '' else -1,
                           summary_item['reason'].encode('utf-8'),
                           get_current_timestamp("Asia/Shanghai"))

            try:
                self.database_instance.insert_detail_info_dfcf(detail_row)
                self.database_instance.insert_summary_info_dfcf(summary_row)
            except mysql.connector.errors.IntegrityError as e:
                self.logger.info(item)
                self.logger.error(e)

    def process_items(self):

        """
        Process items from a redis queue.
        """
        processed_item_number = 0

        while processed_item_number < self.limit:
            items = self.get_batch_items()
            if len(items) == 0:
                time.sleep(self.sleep_secs)
                continue
            self.insert_lhb_table(items)
            processed_item_number += len(items)

        self.database_instance.close_db()
        self.session.close()
        self.database_instance = None

    def setup_mysql(self):

        """
        This method sets up MySQL database connection instance.
        Returns
        -------
        None
        """

        super().setup_mysql()
        self.database_instance = LhbDB(self.mysql_args)
        self.database_instance.connect_db()

if __name__ == '__main__':
    lhb_processor = LhbDfcfProcessor()
    lhb_processor.run()
