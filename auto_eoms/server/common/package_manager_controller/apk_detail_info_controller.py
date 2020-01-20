import os
from datetime import datetime

from common.package_manager_controller.base_info_controller import BaseInfoController
from common.utils.key_constant import *
from common.utils.utils import Utils


class ApkDetailInfoController(BaseInfoController):

    def write_apk_detail_info(self, model):
        """
        记录 apk 信息
        :param model:
        :return:
        """
        common_path = self._apk_common_path
        apk_s = os.listdir(common_path + self._job_name)
        for apk in apk_s:
            print(apk)
            model.objects.create(build_id=self._build_id, apk_name=apk, apk_type=self._job_name,
                                 apk_location=common_path + self._job_name + os.sep + apk)

    @classmethod
    def query_apk_detail_where_pull_request_id_is_not_zero(cls, model, pull_request_query_data):
        """
        根据传入的 pull request 信息，查询对应的 apk detail 信息
        :param model:
        :param pull_request_query_data:
        :return:
        """
        for i in range(len(pull_request_query_data)):
            build_infos = pull_request_query_data[i].get(const.DATA_KEY)
            for j in range(len(build_infos)):
                build_id = build_infos[j].get(const.BUILD_ID_KEY)
                models = model.objects.filter(build_id__exact=build_id, apk_type__in=["debug", "release"]).order_by(
                    '-create_time').all()
                pull_request_query_data[i][const.DATA_KEY][j][const.DATA_KEY] = Utils.model_objects_to_list(models)
        return pull_request_query_data

    @classmethod
    def query_apk_detail_where_pull_request_id_is_zero(cls, model, pull_request_query_data):
        """
        pull request 信息不存在时， 查询对应的 apk detail 信息
        :param model:
        :param pull_request_query_data:
        :return:
        """
        for i in range(len(pull_request_query_data)):
            build_id = pull_request_query_data[i].get(const.BUILD_ID_KEY)
            models = model.objects.filter(build_id__exact=build_id, apk_type__in=["debug", "release"]).order_by(
                '-create_time').all()
            pull_request_query_data[i][const.DATA_KEY] = Utils.model_objects_to_list(models)
        return pull_request_query_data

    @classmethod
    def update_test_result(cls, model, apk_id, result_str):
        """
        更新 测试结果
        :param model:
        :param apk_id:
        :param result_str:
        :return:
        """
        model.objects.filter(id__exact=apk_id).update(test_result=result_str)

    @classmethod
    def update_test_description(cls, model, apk_id, description_str):
        """
         更新 测试备注
        :param model:
        :param apk_id:
        :param description_str:
        :return:
        """
        model.objects.filter(id__exact=apk_id).update(test_desc=description_str)

    @classmethod
    def update_test_sign(cls, model, apk_id, sign_str):
        """
        更新 测试打标信息, 只有打标时，修改update time
        :param model:
        :param apk_id:
        :param sign_str:
        :return:
        """
        apk_info = model.objects.get(id__exact=apk_id)
        apk_info.pull_request_items = sign_str
        apk_info.is_tab = 1
        apk_info.save()

    @classmethod
    def cancel_sign(cls, model, apk_id):
        """
        取消打标信息
        :param model:
        :param apk_id:
        :return:
        """
        model.objects.filter(id__exact=apk_id).update(is_tab=0)

    @classmethod
    def update_test_report_status(cls, model, apk_id, is_report_deleted=True):
        """
        更新测试报告状态为1（已上传）
        :param model:
        :param apk_id:
        :param is_report_deleted:
        :return:
        """
        if is_report_deleted:
            model.objects.filter(id__exact=apk_id).update(is_report='0')
        else:
            model.objects.filter(id__exact=apk_id).update(is_report='1')

    @classmethod
    def query_market_info(cls, model, page_num, select_word, start_time, end_time):
        """
         市场部下载 vue 表格中信息获取
        :param model:
        :param page_num:
        :param select_word:
        :param start_time:
        :param end_time:
        :return:
        """
        start, end = Utils.page_rules(page_num)
        end_time = datetime.now() if end_time is None else end_time
        start_time = Utils.time_str_to_datetime_object('1970-01-01T01:01:01') if start_time is None else start_time
        if select_word is None:
            release_info = model.objects.filter(test_result__exact="测试通过", is_tab__exact=1, is_report=1,
                                                update_time__range=(start_time, end_time)).order_by('-update_time').all()
        else:
            release_info = model.objects.filter(test_result__exact="测试通过", is_tab__exact=1, is_report=1,
                                                update_time__range=(start_time, end_time),
                                                apk_name__contains=select_word).order_by('-update_time').all()
        data = Utils.model_objects_to_list(release_info)[start: end]
        total = len(release_info)
        return total, data

    @classmethod
    def update_market_description(cls, model, apk_id, description_str):
        """
        更新 市场备注
        :param model:
        :param apk_id:
        :param description_str:
        :return:
        """
        model.objects.filter(id__exact=apk_id).update(market_desc=description_str)

    @classmethod
    def query_pull_request_items(cls, model, apk_id):
        """
        查询 打标的 pull request items 列表
        :param model:
        :param apk_id:
        :return:
        """
        return model.objects.filter(id__exact=apk_id).first().pull_request_items
