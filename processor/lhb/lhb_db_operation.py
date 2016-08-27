"""
This modules handles imax MySQL database operations.
"""

import mysql.connector

from processor.db_operation import MySQLdb


class ImaxDB(MySQLdb):
    """
    This class handles lhb database operations.
    """

    def insert_cinema(self, item):
        """
        This method inserts one row into tale cinema_info.
        Parameters
        ----------
        item: row to insert

        Returns
        -------
        True if succeed.
        """
        sql = ("INSERT INTO cinema_info "
               "(cinema_id, sname, cname, address, show_time_page, feature_imax, feature_3d, lowest_price, city, process_date) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        return self.insert_data(sql, item)

    def is_cinema_existed(self, cinema_id):
        """
        This method checks whether cinema_id is existed in any row of table cinema_info.
        Parameters
        ----------
        cinema_id: cinema id (primary key)

        Returns
        -------
        True if existed.
        """

        sql = ("SELECT * FROM cinema_info "
               "WHERE cinema_id = {0}".format(cinema_id))
        try:
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            return len(rows) > 0
        except mysql.connector.Error as err:
            self.logger.exception(err)
            return False

    def select_all_cinema_info(self):
        """
        This method select all rows from table cinema_info.

        Returns
        -------
        Rows
        """

        sql = ("SELECT * FROM cinema_info "
               "WHERE 1 = 1")
        try:
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            return rows
        except mysql.connector.Error as err:
            self.logger.exception(err)
            return None

    def delete_row_by_sku_id(self, table, cinema_id):
        """
        This method deletes row(s) from table based on cinema_id.
        Parameters
        ----------
        table: which table to delete
        cinema_id: cinema id (primary key)

        Returns
        -------
        True if succeed.
        """
        sql = ("DELETE FROM {0} WHERE cinema_id = {1}".format(table, cinema_id))
        try:
            self.cursor.execute(sql)
            self.connection.commit()
            self.logger.info('delete succeed: {0}'.format(cinema_id))
            return True
        except mysql.connector.Error as err:
            self.logger.exception(err)
            return False

    def insert_seats_info(self, item):
        insert_list = (
            ('cinema_id', 0),
            ('movie_id', 0),
            ('crawled_date', 1),
            ('hall_id', 0),
            ('hall_name', 1),
            ('id', 0),
            ('is_sale', 0),
            ('movie_end_time', 1),
            ('mtime_price', 0),
            ('price', 0),
            ('show_time_id', 0),
            ('seats_count', 0),
            ('unsold_seats', 0),
            ('hall_seats_view', 1)
        )
        place_holder = ', '.join(['%s'] * len(insert_list))

        sql = ("INSERT INTO showtime_info (" +
        ', '.join([k[0] for k in insert_list]) +
               ") VALUES ({0})".format(place_holder))
        return self.insert_data(sql, item)

    def is_seats_info_existed(self, showtime_id):
        sql = ("SELECT * FROM showtime_info WHERE show_time_id = {0}"
               .format(showtime_id))
        try:
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            return len(rows) > 0
        except mysql.connector.Error as err:
            self.logger.exception(err)
            return False

    def insert_movie_info(self, movie_row):
        sql = ("INSERT INTO movie_info "
               "(movie_id, movie_info)"
               "VALUES (%s, %s)")
        return self.insert_data(sql, movie_row)

    def is_movie_existed(self, movie_id):
        sql = ("SELECT * FROM movie_info WHERE movie_id = {0}"
               .format(movie_id))
        try:
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            return len(rows) > 0
        except mysql.connector.Error as err:
            self.logger.exception(err)
            return False
