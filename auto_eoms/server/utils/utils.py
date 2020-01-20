import datetime

import pytz


class Utils:

    TIMEZONE = 'Asia/Shanghai'

    @classmethod
    def page_rules(cls, page_num):
        """
        分页规则，每页默认十条
        :param page_num:
        :return:
        """
        return 10 * (page_num - 1)

    @classmethod
    def get_time(cls, filename=False, dir_=False) -> str:
        """获得时区为上海的当前时间"""
        tz = pytz.timezone(cls.TIMEZONE)
        if filename:
            return datetime.datetime.now(tz).strftime("%Y-%m-%d %H-%M-%S")
        if dir_:
            return datetime.datetime.now(tz).strftime("%Y-%m-%d")
        return datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
