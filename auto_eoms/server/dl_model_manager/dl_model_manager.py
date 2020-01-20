import json
import os
import platform
import time

from dl_model_manager.models import ModelsAndNetworksInfo
from utils.utils import Utils
from common.utils.utils import Utils as Util


class DLModelManager:

    if platform.system() == "Windows":
        common_path = r"D:/model-files/"
    if platform.system() == "Linux":
        common_path = r"/usr/share/auto_eoms/models-file/"

    TOTAL_PARAMS_KEY = 'total params:'

    FLOPS_KEY = 'FLOPs: '

    FLOPS_SCRIPT_STATUS_WAIT_IN_LINE = "脚本队列中"

    @classmethod
    def model_and_network_save(cls, files):
        """
        模型和网络保存
        :param files:
        :return:
        """
        files_path = cls._mkdir() + os.sep
        for i in files:
            f = open(files_path + i, 'wb')
            for j in files.get(i).chunks():
                f.write(j)
            f.close()
        cls.write_model_and_network_info_of_upload(files, files_path)

    @classmethod
    def write_model_and_network_info_of_upload(cls, files, files_path):
        """
        上传的模型和网络结构保存到数据库
        :param files:
        :param files_path:
        :return:
        """
        model_name, model_path, model_size, network_path = None, None, None, None
        for filename in files:
            filename_split = filename.split('.')
            if "model" in filename_split[-1]:
                model_name = filename_split[0]
                model_path = files_path + filename
                model_size = os.path.getsize(model_path)
            else:
                network_path = files_path + filename
                print(network_path)
        ModelsAndNetworksInfo.objects.create(
            common_path=cls.common_path,
            models_name=model_name,
            models_path=model_path,
            models_size=model_size,
            networks_path=network_path
        )

    @classmethod
    def _mkdir(cls):
        """
        模型保存路径
        :return:
        """
        time_path = Utils.get_time(dir_=True)
        common_path = cls.common_path + time_path
        if not os.path.exists(common_path):
            os.makedirs(common_path)
        path = common_path + os.sep + str(time.time())
        os.makedirs(path)
        return path

    @classmethod
    def update_models_and_networks_flops(cls, model, data):
        """
         模型和网络算力结果记录
        :param model:
        :param data:
        :return:
        """
        data = json.loads(data, encoding='utf-8')
        r = json.loads(data, encoding='utf-8')
        id_num = r.get('id')
        model = model.objects.get(id__exact=id_num)
        model.flops = r.get(cls.FLOPS_KEY)
        model.flops_result_info = data
        model.total_params = r.get(cls.TOTAL_PARAMS_KEY)
        model.flops_result = '脚本执行完毕'
        model.save()

    @classmethod
    def run_flops_script(cls, model, id_num):
        """
        执行算力脚本
        :param model:
        :param id_num:
        :return:
        """
        model = model.objects.filter(id__exact=id_num).first()
        networks_path = model.networks_path
        os.system("python ../ws_calc_params.py %s %s" % (networks_path, id_num))

    @classmethod
    def get_full_info(cls, model, page_num, select_word):
        """
        获得模型和网络数据
        :param model:
        :param page_num:
        :param select_word:
        :return:
        """
        start, end = Util.page_rules(page_num)
        if select_word is not None:
            dl_model_info = model.objects.filter(models_name__contains=select_word).order_by('-create_time').all()
        else:
            dl_model_info = model.objects.filter().order_by('-create_time').all()
        total = len(dl_model_info)
        data = Util.model_objects_to_list(dl_model_info[start: end])
        for i in range(len(data)):
            if len(data[i].get("flops_result_info")) > 0:
                data[i]["flops_result_info"] = json.loads(data[i].get("flops_result_info"), encoding="utf-8")
        return total, data

    @classmethod
    def batch_run_flops_script(cls, model):
        """
        批量跑脚本
        :param model:
        :return:
        """
        models_info = model.objects.filter(flops_result__exact=cls.FLOPS_SCRIPT_STATUS_WAIT_IN_LINE).all()
        for model in models_info:
            id_num = model.id
            cls.run_flops_script(ModelsAndNetworksInfo, id_num)

    @classmethod
    def flops_script_sign(cls, model, id_num):
        """
        执行脚本标记
        :param model:
        :param id_num:
        :return:
        """
        model = model.objects.get(id__exact=id_num)
        model.flops_result = cls.FLOPS_SCRIPT_STATUS_WAIT_IN_LINE
        model.save()






