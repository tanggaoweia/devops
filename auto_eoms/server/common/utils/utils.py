import time
from datetime import datetime


class Utils(object):
    @classmethod
    def page_rules(cls, page_num):
        """
        分页规则，每页默认十条
        :param page_num:
        :return:
        """
        return 10 * (page_num - 1), 10 * page_num

    @classmethod
    def model_objects_to_list(cls, model_objects):
        """
        model 查询结果转化为 [{},{}] 格式
        :param model_objects:
        :return:
        """
        model_dict_list = []
        for model_obj in model_objects:
            model_dict = model_obj.__dict__
            model_dict.pop('_state')
            model_dict_list.append(model_dict)
        return model_dict_list

    @classmethod
    def time_str_to_datetime_object(cls, time_str):
        """
         时间字符串转化为datetime对象
        :param time_str:
        :return:
        """
        return datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S")

    @classmethod
    def utc_to_local(cls, utc_dtm):
        """
        utc 时间转本地时间
        :param utc_dtm:
        :return:
        """
        now_stamp = time.time()
        local_time = datetime.fromtimestamp(now_stamp)
        utc_time = datetime.utcfromtimestamp(now_stamp)
        offset = local_time - utc_time
        return utc_dtm + offset






