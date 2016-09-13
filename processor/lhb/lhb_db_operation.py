"""
This modules handles LHB MySQL database operations.
"""
from processor.db_operation import MySQLdb
import mysql
import traceback


class LhbDB(MySQLdb):
    """
    This class handles lhb database operations.
    """

    def insert_summary_info(self, item):
        """
        This method inserts one row into tale lhb_summary.
        Parameters
        ----------
        item: row to insert

        Returns
        -------
        True if succeed.
        """
        sql = ("INSERT INTO lhb_summary"
               "(stock_id, end_date, reason, change_percent, buy_value, sell_value, net_value, process_date) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
        return self.insert_data(sql, item)

    def insert_summary_info_dfcf(self, item):
        """
        This method inserts one row into tale lhb_summary.
        Parameters
        ----------
        item: row to insert

        Returns
        -------
        True if succeed.
        """
        sql = ("INSERT INTO lhb_summary_dfcf"
               "(lhb_date, stock_id, stock_name, close_price, change_percent, "
               "lhb_net_value, lhb_buy_value, lhb_sell_value, lhb_total_value, trade_amount,"
               "net_value_percent, total_value_percent, turnover_ratio, reason, process_date) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        return self.insert_data(sql, item)

    def insert_detail_info_dfcf(self, item):
        """
        This method inserts one row into tale lhb_summary.
        Parameters
        ----------
        item: row to insert

        Returns
        -------
        True if succeed.
        """
        sql = ("INSERT INTO lhb_detail_dfcf"
               "(lhb_date, stock_id, stock_name, reason, yyb_name, buy_or_sell, buy_or_sell_order, "
               "buy_value, buy_value_percent, sell_value, sell_value_percent, net_value, process_date) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        return self.insert_data(sql, item)

    def select_summary_info_dfcf_by_date(self, start_date, end_date):
        """
        Pass in start_date and end_date like 'YYYY-MM-DD'
        Parameters
        ----------
        start_date
        end_date

        Returns
        -------

        """
        sql = ("SELECT * FROM lhb_summary_dfcf "
               "WHERE lhb_date >= '{0}' and lhb_date <= '{1}'".format(start_date, end_date))
        try:
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            return rows
        except mysql.connector.Error as err:
            self.logger.exception(err)
            return False

    def is_summary_info_existed(self, stock_id, lhb_date, reason):
        """"
        Pass in
        Parameters
        ----------
        stock_id
        lhb_date
        reason

        Returns
        -------
        """
        sql = ("SELECT * FROM lhb_summary_dfcf "
               "WHERE stock_id = '{0}' and lhb_date = '{1}' and reason = '{2}'".format(stock_id, lhb_date, reason))
        try:
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            return len(rows) > 0
        except mysql.connector.Error as err:
            self.logger.exception("Exception. {0}. Trace: {1}".format(err, traceback.print_exc()))
            return False

    def is_detail_info_existed(self, stock_id, lhb_date, reason, yyb_name, buy_or_sell, buy_or_sell_order):
        """"
        Pass in
        Parameters
        ----------
        stock_id
        lhb_date
        reason
        yyb_name
        buy_or_sell
        buy_or_sell_order

        Returns
        -------
        """
        sql = ("SELECT * FROM lhb_detail_dfcf "
               "WHERE stock_id = '{0}' and lhb_date = '{1}' and reason = '{2}' "
               "and yyb_name = '{3}' and buy_or_sell = {4} and buy_or_sell_order = {5}".format(stock_id, lhb_date, reason, yyb_name, buy_or_sell, buy_or_sell_order))
        try:
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            return len(rows) > 0
        except mysql.connector.Error as err:
            self.logger.exception("Exception. {0}. Trace: {1}".format(err, traceback.print_exc()))
            return False

    def select_summary_info_dfcf_by_stock_id(self, stock_id):
        """
        Pass in stock_id'
        Parameters
        ----------
        stock_id

        Returns
        -------

        """
        sql = ("SELECT * FROM lhb_summary_dfcf "
               "WHERE stock_id = {0}".format(stock_id))
        try:
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            return rows
        except mysql.connector.Error as err:
            self.logger.exception(err)
            return False
