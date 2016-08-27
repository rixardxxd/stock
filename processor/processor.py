# -*- coding: utf-8 -*-

"""
This module is the base class of processor.
It parses arguments from command line,
sets up Redis and MySQL.
"""

from __future__ import print_function, unicode_literals

import json
import logging
import os
import time
from json.decoder import JSONDecodeError

from config.config_parser_util import ConfigParserUtil
from my_scrapy_redis.connection import get_redis
from utils import get_requests_session


class Processor(object):
    """
    This class is the base class of processor.
    """

    def __init__(self, batch_item_count=1000,
                 timeout=5, limit=0, log_every=1000, sleep_secs=0.01, verbose=False):
        """

        Parameters
        ----------
        batch_item_count: maximal items to retrieve from Redis every time
        timeout: The maximum number of seconds to block Redis
        limit: Item amount to be processed.
        log_every: Write log after processing a batch of log_every items
        sleep_secs: Seconds to suspend
        verbose: Verbose level
        """
        self.config_parser = ConfigParserUtil.get_config_parser("config/env.cfg")
        self.redis_key = None
        self.mysql_database = None
        self.redis_host = None
        self.mysql_host = None
        self.mysql_user = None
        self.mysql_password = None
        self.batch_item_count = batch_item_count
        self.timeout = timeout
        self.limit = limit
        if self.limit == 0:
            self.limit = float('inf')
        self.log_every = log_every
        self.sleep_secs = sleep_secs
        self.verbose = verbose
        self.redis_instance = None
        self.mysql_args = None
        self.database_instance = None
        self.logger = None
        self.session = get_requests_session()
        self.comment_session = get_requests_session()

    def parse_config(self):
        """
        This method parses arguments from command line.
        Returns
        -------
        None
        """
        env = os.environ.get("ENV")  # ENV equals section name in env.cfg
        self.redis_host = self.config_parser.get(env, "REDIS_HOST")
        self.mysql_host = self.config_parser.get(env, "MYSQL_HOST")
        self.mysql_user = self.config_parser.get(env, "MYSQL_USER")
        self.mysql_password = self.config_parser.get(env, "MYSQL_PASSWORD")

    def setup_redis(self):
        """
        This method sets up Redis instance.
        Returns
        -------
        None
        """
        params = {"host": self.redis_host if self.redis_host else "", "port": 6379}
        logging.basicConfig(level=logging.DEBUG if self.verbose else logging.INFO)
        self.redis_instance = get_redis(**params)

    def setup_mysql(self):
        """
        This method sets up MySQL database connection instance.
        Returns
        -------
        None
        """
        self.mysql_args = {"host": self.mysql_host, "database": self.mysql_database, 'user': self.mysql_user,
                           "password": self.mysql_password}

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
            self.insert_product_info_table(items)
            self.insert_sales_info_table(items)
            processed_item_number += len(items)

        self.database_instance.close_db()
        self.session.close()

    def get_batch_items(self):
        """
        This method gets a list of items from Redis, whose number equals to batch_item_count.
        Parameters
        ----------
        Returns
        -------
        items: a list of items in JSON format
        """
        pipeline = self.redis_instance.pipeline()
        for _ in range(self.batch_item_count):
            # blpop: queue, FIFO
            # brpop: stack, LIFO
            pipeline.blpop(self.redis_key, self.timeout)
        result = filter(lambda x: x, pipeline.execute())  # execute a few commands, and filter out None values
        data = map(lambda x: x[1].decode("utf-8"), result)  # retrieve data from tuple
        items = []
        for datum in data:
            try:
                items.append(json.loads(datum))
            except TypeError as te:
                self.logger.exception("Type Error. Exception: {0}".format(te))
            except JSONDecodeError as jde:
                self.logger.exception("JSON decoder error. Exception: {0}".format(jde))
        return items

    def insert_product_info_table(self, items):
        """
        This method inserts into table product_info. Override required.
        Parameters
        ----------
        items: a list of items to insert

        Returns
        -------
        None
        """
        pass

    def insert_sales_info_table(self, items):
        """
        This method inserts into table sales_info. Override required.
        Parameters
        ----------
        items: a list of items to insert

        Returns
        -------
        None
        """
        pass

    def run_processor(self):
        """
        This method runs jd or jumei processor.
        Returns
        -------
        Exit code
        """
        try:
            self.process_items()
            return 0
        except KeyboardInterrupt as ki:
            self.logger.exception("Keyboard exception. Exception: {0}".format(ki))
            return 0
        except Exception as e:
            self.logger.exception("Unhandled exception. Exception: {0}".format(e))
            return 2

    def run(self):
        """
        Run methods.
        Returns
        -------
        None
        """
        self.setup_redis()
        self.setup_mysql()
        self.run_processor()
