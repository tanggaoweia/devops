from io import BytesIO

from django.http import JsonResponse, FileResponse
from django.utils.http import urlquote

from android_phone_package_manager_server.models import *
from common.package_manager_controller.apk_detail_info_controller import ApkDetailInfoController
from common.package_manager_controller.apk_report_detail_controller import ApkReportDetailController
from common.package_manager_controller.build_info_controller import BuildInfoController
from common.package_manager_controller.pull_request_info_controller import PullRequestInfoController
from common.utils.format_data import FormatData
from common.utils.key_constant import *
from common.utils.utils import Utils


def manual_pull_info(request):
    """
    手动拉取 android phone 的信息
    :param request:
    :return:
    """
    if request.method == "GET":
        PullRequestInfoController.write_pull_request_info(PullRequestInfoController.ANDROID_PHONE_PULL_REQUEST_BASE_URI,
                                                          PullRequestInfo)
        return JsonResponse(FormatData.response_data())
    return JsonResponse(FormatData.response_data(code=FormatData.ERROR_CODE, msg=FormatData.ERROR_MSG))


def query_table_info_where_triggered_by_pull_request(request):
    """
    pull request 信息存在时，页面加载表格信息查询
    :param request:
    :return:
    """
    if request.method == "GET":
        page_num = int(request.GET.get(const.PAGE_NUM_KEY))
        select_word = request.GET.get(const.SELECT_WORD_KEY)
        total, data = PullRequestInfoController.query_pull_request_info(PullRequestInfo, page_num, select_word)
        data = BuildInfoController.query_build_info_where_triggered_by_pull_request(BuildInfo, data)
        data = ApkDetailInfoController.query_apk_detail_where_pull_request_id_is_not_zero(ApkDetailInfo, data)
        return JsonResponse(FormatData.response_data(data=data, total=total))
    return JsonResponse(FormatData.response_data(code=FormatData.ERROR_CODE, msg=FormatData.ERROR_MSG))


def query_table_info_where_not_triggered_by_pull_request(request):
    """
    pull request 信息不存在时，页面加载表格信息查询
    :param request:
    :return:
    """
    if request.method == "GET":
        page_num = int(request.GET.get(const.PAGE_NUM_KEY))
        select_word = request.GET.get(const.SELECT_WORD_KEY)
        total, data = BuildInfoController.query_build_info_where_not_triggered_by_pull_request(BuildInfo, page_num,
                                                                                               select_word)
        data = ApkDetailInfoController.query_apk_detail_where_pull_request_id_is_zero(ApkDetailInfo, data)
        return JsonResponse(FormatData.response_data(data=data, total=total))
    return JsonResponse(FormatData.response_data(code=FormatData.ERROR_CODE, msg=FormatData.ERROR_MSG))


def update_test_result(request):
    """
    更新测试结果
    :param request:
    :return:
    """
    if request.method == "POST":
        apk_id = int(request.POST.get(const.ID_KEY))
        test_result = request.POST.get(const.TEST_RESULT_KEY)
        ApkDetailInfoController.update_test_result(ApkDetailInfo, apk_id, test_result)
        return JsonResponse(FormatData.response_data())
    return JsonResponse(FormatData.response_data(code=FormatData.ERROR_CODE, msg=FormatData.ERROR_MSG))


def update_description(request):
    """
    更新测试备注
    :param request:
    :return:
    """
    if request.method == "POST":
        apk_id = int(request.POST.get(const.ID_KEY))
        description = request.POST.get(const.DESCRIPTION_KEY)
        ApkDetailInfoController.update_test_description(ApkDetailInfo, apk_id, description)
        return JsonResponse(FormatData.response_data())
    return JsonResponse(FormatData.response_data(code=FormatData.ERROR_CODE, msg=FormatData.ERROR_MSG))


def update_sign(request):
    """
    更新打标信息
    :param request:
    :return:
    """
    if request.method == "POST":
        apk_id = int(request.POST.get(const.ID_KEY))
        sign = request.POST.get(const.SIGN_KEY)
        ApkDetailInfoController.update_test_sign(ApkDetailInfo, apk_id, sign)
        return JsonResponse(FormatData.response_data())
    return JsonResponse(FormatData.response_data(code=FormatData.ERROR_CODE, msg=FormatData.ERROR_MSG))


def query_pull_request_info_of_month(request):
    """
    获得特定时间一个月内的 pull request 信息
    :param request:
    :return:
    """
    if request.method == "GET":
        build_id = request.GET.get(const.BUILD_ID_KEY)
        if build_id is not None:  # 自动build查询 过去四周 pull request
            pull_request_id = BuildInfoController.query_pull_request_id_adopt_build_id(BuildInfo, build_id)
            data = PullRequestInfoController.query_data_of_a_month_at_specific_time(PullRequestInfo, pull_request_id)
        else:  # 手动build查询 过去四周 pull request
            end_time = request.GET.get(const.TIME_KEY).split(".")[0]
            end_time = Utils.time_str_to_datetime_object(end_time)
            data = PullRequestInfoController.query_data_of_a_month_at_specific_time(PullRequestInfo, end_time=end_time)
        return JsonResponse(FormatData.response_data(data=data))
    return JsonResponse(FormatData.response_data(code=FormatData.ERROR_CODE, msg=FormatData.ERROR_MSG))


