from rest_framework.throttling import SimpleRateThrottle, ScopedRateThrottle
from django.core.cache import cache as default_cache
from apis.extension import returnCode
from rest_framework.exceptions import APIException
from rest_framework import status


class ThrottledException(APIException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_code = 'throttled'


class NewsCreateRateThrottle(SimpleRateThrottle):
    cache = default_cache
    cache_format = 'throttle_%(scope)s_%(ident)s'
    # construct key of cache.
    scope = "user"

    THROTTLE_RATES = {"user": "1/20s"}

    def parse_rate(self, rate):
        """
        Given the request rate string, return a two tuple of:
        <allowed number of requests>, <period of time in seconds>
        """
        if rate is None:
            return (None, None)
        num, period = rate.split('/')
        num_requests = int(num)
        duration = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}[period[-1]]
        # 忘记转换数据类型，无类型检查
        count = int(period[0: -1])

        return (num_requests, count * duration)

    def get_cache_key(self, request, view):
        ident = request.user.pk
        return self.cache_format % {
            'scope': self.scope,
            #  scope = "user"
            'ident': ident}

    def throttle_failure(self):
        wait = self.wait()
        detail = {
            "code": returnCode.REQUEST_OVERLOAD,
            "data": "访问频率限制",
            'detail': "需等待{}秒后才能访问".format(int(wait))
        }
        raise ThrottledException(detail)

    def throttle_success(self):
        # self.history.insert(0, self.now)
        # self.cache.set(self.key, self.history, self.duration)
        return True

    def done(self):
        """
        after storing data in database, news class call this function to avoid error data posted to be throttled.
        """
        self.history.insert(0, self.now)
        self.cache.set(self.key, self.history, self.duration)
