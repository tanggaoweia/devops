import sys
import os
from core.process import Process
from core.utils import Utils
from core.log import Log
from conf.constant_settings import NONE_EXCEPTION


class TestProcess(object):

    MAPA_PROCESS_NAME = 'com.wissen.mapa'
    TEST_RESULT_SUCCESS = 'pass'
    TEST_RESULT_FAILED = 'fail'

    def __init__(self, test_run_id, mysql_cursor, loop_num):
        self.test_run_id = test_run_id
        self.mysql_cursor = mysql_cursor
        self.loop_num = loop_num
        self.record = Record()
        self.process = Process()
        self._test_process_log_key = 'process test is complete'
        self._test_process_log_value = ' is completed'

    def test_runner(self, log):
        try:
            for i in range(self.loop_num):
                self._mapa_process_restart_test()
                self._write_test_result(log)
            Log.write_operation_log(self.mysql_cursor,
                                      self.test_run_id,
                                      self._test_process_log_key,
                                      self._test_process_log_value,
                                      is_error=False)
        except Exception as e:
            error_key = sys._getframe().f_code.co_name
            Log.write_operation_log(self.mysql_cursor, self.test_run_id, error_key, Utils.del_str_quotes(str(e)))

    def _write_test_result(self, log):
        test_process_result_sql = "insert into process_test_result (test_run_id,mapa_restarted_success,created_time)" \
                                  "values ('%s', '%s', '%s')" % \
                                  (self.test_run_id, self.record.mapa_restart_success, Utils.get_time())
        exception = None
        try:
            self.mysql_cursor.mysql_insert_or_update_sql(test_process_result_sql)
        except Exception as e:
            exception = e
        finally:
            location_of_error = NONE_EXCEPTION if exception is None \
                else "%s.%s" % (os.path.split(__file__)[-1], Utils.get__function_name())
            error_info = Utils.exception_to_str(exception)
            log.write_db_log(location_of_error, error_info,
                             Utils.del_str_quotes(test_process_result_sql), test_run_id=self.test_run_id)

    def _mapa_process_restart_test(self):
        """case 主进程重启"""
        before_restart_status = self.process.get_process_status(self.MAPA_PROCESS_NAME)
        if before_restart_status == 'F':
            self.record.mapa_restart_success = self.TEST_RESULT_FAILED
        else:
            self.process.kill_process(self.MAPA_PROCESS_NAME)
            after_restart_status = self.process.get_process_status(self.MAPA_PROCESS_NAME)
            if before_restart_status == after_restart_status:
                self.record.mapa_restart_success = self.TEST_RESULT_SUCCESS
            else:
                self.record.mapa_restart_success = self.TEST_RESULT_FAILED


class Record(object):

    def __init(self):
        self.mapa_restart_success = ''

