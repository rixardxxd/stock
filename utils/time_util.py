"""
This module provides time related utility methods.
"""
import time
import datetime
import pytz

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
SIMPLE_DATETIME_FORMAT = "%Y%m%d"
CHINA_TIMEZONE = "Asia/Shanghai"
UTC_TIMEZONE = "UTC"


def get_current_timestamp(timezone="UTC"):
    """
    This method gets current timestamp in Chinese time zone (UTC +8)
    Format: YYYY-MM-DD hh:mm:ss
    Parameters
    ----------
    timezone: an instance in pytz all_timezones, http://pytz.sourceforge.net/

    Returns
    -------
    timestamp in DATETIME_FORMAT
    """
    tz = pytz.timezone(timezone)
    today = datetime.datetime.now(tz).strftime(DATETIME_FORMAT)
    return today


def get_current_timestamp_with_simple_datetime_format(timezone="UTC"):
    """
    This method gets current timestamp in Chinese time zone (UTC +8)
    Format: YYYYMMDD
    Parameters
    ----------
    timezone: an instance in pytz all_timezones, http://pytz.sourceforge.net/

    Returns
    -------
    timestamp in DATETIME_FORMAT
    """
    tz = pytz.timezone(timezone)
    today = datetime.datetime.now(tz).strftime(SIMPLE_DATETIME_FORMAT)
    return today


def unix_current_time():
    """
    Get current time in unix timestamp. Return Long
    Returns
    -------

    """
    now = datetime.datetime.now()
    return time.mktime(now.timetuple())


def unix_to_china_time(timestamp):
    """
    Convert timestamp to China time
    Parameters
    ----------
    timestamp

    Returns
    -------

    """
    t = datetime.datetime.fromtimestamp(timestamp, pytz.timezone(CHINA_TIMEZONE))
    return t.strftime(DATETIME_FORMAT)


def naive_datetime_to_china_datetime(dt):
    """
    Convert datetime without timezone info to China timezone
    Parameters
    ----------
    dt

    Returns
    -------

    """
    tz = pytz.timezone(CHINA_TIMEZONE)
    dt = tz.localize(dt)
    return dt
