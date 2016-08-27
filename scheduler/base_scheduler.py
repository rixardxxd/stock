from scrapy_redis import get_redis


class BaseRedisScheduler(object):
    """
    This is a parent Scheduler class
    """

    def __init__(self, params):
        self.r = None
        self.params = params

    def connect_redis(self):
        self.r = get_redis(host=self.params['host'], port=self.params['port'])
