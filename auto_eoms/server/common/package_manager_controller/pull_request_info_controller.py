import datetime

import requests

from common.utils.utils import Utils


class PullRequestInfoController(object):
    _TOKEN = 's5gfbkrjxck2iwasvoptwdwitjcxojjksmiu4vdhgf37l5e6n7ra'

    ANDROID_PHONE_PULL_REQUEST_BASE_URI = r'http://10.1.1.53:8080/tfs/sh-ws-office/Mapa/_apis/git/repositories/' \
                                          r'Mapa2_Android_phone/pullrequests/'

    MAPA_PULL_REQUEST_BASE_URI = r'http://10.1.1.53:8080/tfs/sh-ws-office/Mapa/_apis/git/repositories/' \
                                 r'mapa2_arm_mtk_xiaozhuo/pullrequests/'

    _PULL_REQUEST_KEY = ["pull_request_id", "value", "lastMergeTargetCommit", "commitId",
                         "closedDate", "status", "title", "pullRequestId"]

    _STRING_COMPLETED = "completed"

    _STRING_ACTIVE = "active"

    @classmethod
    def _get_pull_request_info(cls, url, pull_request_is_completed=True) -> dict:
        """
        查询 pull request 信息，pull_request_is_completed为True时，查询状态为 completed，为False时，查询当前没有完成的
        :param url:
        :param pull_request_is_completed:
        :return:
        """
        auth = ("", cls._TOKEN)
        params = {'api-version': 5.0, "searchCriteria.status": cls._STRING_COMPLETED}
        if not pull_request_is_completed:
            params = {'api-version': 5.0, "searchCriteria.status": cls._STRING_ACTIVE}
        r = requests.get(url, params=params, auth=auth, verify=False)
        return r.json()

    @classmethod
    def _get_last_complete_time(cls, model):
        """
        获得数据库最新的pull request id,model为pull request model
        :param model:
        :return:
        """
        r = model.objects.filter().order_by('-complete_time').first()
        return r.complete_time

    @classmethod
    def _write_pull_request_info_status_is_completed(cls, url, model):
        """
        数据库中记录 pull request 状态为完成的
        :param url:
        :param model:
        :return:
        """
        last_complete_time = cls._get_last_complete_time(model)
        pull_request_infos = cls._get_pull_request_info(url)
        for info in pull_request_infos.get(cls._PULL_REQUEST_KEY[1]):
            completion_time = info.get(cls._PULL_REQUEST_KEY[4]).split(".")[0]
            title = info.get(cls._PULL_REQUEST_KEY[-2])
            pull_request_id = info.get(cls._PULL_REQUEST_KEY[-1])
            completion_time = Utils.time_str_to_datetime_object(completion_time)
            if completion_time > last_complete_time:
                model.objects.create(
                    pull_request_id=pull_request_id,
                    title=title,
                    complete_time=completion_time,
                    status=cls._STRING_COMPLETED,
                )

    @classmethod
    def _write_pull_request_info_status_is_not_completed(cls, url, model):
        """
        数据库中记录 pull request 状态为未完成的
        :param url:
        :param model:
        :return:
        """
        model.objects.filter(status__exact=cls._STRING_ACTIVE).all().delete()
        pull_request_infos = cls._get_pull_request_info(url, False)
        for info in pull_request_infos.get(cls._PULL_REQUEST_KEY[1]):
            title = info.get(cls._PULL_REQUEST_KEY[-2])
            pull_request_id = info.get(cls._PULL_REQUEST_KEY[-1])
            model.objects.create(
                pull_request_id=pull_request_id,
                title=title,
                complete_time=None,
                status=cls._STRING_ACTIVE,
            )

    @classmethod
    def write_pull_request_info(cls, url, model):
        """
        数据库中写 pull request 信息，根据model url不同，写不同的库
        :param url:
        :param model:
        :return:
        """
        cls._write_pull_request_info_status_is_not_completed(url, model)
        cls._write_pull_request_info_status_is_completed(url, model)

    @classmethod
    def query_pull_request_info(cls, model, page_num, select_word=None):
        """
        查询 pull request 信息
        :param model:
        :param page_num:
        :param select_word:
        :return:
        """
        start, end = Utils.page_rules(page_num)
        if select_word is not None:
            model_infos = model.objects.filter(title__contains=select_word).order_by('-pull_request_id').all()
        else:
            model_infos = model.objects.filter().order_by('-pull_request_id').all()
            for model in model_infos:
                if model.complete_time is not None:
                    model.complete_time = Utils.utc_to_local(model.complete_time)  # utc 时间转为本地时间
        total = len(model_infos)
        return total, Utils.model_objects_to_list(model_infos[start: end])

    @classmethod
    def query_data_of_a_month_at_specific_time(cls, model, pull_request_id=None, end_time=None):
        """
        获取特定时间，一个月内的 pull request 信息
        :param model:
        :param pull_request_id:
        :param end_time:
        :return:
        """
        if end_time is None:
            end_time = model.objects.filter(pull_request_id__exact=pull_request_id).first().complete_time
            if end_time is None:  # 如果complete time为None，直接返回空数据
                return []
        month = end_time - datetime.timedelta(weeks=4)
        pull_request_models = model.objects.filter(complete_time__gte=month, complete_time__lte=end_time).order_by(
            '-complete_time')
        for model in pull_request_models:
            if model.complete_time is not None:
                model.complete_time = Utils.utc_to_local(model.complete_time)  # utc 时间转为本地时间
        return Utils.model_objects_to_list(pull_request_models)

    @classmethod
    def query_pull_request_items(cls, model, pull_request_items_str: str):
        """
         查看打标的 pull request 信息
        :param model:
        :param pull_request_items_str:
        :return:
        """
        pull_request_items_list = pull_request_items_str.split(",")
        data = model.objects.filter(pull_request_id__in=pull_request_items_list).order_by('-pull_request_id').all()
        for model in data:
            if model.complete_time is not None:
                model.complete_time = Utils.utc_to_local(model.complete_time)  # utc 时间转为本地时间
        return Utils.model_objects_to_list(data)


