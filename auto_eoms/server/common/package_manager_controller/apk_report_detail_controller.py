from common.utils.utils import Utils


class ApkReportDetailController(object):

    @classmethod
    def save_test_report(cls, model, file_obj, apk_id):
        """
        保存测试报告
        :param model:
        :param file_obj:
        :param apk_id:
        :return:
        """
        test_report_name = file_obj.name
        test_report_data = file_obj.read()
        model.objects.create(test_report_name=test_report_name, test_report_data=test_report_data, apk_id=apk_id)

    @classmethod
    def query_test_report(cls, model, apk_id):
        """
        查询测试报告信息，不返回 测试报告具体内容（具体内容为二进制文件，需下载查看）
        :param model:
        :param apk_id:
        :return:
        """
        models = model.objects.filter(apk_id__exact=apk_id).all()
        for i in range(len(models)):
            models[i].test_report_data = None           # 测试报告内容为空，否则bytes 类型不能转化为json 格式
        return Utils.model_objects_to_list(models)

    @classmethod
    def query_need_download_test_report(cls, model, report_id):
        """
        查询需要下载的测试报告
        :param model:
        :param report_id:
        :return:
        """
        return model.objects.filter(id__exact=report_id).first()

    @classmethod
    def del_test_report(cls, model, report_id, apk_id):
        """
        删除测试报告
        :param model:
        :param report_id:
        :param apk_id:
        :return:
        """
        model.objects.filter(id__exact=report_id).all().delete()
        return True if len(model.objects.filter(apk_id=apk_id).all()) == 0 else False
