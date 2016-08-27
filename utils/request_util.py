"""
This modules handles url related utility functions.
"""
import grequests
import requests


def get_requests_session(pool_connections=1, pool_maxsize=32, max_retries=5):
    """
    This method gets a request session.
    Call this function when send many requests to the same host.
    Parameters
    ----------
    pool_connections: number of connection pools
    pool_maxsize: size of each pool
    max_retries: max retry times when connection fails

    Returns
    -------
    Session
    """
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(pool_connections=pool_connections,
                                            pool_maxsize=pool_maxsize, max_retries=max_retries)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def get_grequests_session(pool_connections=1, pool_maxsize=32, max_retries=5):
    """
    This method gets a grequest session.
    Call this function when send many requests to the same host.
    Parameters
    ----------
    pool_connections: number of connection pools
    pool_maxsize: size of each pool
    max_retries: max retry times when connection fails

    Returns
    -------
    Session
    """
    session = grequests.Session()
    adapter = requests.adapters.HTTPAdapter(pool_connections=pool_connections,
                                            pool_maxsize=pool_maxsize,
                                            max_retries=max_retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session
