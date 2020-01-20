import datetime
import pytz
import os
import re
import inspect
from conf.constant_settings import RESPONSE_VALUE_KEY, RESPONSE_TOTAL_NUM_KEY, NONE_EXCEPTION, APK_PATH_KEY


class Utils(object):

    CREATED_TIME = 'created_time'

    TIMEZONE = 'Asia/Shanghai'

    @classmethod
    def get_time(cls, filename=False) -> str:
        """获得时区为上海的当前时间"""
        tz = pytz.timezone(Utils.TIMEZONE)
        if filename:
            return datetime.datetime.now(tz).strftime("%Y-%m-%d %H-%M-%S")
        return datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def is_file_not_empty(cls, filename) -> bool:
        """判断文件是否为空"""
        if os.path.exists(filename):
            return os.path.getsize(filename) > 0

    @classmethod
    def page_rule(cls, page: int):
        """查询接口的分页规则"""
        return 10 * page - 10, 10

    @classmethod
    def sql_result_converted_to_json(cls, select_value_result: list, select_total_num: int) -> dict:
        """datetime 转化为str 格式"""
        dict_result = {}
        for i in range(len(select_value_result)):
            for j in select_value_result[i]:
                if j == Utils.CREATED_TIME:
                    select_value_result[i][j] = str(select_value_result[i][j])
        dict_result[RESPONSE_VALUE_KEY] = select_value_result
        dict_result[RESPONSE_TOTAL_NUM_KEY] = select_total_num
        return dict_result

    @classmethod
    def get__function_name(cls):
        """获取正在运行函数(或方法)名称"""
        return inspect.stack()[1][3]

    @classmethod
    def exception_to_str(cls, e):
        """error信息转化为str"""
        return Utils.del_str_quotes(str(e))if e is not None else NONE_EXCEPTION

    @classmethod
    def del_str_quotes(cls, string) -> str:
        """删除字符串中的单引号和双引号"""
        string = re.sub("\"", ' ', string)
        return re.sub("'", " ", string)



