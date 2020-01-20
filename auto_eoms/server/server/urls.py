"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url

from dl_model_manager.dl_model_manager import DLModelManager
from dl_model_manager.models import ModelsAndNetworksInfo
from jenkins_server import views
from http_server import views as view
from dl_model_manager import views as algorithm_manager
from apscheduler.scheduler import Scheduler


from android_phone_package_manager_server import views as android_phone_package_manager_server
from mapa_package_manager_server import views as mapa_package_manager_server

urlpatterns = [
    path('admin/', admin.site.urls),
    url('^jenkins$', views.jenkins_info),  # jenkins 打包完成后信息通知

    url('^download_apk$', view.download_apk),  # 下载apk
    url('^v1/download_apk$', view.download_apk),  # 下载apk

    url('^dl_model_manager/models_and_networks_upload$', algorithm_manager.models_and_networks_upload),  # 模型和网络上传
    url('^dl_model_manager/models_and_networks_data$', algorithm_manager.models_and_networks_flops_data),# 模型和网络数据结果保存（针对某一个具体的网络模型）
    url('^dl_model_manager/flops_script_sign$', algorithm_manager.models_and_networks_flops_script_sign),  # 跑算力脚本
    url('^dl_model_manager/full_info$', algorithm_manager.models_and_networks_full_info),  # 获得模型和网络数据

    url('^v1/android_phone/manual_pull_info$', android_phone_package_manager_server.manual_pull_info),  # 手动拉取最新的 android phone pullRequest信息
    url('^v1/android_phone/table_info_where_pull_request_id_is_not_zero$', android_phone_package_manager_server.query_table_info_where_triggered_by_pull_request),  # pull request 信息存在时，页面加载表格信息查询
    url('^v1/android_phone/table_info_where_pull_request_id_is_zero$', android_phone_package_manager_server.query_table_info_where_not_triggered_by_pull_request),  # pull request 信息不存在时，页面加载表格信息查询
    url('^v1/android_phone/update_test_result$', android_phone_package_manager_server.update_test_result),  # 更新测试结果
    url('^v1/android_phone/update_description$', android_phone_package_manager_server.update_description),  # 更新测试备注
    url('^v1/android_phone/update_sign$', android_phone_package_manager_server.update_sign),  # 更新打标信息
    url('^v1/android_phone/pull_request_info_of_month$', android_phone_package_manager_server.query_pull_request_info_of_month),  # 获得特定时间一个月内的 pull request 信息
    url('^v1/android_phone/cancel_sign$', android_phone_package_manager_server.cancel_sign),  # 取消打标信息
    url('^v1/android_phone/test_report$', android_phone_package_manager_server.upload_test_report),  # 上传测试报告
    url('^v1/android_phone/market_table_info$', android_phone_package_manager_server.query_market_table_info),  # 市场部表格数据获取
    url('^v1/android_phone/update_market_desc$', android_phone_package_manager_server.update_market_desc),  # 更新市场备注
    url('^v1/android_phone/sign_pull_request_info$', android_phone_package_manager_server.sign_pull_request_info),  # 查看打标的 pull request 信息
    url('^v1/android_phone/market_test_report$', android_phone_package_manager_server.query_market_test_report),  # 查看测试报告
    url('^v1/android_phone/download_test_report$', android_phone_package_manager_server.download_test_report),  # 下载测试报告
    url('^v1/android_phone/del_test_report$', android_phone_package_manager_server.del_test_report),  # 删除测试报告

    url('^v1/mapa/manual_pull_info$', mapa_package_manager_server.manual_pull_info),  # 手动拉取最新的 mapa pullRequest信息
    url('^v1/mapa/table_info_where_pull_request_id_is_not_zero$', mapa_package_manager_server.query_table_info_where_triggered_by_pull_request),  # pull request 信息存在时，页面加载表格信息查询
    url('^v1/mapa/table_info_where_pull_request_id_is_zero$', mapa_package_manager_server.query_table_info_where_not_triggered_by_pull_request),  # pull request 信息不存在时，页面加载表格信息查询
    url('^v1/mapa/update_test_result$', mapa_package_manager_server.update_test_result),  # 更新测试结果
    url('^v1/mapa/update_description$', mapa_package_manager_server.update_description),  # 更新测试备注
    url('^v1/mapa/update_sign$', mapa_package_manager_server.update_sign),  # 更新打标信息
    url('^v1/mapa/pull_request_info_of_month$', mapa_package_manager_server.query_pull_request_info_of_month),  # 获得特定时间一个月内的 pull request 信息
    url('^v1/mapa/cancel_sign$', mapa_package_manager_server.cancel_sign),  # 取消打标信息
    url('^v1/mapa/test_report$', mapa_package_manager_server.upload_test_report),  # 上传测试报告
    url('^v1/mapa/market_table_info$', mapa_package_manager_server.query_market_table_info),  # 市场部表格数据获取
    url('^v1/mapa/update_market_desc$', mapa_package_manager_server.update_market_desc),  # 更新市场备注
    url('^v1/mapa/sign_pull_request_info$', mapa_package_manager_server.sign_pull_request_info),  # 查看打标的 pull request 信息
    url('^v1/mapa/market_test_report$', mapa_package_manager_server.query_market_test_report),  # 查看测试报告
    url('^v1/mapa/download_test_report$', mapa_package_manager_server.download_test_report),  # 下载测试报告
    url('^v1/mapa/del_test_report$', mapa_package_manager_server.del_test_report),  # 删除测试报告

]

scheduler = Scheduler()  # 实例化，固定格式


# @scheduler.cron_schedule(hour='23', day='*')  # 装饰器，每天23点运行
# def cron_job():
#     run()


def run_flops_script():     # flops 脚本，每隔五分钟查询一次
    DLModelManager.batch_run_flops_script(ModelsAndNetworksInfo)


scheduler.add_interval_job(run_flops_script, minutes=5)

scheduler.start()  # 启动该脚本
