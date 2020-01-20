import os
from core.mysql_client import MysqlClient
from core.utils import Utils
from conf.constant_settings import SQL_COUNT_KEY, NONE_EXCEPTION, TEST_RUN_ID_KEY,TOTAL_IS_NONE


class Tests(object):

    def __init__(self, mysql_cursor: MysqlClient):
        self.mysql_cursor = mysql_cursor

    def query_tests(self, page: int, build_id: str, log):
        page_start, page_end = Utils.page_rule(page)
        sql_for_select_test_run_id = "SELECT a.test_run_id, b.uuid, b.android_version, " \
                                     "b.app_version, a.created_time, c.source " \
                                     "FROM build_and_test_info a " \
                                     "INNER JOIN build_description b ON a.build_id = b.build_id " \
                                     "INNER JOIN task_info c ON a.test_run_id=c.test_run_id " \
                                     "WHERE b.build_id = '%s'" \
                                     "ORDER BY a.created_time desc LIMIT  %d, %d;" % (build_id, page_start, page_end)
        print(sql_for_select_test_run_id)

        exception = None
        try:
            select_value_result = self.mysql_cursor.mysql_select_sql(sql_for_select_test_run_id)
            select_total_num = self._query_test_total_num(build_id, log)
            for i in range(len(select_value_result)):
                select_value_result[i] = dict(select_value_result[i],
                                              **self.query_test_total_info(select_value_result[i][TEST_RUN_ID_KEY], log))
            return Utils.sql_result_converted_to_json(select_value_result, select_total_num)
        except Exception as e:
            exception = e
        finally:
            location_of_error = NONE_EXCEPTION if exception is None \
                else "%s.%s" % (os.path.split(__file__)[-1], Utils.get__function_name())
            error_info = Utils.exception_to_str(exception)
            log.write_db_log(location_of_error, error_info, Utils.del_str_quotes(sql_for_select_test_run_id), log=log)

    def query_test_total_info(self, test_run_id, log):
        sql_for_select_test_total_info = "select process_total_num,process_pass_num,hardware_total_num," \
                                         "hardware_pass_num from test_result_total where test_run_id='%s'" % test_run_id
        exception = None
        try:
            test_total_info = self.mysql_cursor.mysql_select_sql(sql_for_select_test_total_info)
            if len(test_total_info) > 0:
                return test_total_info[0]
            return TOTAL_IS_NONE
        except Exception as e:
            exception = e
        finally:
            location_of_error = NONE_EXCEPTION if exception is None \
                else "%s.%s" % (os.path.split(__file__)[-1], Utils.get__function_name())
            error_info = Utils.exception_to_str(exception)
            log.write_db_log(location_of_error, error_info, Utils.del_str_quotes(sql_for_select_test_total_info), log=log)

    def _query_test_total_num(self, build_id, log):
        select_build_total_result_num = "SELECT COUNT(*) FROM task_info WHERE build_id = '%s'" % build_id
        exception = None
        try:
            return int(self.mysql_cursor.mysql_select_sql(select_build_total_result_num)[0][SQL_COUNT_KEY])
        except Exception as e:
            exception = e
        finally:
            location_of_error = NONE_EXCEPTION if exception is None \
                else "%s.%s" % (os.path.split(__file__)[-1], Utils.get__function_name())
            error_info = Utils.exception_to_str(exception)
            log.write_db_log(location_of_error, error_info,
                             Utils.del_str_quotes(select_build_total_result_num), log=log)

    def query_process(self, page: int, test_run_id: str, log):
        page_start, page_end = Utils.page_rule(page)
        sql = "SELECT * FROM process_test_result " \
              "WHERE test_run_id = '%s' " \
              "ORDER BY created_time desc " \
              "LIMIT  %d, %d;" % (test_run_id, page_start, page_end)
        exception = None
        try:
            select_value_result = self.mysql_cursor.mysql_select_sql(sql)
            select_total_num = self._query_process_total_num(test_run_id, log)
            return Utils.sql_result_converted_to_json(select_value_result, select_total_num)
        except Exception as e:
            exception = e
        finally:
            location_of_error = NONE_EXCEPTION if exception is None \
                else "%s.%s" % (os.path.split(__file__)[-1], Utils.get__function_name())
            error_info = Utils.exception_to_str(exception)
            log.write_db_log(location_of_error, error_info, Utils.del_str_quotes(sql), log=log)

    def _query_process_total_num(self, test_run_id, log):
        select_process_total_result_num = "SELECT COUNT(*) FROM process_test_result WHERE test_run_id = '%s'" \
                                          % test_run_id
        exception = None
        try:
            return int(self.mysql_cursor.mysql_select_sql(select_process_total_result_num)[0][SQL_COUNT_KEY])
        except Exception as e:
            exception = e
        finally:
            location_of_error = NONE_EXCEPTION if exception is None \
                else "%s.%s" % (os.path.split(__file__)[-1], Utils.get__function_name())
            error_info = Utils.exception_to_str(exception)
            log.write_db_log(location_of_error, error_info,
                             Utils.del_str_quotes(select_process_total_result_num), log=log)

    def query_hardware(self, page: int, test_run_id: str, log):
        page_start, page_end = Utils.page_rule(page)
        sql = "SELECT * FROM hardware_test_result " \
              "WHERE test_run_id = '%s' " \
              "ORDER BY created_time desc " \
              "LIMIT  %d, %d;" % (test_run_id, page_start, page_end)
        exception = None
        try:
            select_value_result = self.mysql_cursor.mysql_select_sql(sql)
            select_total_num = self._query_hardware_total_num(test_run_id,log)
            return Utils.sql_result_converted_to_json(select_value_result, select_total_num)
        except Exception as e:
            exception = e
        finally:
            location_of_error = NONE_EXCEPTION if exception is None \
                else "%s.%s" % (os.path.split(__file__)[-1], Utils.get__function_name())
            error_info = Utils.exception_to_str(exception)
            log.write_db_log(location_of_error, error_info, Utils.del_str_quotes(sql), log=log)

    def _query_hardware_total_num(self, test_run_id, log):
        select_hardware_total_result_num = "SELECT COUNT(*) FROM hardware_test_result WHERE test_run_id = '%s'"\
                                          % test_run_id
        exception = None
        try:
            return int(self.mysql_cursor.mysql_select_sql(select_hardware_total_result_num)[0][SQL_COUNT_KEY])
        except Exception as e:
            exception = e
        finally:
            location_of_error = NONE_EXCEPTION if exception is None \
                else "%s.%s" % (os.path.split(__file__)[-1], Utils.get__function_name())
            error_info = Utils.exception_to_str(exception)
            log.write_db_log(location_of_error, error_info,
                             Utils.del_str_quotes(select_hardware_total_result_num), log=log)

    def insert_test_total_result(self, test_run_id: str, log):
        """测试技术后，对这一次测试的结果计算，并插入对应数据库"""
        select_process_result_sql = "select * from process_test_result where test_run_id = '%s';" % test_run_id
        select_hardware_result_sql = "select * from hardware_test_result where test_run_id = '%s';" % test_run_id
        process_result = self.mysql_cursor.mysql_select_sql(select_process_result_sql)
        hardware_result = self.mysql_cursor.mysql_select_sql(select_hardware_result_sql)
        process_total_num = len(process_result)
        hardware_total_num = len(hardware_result)
        process_pass_num = 0
        hardware_pass_num = 0
        for i in process_result:
            if Tests._one_test_result_is_pass(i):
                process_pass_num += 1
        for i in hardware_result:
            if Tests._one_test_result_is_pass(i):
                hardware_pass_num += 1
        insert_result_total_sql = "insert into test_result_total (test_run_id, " \
                                  "process_total_num, " \
                                  "process_pass_num," \
                                  "hardware_total_num," \
                                  " hardware_pass_num," \
                                  "created_time) values ('%s', '%s', '%s', '%s', '%s', '%s')" % \
                                  (test_run_id,
                                   process_total_num,
                                   process_pass_num,
                                   hardware_total_num,
                                   hardware_pass_num,
                                   Utils.get_time())
        exception = None
        try:
            self.mysql_cursor.mysql_insert_or_update_sql(insert_result_total_sql)
        except Exception as e:
            exception = e
        finally:
            location_of_error = NONE_EXCEPTION if exception is None \
                else "%s.%s" % (os.path.split(__file__)[-1], Utils.get__function_name())
            error_info = Utils.exception_to_str(exception)
            log.write_db_log(location_of_error, error_info,
                             Utils.del_str_quotes(select_process_result_sql), test_run_id=test_run_id)
            log.write_db_log(location_of_error, error_info,
                             Utils.del_str_quotes(select_hardware_result_sql), test_run_id=test_run_id)
            log.write_db_log(location_of_error, error_info,
                             Utils.del_str_quotes(insert_result_total_sql), test_run_id=test_run_id)

    @classmethod
    def _one_test_result_is_pass(cls, one_result: dict):
        for value in one_result.values():
            if value in ('pass', 'true'):
                return True
        return False

