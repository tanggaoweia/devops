import json

from django.http import JsonResponse

# Create your views here.
from dl_model_manager.dl_model_manager import DLModelManager
from dl_model_manager.models import ModelsAndNetworksInfo
from common.utils.key_constant import *
from utils.format_data import FormatData


def models_and_networks_upload(request):
    """
    模型和网络上传
    :param request:
    :return:
    """
    if request.method == 'POST':
        files = request.FILES
        if len(files) > 0:
            DLModelManager.model_and_network_save(files)
            return JsonResponse(FormatData.response_data())
    return JsonResponse(FormatData.response_data(msg=FormatData.ERROR_MSG, code=FormatData.ERROR_CODE))


def models_and_networks_flops_data(request):
    """
    模型和网络算力结果记录
    :param request:
    :return:
    """
    if request.method == 'POST':
        data = json.dumps(str(request.body, encoding='utf-8'))
        DLModelManager.update_models_and_networks_flops(ModelsAndNetworksInfo, data)
        return JsonResponse(FormatData.response_data())
    return JsonResponse(FormatData.response_data(msg=FormatData.ERROR_MSG, code=FormatData.ERROR_CODE))


def models_and_networks_run_flops_script(request):
    """
    跑算力脚本
    :param request:
    :return:
    """
    if request.method == 'GET':
        id_num = request.GET.get(const.ID_KEY)
        DLModelManager.run_flops_script(ModelsAndNetworksInfo, id_num)
        return JsonResponse(FormatData.response_data())
    return JsonResponse(FormatData.response_data(msg=FormatData.ERROR_MSG, code=FormatData.ERROR_CODE))


def models_and_networks_full_info(request):
    """
    获得模型和网络数据
    :param request:
    :return:
    """
    if request.method == 'GET':
        page_num = int(request.GET.get(const.PAGE_NUM_KEY))
        select_word = request.GET.get(const.SELECT_WORD_KEY)
        total, data = DLModelManager.get_full_info(ModelsAndNetworksInfo, page_num, select_word)
        return JsonResponse(FormatData.response_data(data=data, total=total))


def models_and_networks_flops_script_sign(request):
    """
    flops脚本 队列标记
    :param request:
    :return:
    """
    if request.method == "POST":
        id_num = request.POST.get(const.ID_KEY)
        DLModelManager.flops_script_sign(ModelsAndNetworksInfo, id_num)
        return JsonResponse(FormatData.response_data())
    return JsonResponse(FormatData.response_data(msg=FormatData.ERROR_MSG, code=FormatData.ERROR_CODE))