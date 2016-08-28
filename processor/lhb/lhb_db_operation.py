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

