# -*- coding: utf-8 -*-
"""A script to process items from a redis queue and store them into MySQL."""

from __future__ import print_function, unicode_literals

import os

from config.config_parser_util import ConfigParserUtil
from processor.lhb.lhb_db_operation import LhbDB
from utils.logger_util import get_logger


class LhbDfcfDataAnalysis:
    """
      This class is the base class of processor.
      """

    def __init__(self):
        """
        Parameters
        ----------
        """
        self.config_parser = ConfigParserUtil.get_config_parser("config/env.cfg")
        self.mysql_database = None
        self.mysql_host = None
        self.mysql_user = None
        self.mysql_password = None
        self.mysql_args = None
        self.database_instance = None
        self.logger = get_logger(name="lhb_dfcf_data_analysis")
        self.parse_config()
        self.setup_mysql()

    def parse_config(self):
        """
        This method parses arguments from command line.
        Returns
        -------
        None
        """
        env = os.environ.get("ENV")  # ENV equals section name in env.cfg
        self.mysql_host = self.config_parser.get(env, "MYSQL_HOST")
        self.mysql_user = self.config_parser.get(env, "MYSQL_USER")
        self.mysql_password = self.config_parser.get(env, "MYSQL_PASSWORD")
        self.mysql_database = self.config_parser.get("lhb", "MYSQL_DATABASE")

    def setup_mysql(self):
        """
        This method sets up MySQL database connection instance.
        Returns
        -------
        None
        """
        self.mysql_args = {"host": self.mysql_host, "database": self.mysql_database, 'user': self.mysql_user,
                           "password": self.mysql_password}
        self.database_instance = LhbDB(self.mysql_args)
        self.database_instance.connect_db()

    def get_summary_info_by_start_date_and_end_date(self, start_date, end_date):
        return self.database_instance.select_summary_info_dfcf_by_date(start_date, end_date)

    def get_summary_info_by_stock_id(self, stock_id):
        return self.database_instance.select_summary_info_dfcf_by_stock_id(stock_id)


if __name__ == '__main__':
    lhb_dfcf_data_analysis = LhbDfcfDataAnalysis()
    print(lhb_dfcf_data_analysis.get_summary_info_by_start_date_and_end_date('2016-08-31', '2016-08-31'))
    print(lhb_dfcf_data_analysis.get_summary_info_by_stock_id('000002'))
