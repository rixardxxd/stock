import mysql.connector
from config.config_parser_util import ConfigParserUtil
import os


def get_db_connection():
    env = os.environ.get("ENV")
    config_parser = ConfigParserUtil.get_config_parser("config/env.cfg")
    mysql_args = {"host": config_parser.get(env, "MYSQL_HOST"),
                  "user": config_parser.get(env, "MYSQL_USER"),
                  'password': config_parser.get(env, "MYSQL_PASSWORD"),
                  "database": config_parser.get("lhb", "MYSQL_DATABASE")}

    return mysql.connector.connect(**mysql_args)