def cancel_sign(request):
    """
    取消打标
    :param request:
    :return:
    """
    if request.method == "POST":
        apk_id = int(request.POST.get(const.ID_KEY))
        ApkDetailInfoController.cancel_sign(ApkDetailInfo, apk_id)
        return JsonResponse(FormatData.response_data())
    return JsonResponse(FormatData.response_data(code=FormatData.ERROR_CODE, msg=FormatData.ERROR_MSG))


def upload_test_report(request):
    """
    上传测试报告
    :param request:
    :return:
    """
    if request.method == "POST":
        apk_id = int(request.POST.get(const.ID_KEY))
        file_obj = request.FILES.get(const.REPORT_KEY)
        if file_obj is not None:
            ApkReportDetailController.save_test_report(ApkReportDetail, file_obj, apk_id)
            ApkDetailInfoController.update_test_report_status(ApkDetailInfo, apk_id, False)
        return JsonResponse(FormatData.response_data())
    return JsonResponse(FormatData.response_data(code=FormatData.ERROR_CODE, msg=FormatData.ERROR_MSG))


def query_market_table_info(request):
    """
    市场部需要展示的包信息
    :param request:
    :return:
    """
    time_format_str = "T01:01:01"
    if request.method == "GET":
        page_num = int(request.GET.get(const.PAGE_NUM_KEY))
        select_word = request.GET.get(const.SELECT_WORD_KEY)
        start_time = request.GET.get(const.START_TIME_KEY)
        start_time = start_time + time_format_str if start_time != "" and start_time is not None and start_time != "null" else None
        end_time = request.GET.get(const.END_TIME_KEY)
        end_time = end_time + time_format_str if end_time != "" and end_time is not None and end_time != "null" else None
        total, data = ApkDetailInfoController.query_market_info(ApkDetailInfo, page_num, select_word, start_time,
                                                                end_time)
        return JsonResponse(FormatData.response_data(data=data, total=total))
    return JsonResponse(FormatData.response_data(code=FormatData.ERROR_CODE, msg=FormatData.ERROR_MSG))


def update_market_desc(request):
    """
    更新 市场备注
    :param request:
    :return:
    """
    if request.method == "POST":
        apk_id = int(request.POST.get(const.ID_KEY))
        description = request.POST.get(const.DESCRIPTION_KEY)
        ApkDetailInfoController.update_market_description(ApkDetailInfo, apk_id, description)
        return JsonResponse(FormatData.response_data())
    return JsonResponse(FormatData.response_data(code=FormatData.ERROR_CODE, msg=FormatData.ERROR_MSG))


def sign_pull_request_info(request):
    """
    查看打标的 pull request 信息
    :param request:
    :return:
    """
    if request.method == "GET":
        apk_id = int(request.GET.get(const.ID_KEY))
        pull_request_items = ApkDetailInfoController.query_pull_request_items(ApkDetailInfo, apk_id)
        data = PullRequestInfoController.query_pull_request_items(PullRequestInfo, pull_request_items)
        return JsonResponse(FormatData.response_data(data=data))
    return JsonResponse(FormatData.response_data(code=FormatData.ERROR_CODE, msg=FormatData.ERROR_MSG))


def query_market_test_report(request):
    """
    市场部 查询测试报告
    :param request:
    :return:
    """
    if request.method == "GET":
        apk_id = int(request.GET.get(const.ID_KEY))
        data = ApkReportDetailController.query_test_report(ApkReportDetail, apk_id)
        return JsonResponse(FormatData.response_data(data=data))
    return JsonResponse(FormatData.response_data(code=FormatData.ERROR_CODE, msg=FormatData.ERROR_MSG))


def download_test_report(request):
    """
    下载测试报告
    :param request:
    :return:
    """
    if request.method == "GET":
        report_id = int(request.GET.get(const.ID_KEY))
        report_obj = ApkReportDetailController.query_need_download_test_report(ApkReportDetail, report_id)
        response = FileResponse(BytesIO(report_obj.test_report_data))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{}"'.format(urlquote(report_obj.test_report_name))
        return response
    return JsonResponse(FormatData.response_data(code=FormatData.ERROR_CODE, msg=FormatData.ERROR_MSG))


def del_test_report(request):
    """
    删除测试报告
    :param request:
    :return:
    """
    if request.method == "POST":
        report_id = int(request.POST.get(const.ID_KEY))
        apk_id = int(request.POST.get(const.APP_ID_KEY))
        del_ret = ApkReportDetailController.del_test_report(ApkReportDetail, report_id, apk_id)
        if del_ret:
            ApkDetailInfoController.update_test_report_status(ApkDetailInfo, apk_id)
        return JsonResponse(FormatData.response_data())
    return JsonResponse(FormatData.response_data(code=FormatData.ERROR_CODE, msg=FormatData.ERROR_MSG))