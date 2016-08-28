import sys

import mysql.connector
from utils.logger_util import get_logger

from utils.time_util import get_current_timestamp


class MySQLdb:
    """
    Base class for mysql database operations
    db_args = {
        'user': username,
        'password': password,
        'host': db instance host IP address,
        'database: db name'
    }
    """

    def __init__(self, db_args):
        self.db_args = db_args
        self.connection = None
        self.cursor = None
        log_name = "{0}_db.log".format(db_args.get('database', 'no'))
        self.logger = get_logger(log_name)

    # Connect to database
    def connect_db(self):
        try:
            self.connection = mysql.connector.connect(**self.db_args)
            self.cursor = self.connection.cursor()
            return True
        except Exception as e:
            self.logger.exception(e)
            sys.exit()

    # General insert
    def insert_data(self, insert_ddl, insert_data):
        try:
            self.cursor.execute(insert_ddl, insert_data)
            self.connection.commit()
            self.logger.info('Insertion succeed! Timestamp: {0} {1}'
                             .format("UTC+08:00", get_current_timestamp("Asia/Shanghai")))
            return True
        except mysql.connector.Error as err:
            self.logger.exception('Insertion failed. Exception: {0}. Timestamp: {1} {2}'
                                  .format(err, "UTC+08:00", get_current_timestamp("Asia/Shanghai")))
            return False

    # Close the database connection
    def close_db(self):
        self.connection.close()
