from http_server.test_run import TestRun
from utils.mysql_client import MysqlClient
from utils.time_utils import TimeUtils


class Task(object):

    TASK_APK_TYPE = 2  # 需要执行任务的type

    def __init__(self, build_id, source, mysql_client: MysqlClient):
        self.build_id = build_id
        self.source = source
        self.mysql_client = mysql_client
        self.test_run_id = TestRun.get_test_run_id()
        self.type = self.TASK_APK_TYPE

    def write_task_info_to_database(self, test_run_id=None, is_manual=False):
        test_run_id = self.test_run_id if test_run_id is None else test_run_id
        sql_for_insert_task_info = "insert into task_info(build_id,test_run_id,source,type,created_time,update_time)" \
                                   "values('%s', '%s', '%s','%s','%s','%s')" % \
                                   (self.build_id,
                                    test_run_id,
                                    self.source,
                                    self.type,
                                    TimeUtils.get_time(),
                                    TimeUtils.get_time())
        sql_for_insert_build_and_test_info = "insert into build_and_test_info ( build_id, test_run_id, created_time)" \
                                             "values ('%s', '%s', '%s')" % (
                                             self.build_id, test_run_id, TimeUtils.get_time())

        self.mysql_client.mysql_insert_update_delete(sql_for_insert_task_info)
        if is_manual:
            self.mysql_client.mysql_insert_update_delete(sql_for_insert_build_and_test_info)


