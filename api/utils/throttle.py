from rest_framework.throttling import BaseThrottle, SimpleRateThrottle

import time

VISIT_RECORD = {}  # 这东西可以放到缓存里去

'''自定义 频率控制
class VisitThrottle(BaseThrottle):
    """实现 节流 60s内只能访问三次"""

    def __init__(self):
        self.ctime = None
        self.history = None

    def allow_request(self, request, view):
        # 1、获取用户IP 和当前时间
        # remote_addr = request._request.META.get('REMOTE_ADDR')
        remote_addr = request.META.get('REMOTE_ADDR')
        # print(remote_addr)
        # print("****************************")
        self.ctime = time.time()
        # 2. 如果第一次没有访问记录可以运行
        if remote_addr not in VISIT_RECORD:
            VISIT_RECORD[remote_addr] = [self.ctime, ]
            return True
        # 3.如过有访问记录 去 VISIT_RECORD获取访问记录
        history = VISIT_RECORD.get(remote_addr)
        self.history = history
        # 4.技术要点 time.time() 可以相加 以秒为单位
        while history and history[-1] < self.ctime - 60:
            history.pop()

        if len(history) < 3:
            history.insert(0, self.ctime)
            return True

    def wait(self):
        """

        :return: 返还等待时间
        """
        return 60 - (self.ctime - self.history[-1])
'''


# 调用 trolling 中接口实现
class VisitorThrottle(SimpleRateThrottle):
    scope = "visitor"

    def get_cache_key(self, request, view):
        return self.get_ident(request)


class UserThrottle(SimpleRateThrottle):
    scope = "user"

    def get_cache_key(self, request, view):
        return request.user.username
