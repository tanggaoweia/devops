import pytz
import datetime


class TimeUtils(object):
    """工具类"""

    _TIMEZONE = 'Asia/Shanghai'
    _TZ = pytz.timezone(_TIMEZONE)

    @classmethod
    def get_time(cls, filename=False) -> str:
        """
        获得时区为上海的格式化时间，默认获得的时间不能作为文件名
        :param filename:
        :return:
        """
        tz = pytz.timezone(TimeUtils._TIMEZONE)
        data = datetime.datetime.now(tz)
        if filename:
            return data.strftime("%Y-%m-%d %H-%M-%S")
        return data.strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def time_with_year_month_day(cls, with_end="/") -> str:
        """
        获取时区为上海，年月日格式的日期: yyyyMMdd，默认获得时间可以作为目录使用
        :return:
        """
        return datetime.datetime.now(TimeUtils._TZ).strftime("%Y%m%d{}".format(with_end))

# test


# if __name__ == '__main__':
# #     data = TimeUtils.get_time()
# #     print(data)
# #     data = TimeUtils.get_time(True)
# #     print(data)
# #     data = TimeUtils.time_with_year_month_day()
# #     print(data)
# #     data = TimeUtils.time_with_year_month_day("")
# #     print(data)
