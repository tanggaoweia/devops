import os

from http_server.commit import Commit
from http_server.test_run import TestRun
from http_server.task import Task
from utils.constant_key import *
from utils.mysql_client import MysqlClient
from utils.time_utils import TimeUtils


class JenkinsInfo:
    """
    jenkins build msg
    """
    _JENKINS_INFO_KEYS = ('commitId', 'branch', 'requestedForEmail', 'buildId', 'sourceBranch',
                          'targetBranch', 'jobName', 'name', 'buildNumber')

    def __init__(self, data):
        self.mysql_client = MysqlClient()
        self._data = data
        print(self._data)
        self._commit_id = data.get(JenkinsInfo._JENKINS_INFO_KEYS[0])
        self._branch_name = data.get(JenkinsInfo._JENKINS_INFO_KEYS[1])
        self._build_author = data.get(JenkinsInfo._JENKINS_INFO_KEYS[2])
        self._build_id = data.get(JenkinsInfo._JENKINS_INFO_KEYS[3]) + '--' + self._commit_id
        self._build_number = data.get(JenkinsInfo._JENKINS_INFO_KEYS[-1])
        self._job_name = data.get(JenkinsInfo._JENKINS_INFO_KEYS[-3]).split('_')[-1]
        self._source_branch = data.get(JenkinsInfo._JENKINS_INFO_KEYS[4]).split('/')[-1]
        self._target_branch = data.get(JenkinsInfo._JENKINS_INFO_KEYS[-4]).split('/')[-1]
        self._common_path_header = '/home/sh-ws-dispatch/releasewindows'
        self._apk_common_path = '{}/{}/{}/{}@{}@{}@{}@{}@{}/'.format(
            self._common_path_header,
            self._build_number.split('.')[0],
            self._data.get(JenkinsInfo._JENKINS_INFO_KEYS[-2]),
            self._branch_name,
            self._build_author.split('@')[0],
            self._source_branch,
            self._target_branch,
            self._build_number,
            self._commit_id
        )
        self._pull_request_id = data.get(PULL_REQUEST_ID_KEY)
        self._jenkins_info = {
            DATA_KEY: self._data,
            BUILD_ID_KEY: self._build_id,
            COMMIT_ID_KEY: self._commit_id,
            BUILD_AUTHOR_KEY: self._build_author,
            BRANCH_NAME_KEY: self._branch_name,
            APK_COMMON_PATH_KEY: self._apk_common_path,
            PULL_REQUEST_ID_KEY: self._pull_request_id
        }

    def get_jenkins_info(self):
        job_name = self._job_name
        print(job_name)
        self._jenkins_info[APK_PATH_KEY] = self._jenkins_info[APK_COMMON_PATH_KEY]
        apk_type = 1
        if job_name == 'iautotest':
            apk_type = 2
            self._jenkins_info[APK_PATH_KEY] = self._jenkins_info[APK_COMMON_PATH_KEY] + job_name + '/' \
                                               + os.listdir(self._jenkins_info[APK_COMMON_PATH_KEY] + job_name)[0]
        if job_name == 'debug':
            apk_type = 3
        if job_name == 'itest':
            apk_type = 4
        self._jenkins_info[APK_TYPE_KEY] = apk_type
        return self._jenkins_info

    def write_jenkins_info(self, source='jenkins', build_method='auto'):
        self.get_jenkins_info()
        build_id = self._jenkins_info.get(BUILD_ID_KEY)
        commit_id = self._jenkins_info.get(COMMIT_ID_KEY)
        test_run_id = TestRun.get_test_run_id()
        build_author = self._jenkins_info.get(BUILD_AUTHOR_KEY)
        commit_author = Commit.get_commit_author(commit_id)
        link_work_item = Commit.get_link_work_item()
        apk_path = self._jenkins_info.get(APK_PATH_KEY)
        branch_name = self._jenkins_info.get(BRANCH_NAME_KEY)
        commit_msg = Commit.get_commit_msg(commit_id)
        apk_type = self._jenkins_info.get(APK_TYPE_KEY)
        pull_request_id = self._jenkins_info.get(PULL_REQUEST_ID_KEY)
        print("pull_request_id", pull_request_id)
        sql_for_insert_apk_info = "insert into apk_info (" \
                                  "build_id, " \
                                  "apk_path, " \
                                  "type," \
                                  "pull_request_id," \
                                  "created_time," \
                                  "update_time) values ('%s', '%s', '%s', %d,'%s', '%s');" % \
                                  (build_id,
                                   apk_path,
                                   apk_type,
                                   int(pull_request_id),
                                   TimeUtils.get_time(),
                                   TimeUtils.get_time())
        sql_for_insert_build_and_test_info = "insert into build_and_test_info" \
                                             "(build_id, test_run_id, created_time) values ('%s', '%s', '%s');" \
                                             % (build_id, test_run_id, TimeUtils.get_time())

        sql_for_insert_commit_and_build_info = "insert into commit_and_build_info" \
                                               "(commit_id, build_id, created_time) values ('%s', '%s', '%s');" \
                                               % (commit_id, build_id, TimeUtils.get_time())
        sql_for_insert_build_description = "insert into build_description(" \
                                           "build_id, " \
                                           "commit_msg, " \
                                           "commit_author, " \
                                           "build_author," \
                                           "linked_work_item," \
                                           "branch," \
                                           "build_method," \
                                           "created_time) values ('%s', '%s', '%s','%s','%s','%s','%s','%s');" % \
                                           (build_id,
                                            commit_msg,
                                            commit_author,
                                            build_author,
                                            link_work_item,
                                            branch_name,
                                            build_method,
                                            TimeUtils.get_time())
        select_for_builds_is_exist = " select * from apk_info where build_id = '%s'" % build_id
        select_build_info = self.mysql_client.mysql_select(select_for_builds_is_exist)
        print(1, sql_for_insert_apk_info)
        self.mysql_client.mysql_insert_update_delete(sql_for_insert_apk_info)
        print(2, sql_for_insert_build_and_test_info)
        self.mysql_client.mysql_insert_update_delete(sql_for_insert_build_and_test_info)

        if len(select_build_info) == 0:
            self.mysql_client.mysql_insert_update_delete(sql_for_insert_commit_and_build_info)
            self.mysql_client.mysql_insert_update_delete(sql_for_insert_build_description)
        if Task.TASK_APK_TYPE == apk_type:
            Task(build_id, source, self.mysql_client).write_task_info_to_database(test_run_id)
        return self.get_jenkins_info()




# if __name__ == '__main__':
#
#     data1 = {'repo': 'https://ws-tfs-01/tfs/sh-ws-office/Mapa/_git/Mapa2_ARM_MTK_xiaozhuo',
#             'commitId': '65ccf14f3c97788c0446653ee2e086d79b8d9754', 'name': 'Mapa2_ARM_MTK_xiaozhuo',
#              'branch': 'merge', 'requestedFor': '李丁', 'requestedForEmail': 'wsliding@sunnyoptical.com',
#              'buildId': '2142', 'buildNumber': '20191203.6', 'queuedById': '000007f5-0000-8888-8000-000000000000',
#              'queuedBy': 'Microsoft.TeamFoundation.System', 'requestedForId': '1418052c-b72d-4ac1-9c58-e2f7c925a5dc',
#              'sourceBranch': 'refs/heads/dev_ZheJiang_PutOnRecord-on-feature-hobot-1.9.8-Maliang-on-feature',
#              'targetBranch': 'refs/heads/feature', 'success': True, 'jenkinsNum': '779',
#              'jobName': 'Mapa2_ARM_MTK_xiaozhuo_iautotest'}
#
#     print(JenkinsInfo(data1).write_jenkins_info())
