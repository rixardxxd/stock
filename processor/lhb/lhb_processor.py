# -*- coding: utf-8 -*-
"""A script to process items from a redis queue and store them into MySQL."""

from __future__ import print_function, unicode_literals

import logging
import time

from processor.lhb.lhb_db_operation import ImaxDB
from processor.processor import Processor
from utils.time_util import get_current_timestamp


class LhbProcessor(Processor):
    def __init__(self):
        super().__init__()
        self.parse_config()
        logging.basicConfig(format='%(asctime)s %(message)s')
        self.logger = logging.getLogger('lhb_processor')

    def parse_config(self):
        """
        This method parses config from env.cfg
        Returns
        -------
        None
        """
        super().parse_config()
        self.redis_key = self.config_parser.get("lhb", "CINEMA_INFO_REDIS_KEY")
        self.mysql_database = self.config_parser.get("lhb", "MYSQL_DATABASE")

    def insert_cinema_info_table(self, items):
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
            if not self.database_instance.is_cinema_existed(int(item['cinema_id'])):
                cinema_row = (int(item['cinema_id']),
                              item['sname'].encode('utf-8'),
                              item['cname'].encode('utf-8'),
                              item['address'].encode('utf-8'),
                              item['show_time_page'],
                              item['feature_imax'],
                              item['feature_3d'],
                              item['lowest_price'],
                              item['city'],
                              get_current_timestamp("Asia/Shanghai"))
                self.database_instance.insert_cinema(cinema_row)

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
            self.insert_cinema_info_table(items)
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
        self.database_instance = ImaxDB(self.mysql_args)
        self.database_instance.connect_db()


if __name__ == '__main__':
    imax_processor = LhbProcessor()
    imax_processor.run()
