from django.shortcuts import HttpResponse

# Create your views here.


from jenkinsapi.jenkins import Jenkins

import android_phone_package_manager_server.models
from common.package_manager_controller.apk_detail_info_controller import ApkDetailInfoController
from common.package_manager_controller.build_info_controller import BuildInfoController
import mapa_package_manager_server.models
from common.utils.commit import Commit
from utils.constant_key import NAME_KEY
from common.utils.format_data import FormatData

JENKINS_URL = 'http://10.1.1.82'
USER = 'sh-ws-jenkins1'
PASSWORD = 'abc1234!'


def jenkins_info(request):
    """
    jenkins build完成后，消息通知，build msg获取
    :param request:
    :return:
    """
    print(request.POST)
    jenkins_object = Jenkins(JENKINS_URL, USER, PASSWORD)
    if request.method == 'POST':
        request_list = request.POST.get('url').split('/')
        job_name = request_list[-3]
        build_num = request_list[-2]
        job = jenkins_object[job_name]
        build_info = job.get_build(int(build_num))
        build_msg = build_info.get_params()
        data = {**build_msg, **{"success": build_info.is_good(), "jenkinsNum": build_num, "jobName": job_name}}
        print(data)
        name = data.get(NAME_KEY)
        if name == 'Mapa2_Android_phone':  # android phone 逻辑

            BuildInfoController(data).write_build_info(android_phone_package_manager_server.models.BuildInfo,
                                                       Commit.ANDROID_PHONE_COMMIT_BASE_URI)
            ApkDetailInfoController(data).write_apk_detail_info(
                android_phone_package_manager_server.models.ApkDetailInfo)

        if name == 'Mapa2_ARM_MTK_xiaozhuo':
            BuildInfoController(data).write_build_info(mapa_package_manager_server.models.BuildInfo,
                                                       Commit.MAPA_COMMIT_BASE_URI)
            ApkDetailInfoController(data).write_apk_detail_info(mapa_package_manager_server.models.ApkDetailInfo)

            # data = JenkinsInfo(data).write_jenkins_info()

        return HttpResponse(FormatData.response_data(data=data))



