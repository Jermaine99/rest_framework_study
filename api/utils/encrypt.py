import hashlib
import time
from djangoandrest.settings import SECRET_KEY


def md5_password(data_string):
    """
        对密码进行MD5加密
    :param data_string: 输入数据
    :return: 加密后的数据
    """
    obj = hashlib.md5(SECRET_KEY.encode('utf-8'))
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()


def md5_token(user):
    """
        对用户和时间进行加密返回token
    :param user:
    :return:
    """

    ctime = str(time.time())
    m = hashlib.md5(bytes(user, encoding="utf-8"))
    m.update(bytes(ctime, encoding="utf-8"))
    return m.hexdigest()
