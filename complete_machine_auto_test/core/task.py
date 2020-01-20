import os
import uuid
from core.mysql_client import MysqlClient
from core.utils import Utils
from conf.constant_settings import TASK_APK_TYPE, NONE_EXCEPTION


class Task(object):

    SQL_FOR_SELECT_AN_EXECUTABLE_TASK = "SELECT a.build_id, a.apk_path, b.test_run_id " \
                                        "FROM apk_info a INNER JOIN task_info b ON a.build_id = b.build_id " \
                                        "WHERE b.status = '0' AND a.type='%s' " \
                                        "ORDER BY a.created_time LIMIT 1;" % TASK_APK_TYPE

    def __init__(self, build_id, source, mysql_cursor: MysqlClient, log):
        self.build_id = build_id
        self.source = source
        self.mysql_cursor = mysql_cursor
        self.log = log
        self.test_run_id = Task.get_test_run_id()
        self.type = TASK_APK_TYPE

    def write_task_info_to_database(self, test_run_id=None, is_manual=False):
        test_run_id = self.test_run_id if test_run_id is None else test_run_id
        sql_for_insert_task_info = "insert into task_info(build_id,test_run_id,source,type,created_time,update_time)" \
                                   "values('%s', '%s', '%s','%s','%s','%s')" % \
                                   (self.build_id,
                                    test_run_id,
                                    self.source,
                                    self.type,
                                    Utils.get_time(),
                                    Utils.get_time())
        sql_for_insert_build_and_test_info = "insert into build_and_test_info ( build_id, test_run_id, created_time)" \
                                             "values ('%s', '%s', '%s')" % (self.build_id, test_run_id,Utils.get_time())
        exception = None
        try:
            self.mysql_cursor.mysql_insert_or_update_sql(sql_for_insert_task_info)
            if is_manual:
                self.mysql_cursor.mysql_insert_or_update_sql(sql_for_insert_build_and_test_info)
        except Exception as e:
            exception = e
        finally:
            location_of_error = NONE_EXCEPTION if exception is None \
                else "%s.%s" % (os.path.split(__file__)[-1], Utils.get__function_name())
            error_info = Utils.exception_to_str(exception)
            self.log.write_db_log(location_of_error, error_info, Utils.del_str_quotes(sql_for_insert_task_info),
                                  log=self.log)
            self.log.write_db_log(location_of_error, error_info, Utils.del_str_quotes(
                sql_for_insert_build_and_test_info), log=self.log)

    @classmethod
    def get_test_run_id(cls):
        return str(uuid.uuid4())

    @classmethod
    def get_an_executable_task(cls, mysql_cursor: MysqlClient):
        """获得一条可执行的任务"""
        return mysql_cursor.mysql_select_sql(Task.SQL_FOR_SELECT_AN_EXECUTABLE_TASK)

    @classmethod
    def update_task_status(cls, mysql_cursor, test_run_id):
        """更新任务状态和时间"""
        update_task_status_sql = "update task_info set status = '1', update_time = '%s' where test_run_id = '%s' ;" % \
                                 (Utils.get_time(), test_run_id)
        mysql_cursor.mysql_insert_or_update_sql(update_task_status_sql)
