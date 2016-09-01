"""
This modules handles imax MySQL database operations.
"""
from processor.db_operation import MySQLdb


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
               "(lhb_date, stock_id, stock_name, close_price, change_percent, lhb_net_value, lhb_buy_value, lhb_sell_value, lhb_total_value, trade_amount, net_value_percent, total_value_percent, turnover_ratio, market_value, reason, process_date) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        return self.insert_data(sql, item)

