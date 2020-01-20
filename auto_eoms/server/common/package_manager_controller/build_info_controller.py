import json

from common.package_manager_controller.base_info_controller import BaseInfoController
from common.utils.commit import Commit
from common.utils.key_constant import *
from common.utils.utils import Utils


class BuildInfoController(BaseInfoController):

    def write_build_info(self, model, base_url):
        """
        记录build 信息
        :param model:
        :param base_url:
        :return:
        """
        commit_msg = Commit.get_commit_msg(self._commit_id, base_url)
        if self._pull_request_id is None:
            model.objects.create(build_id=self._build_id,
                                 commit_msg=commit_msg,
                                 apk_type=self._job_name,
                                 jenkins_info_full_str=json.dumps(self._jenkins_info))
        else:
            model.objects.create(build_id=self._build_id,
                                 commit_msg=commit_msg,
                                 apk_type=self._job_name,
                                 pull_request_id=self._pull_request_id,
                                 jenkins_info_full_str=json.dumps(self._jenkins_info))

    @classmethod
    def query_build_info_where_triggered_by_pull_request(cls, model, pull_request_query_data):
        """
        根据传入的 pull request 信息，查询对应的 build 信息
        :param model:
        :param pull_request_query_data:
        :return:
        """
        for i in range(len(pull_request_query_data)):
            pull_request_id = pull_request_query_data[i].get(const.DATA_PULL_REQUEST_ID_KEY)
            models = model.objects.filter(pull_request_id__exact=pull_request_id).values(
                "build_id").distinct().order_by('-build_id').all()
            pull_request_query_data[i][const.DATA_KEY] = list(models)
        return pull_request_query_data

    @classmethod
    def query_build_info_where_not_triggered_by_pull_request(cls, model, page_num, select_word):
        """
        pull request 信息不存在时，页面加载表格信息查询
        :param model:
        :param page_num:
        :param select_word:
        :return:
        """
        start, end = Utils.page_rules(page_num)
        if select_word is not None:
            models = model.objects.filter(pull_request_id__exact=0, commit_msg__contains=select_word).values(
                "build_id").distinct().order_by('-build_id').all()
        else:
            models = model.objects.filter(pull_request_id__exact=0).values(
                "build_id").distinct().order_by('-build_id').all()
        total = len(models)
        models = list(models)[start: end]
        for i in range(len(models)):
            build_id = models[i].get(const.BUILD_ID_KEY)
            build_model = model.objects.filter(build_id__exact=build_id).order_by('-create_time').all()
            models[i] = Utils.model_objects_to_list(build_model)[0]
        return total, models

    @classmethod
    def query_pull_request_id_adopt_build_id(cls, model, build_id):
        """
        通过 build id 查询 pull request it
        :param model:
        :param build_id:
        :return:
        """
        return model.objects.filter(build_id__exact=build_id).first().pull_request_id
