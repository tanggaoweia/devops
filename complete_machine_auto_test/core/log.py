import uuid
from core.utils import Utils
from conf.constant_settings import \
    REQUEST_FOR_DB_RECORD_ID_TYPE, TEST_RUN_FOR_DB_RECORD_ID_TYPE


class Log(object):

    def __init__(self, mysql_cursor):
        self.log_id = self._get_log_id()
        self.mysql_cursor = mysql_cursor

    @classmethod
    def _get_log_id(cls):
        return str(uuid.uuid4())

    @classmethod
    def write_operation_log(cls, mysql_cursor,
                            test_run_id,
                            operation_key,
                            operation_value,
                            is_error=True, ):
        print(test_run_id)
        """记录操作日志"""
        write_log_sql = "insert into operation_log(test_run_id,is_error,operation_key,operation_value,created_time)" \
                        "values('%s','%s','%s', '%s', '%s')" % \
                        (test_run_id, is_error, operation_key, operation_value, Utils.get_time())
        mysql_cursor.mysql_insert_or_update_sql(write_log_sql)

    def write_request_log(self, location_of_error, error_info, url_info, method, params, headers):
        write_request_log_sql = """insert into request_log(
        request_id, location_of_error, error_info, url_info,method, params, created_time, headers) 
        values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" % \
         (self.log_id, location_of_error, error_info, url_info, method, params, Utils.get_time(), headers)
        self.mysql_cursor.mysql_insert_or_update_sql(write_request_log_sql)

    def write_db_log(self, location_of_error, error_info, sql_info, test_run_id=None, log=None):
        db_record_id = log.log_id if test_run_id is None else test_run_id
        db_record_id_type = REQUEST_FOR_DB_RECORD_ID_TYPE if test_run_id is None else TEST_RUN_FOR_DB_RECORD_ID_TYPE
        write_db_log_sql = "insert into db_log(db_record_id, db_record_id_type, location_of_error, error_info, " \
                           "sql_info, created_time) values('%s', '%s', '%s', '%s', '%s', '%s')" % \
                           (db_record_id, db_record_id_type, location_of_error, error_info, sql_info, Utils.get_time())
        self.mysql_cursor.mysql_insert_or_update_sql(write_db_log_sql)