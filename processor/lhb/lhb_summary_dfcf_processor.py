# -*- coding: utf-8 -*-
"""A script to process items from a redis queue and store them into MySQL."""

from __future__ import print_function, unicode_literals

import logging
import time

from processor.lhb.lhb_db_operation import LhbDB
from processor.processor import Processor
from utils.time_util import get_current_timestamp


class LhbSummaryDfcfProcessor(Processor):
    def __init__(self):
        super().__init__()
        self.parse_config()
        logging.basicConfig(format='%(asctime)s %(message)s')
        self.logger = logging.getLogger('lhb_summary_dfcf_processor')

    def parse_config(self):
        """
        This method parses config from env.cfg
        Returns
        -------
        None
        """
        super().parse_config()
        self.redis_key = self.config_parser.get("lhb", "LHB_SUMMARY_DFCF_REDIS_KEY")
        self.mysql_database = self.config_parser.get("lhb", "MYSQL_DATABASE")

    def insert_lhb_summary_table(self, items):
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
            row = (item['lhb_date'],
                   item['stock_id'],
                   item['stock_name'],
                   item['close_price'],
                   item['change_percent'],
                   item['lhb_net_value'],
                   item['lhb_buy_value'],
                   item['lhb_sell_value'],
                   item['lhb_total_value'],
                   item['trade_amount'],
                   item['net_value_percent'],
                   item['total_value_percent'],
                   item['turnover_ratio'],
                   item['market_value'],
                   item['reason'].encode('utf-8'),
                   get_current_timestamp("Asia/Shanghai"))
            self.database_instance.insert_summary_info_dfcf(row)

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
            self.insert_lhb_summary_table(items)
            processed_item_number += len(items)

        self.database_instance.close_db()
        self.session.close()

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
    lhb_processor = LhbSummaryDfcfProcessor()
    lhb_processor.run()
