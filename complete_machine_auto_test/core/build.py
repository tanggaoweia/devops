import os
from core.utils import Utils
from core.mysql_client import MysqlClient
from conf.constant_settings import *
from core.task import Task


class Build(object):
    """build类"""

    def __init__(self, mysql_cursor: MysqlClient):
        self.mysql_cursor = mysql_cursor

    def query_builds(self, page: int, commit_id: str, log) -> dict:
        """查询commit id下面详细的build信息"""
        page_start, page_end = Utils.page_rule(page)

        sql_for_select_build_id = "SELECT build_id FROM commit_and_build_info " \
                                  "WHERE commit_id = '%s' ORDER BY created_time desc " \
                                  "LIMIT %d, %d;" % (commit_id, page_start, page_end)
        exception = None
        build_info = []
        try:
            select_build_id_result = self.mysql_cursor.mysql_select_sql(sql_for_select_build_id)
            print(select_build_id_result)
            for i in range(len(select_build_id_result)):
                build_info.append(self._query_build_info(select_build_id_result[i][BUILD_ID_KEY], log))
            print(build_info)
            select_total_num = self._query_build_total_num(commit_id, log)
            return Utils.sql_result_converted_to_json(build_info, select_total_num)
        except Exception as e:
            exception = e
        finally:
            location_of_error = NONE_EXCEPTION if exception is None \
                else "%s.%s" % (os.path.split(__file__)[-1], Utils.get__function_name())
            error_info = Utils.exception_to_str(exception)
            log.write_db_log(location_of_error, error_info, Utils.del_str_quotes(sql_for_select_build_id), log=log)

    def _query_build_total_num(self, commit_id, log):
        """查询commit id 下面有多少个build"""
        select_build_total_result_num = "SELECT COUNT(*) FROM commit_and_build_info WHERE commit_id = '%s'" % commit_id
        exception = None
        try:
            return int(self.mysql_cursor.mysql_select_sql(select_build_total_result_num)[0][SQL_COUNT_KEY])
        except Exception as e:
            exception = e
        finally:
            location_of_error = NONE_EXCEPTION if exception is None \
                else "%s.%s" % (os.path.split(__file__)[-1], Utils.get__function_name())
            error_info = Utils.exception_to_str(exception)
            log.write_db_log(location_of_error, error_info, Utils.del_str_quotes(select_build_total_result_num),
                             log=log)

    def _query_build_info(self, build_id, log):
        """传入build id，查询这一个build id的详细信息"""
        sql_for_select_apk_path = "select apk_path, type from apk_info where build_id = '%s'" % build_id
        sql_for_select_build_info = "select build_id, build_author, build_method, created_time from build_description " \
                                    "where build_id = '%s'" % build_id
        exception = None
        try:
            # 查询 apk_path
            select_apk_path_value = self.mysql_cursor.mysql_select_sql(sql_for_select_apk_path)

            # 查询build_info
            select_build_info_value = self.mysql_cursor.mysql_select_sql(sql_for_select_build_info)

            apk_path, result = {}, {}
            for i in select_apk_path_value:
                apk_path[i[TYPE_KEY]] = i[APK_PATH_KEY]
            result[APK_PATH_KEY] = apk_path

            # 两条查询的结果，连接到一起
            result = dict(select_build_info_value[0], **result)
            return result
        except Exception as e:
            print(e)
            exception = e
        finally:
            location_of_error = NONE_EXCEPTION if exception is None \
                else "%s.%s" % (os.path.split(__file__)[-1], Utils.get__function_name())
            error_info = Utils.exception_to_str(exception)
            log.write_db_log(location_of_error, error_info,
                             Utils.del_str_quotes(sql_for_select_apk_path), log=log)
            log.write_db_log(location_of_error, error_info,
                             Utils.del_str_quotes(sql_for_select_build_info), log=log)

    def write_build_info_to_database(self, build_info: dict, log):
        """记录每次build成功后的build信息"""
        build_id = build_info[BUILD_ID_KEY]
        commit_id = build_info[COMMIT_ID_KEY]
        test_run_id = build_info[TEST_RUN_ID_KEY]
        build_author = build_info[BUILD_AUTHOR_KEY]
        commit_author = build_info[COMMIT_AUTHOR_KEY]
        link_work_item = build_info[LINK_WORK_ITEMS_KEY]
        apk_path = build_info[APK_PATH_KEY]
        branch_name = build_info[BRANCH_NAME_KEY]
        commit_msg = build_info[COMMIT_MSG_KEY]
        build_method = build_info[BUILD_METHOD_KEY]
        apk_type = build_info[TYPE_KEY]
        source = build_info[SOURCE_KEY]
        sql_for_insert_apk_info = "insert into apk_info (" \
                                  "build_id, " \
                                  "apk_path, " \
                                  "type," \
                                  "created_time," \
                                  "update_time) values ('%s', '%s', '%s', '%s', '%s');" % \
                                  (build_id,
                                   apk_path,
                                   apk_type,
                                   Utils.get_time(),
                                   Utils.get_time())
        sql_for_insert_build_and_test_info = "insert into build_and_test_info" \
                                             "(build_id, test_run_id, created_time) values ('%s', '%s', '%s');" \
                                             % (build_id, test_run_id, Utils.get_time())

        sql_for_insert_commit_and_build_info = "insert into commit_and_build_info" \
                                               "(commit_id, build_id, created_time) values ('%s', '%s', '%s');" \
                                               % (commit_id, build_id, Utils.get_time())
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
                                            Utils.get_time())

        select_for_builds_is_exist = " select * from apk_info where build_id = '%s'" % build_id
        exception = None
        select_build_info = None
        try:
            select_build_info = self.mysql_cursor.mysql_select_sql(select_for_builds_is_exist)
            self.mysql_cursor.mysql_insert_or_update_sql(sql_for_insert_apk_info)
            self.mysql_cursor.mysql_insert_or_update_sql(sql_for_insert_build_and_test_info)
            if len(select_build_info) == 0:
                self.mysql_cursor.mysql_insert_or_update_sql(sql_for_insert_commit_and_build_info)
                self.mysql_cursor.mysql_insert_or_update_sql(sql_for_insert_build_description)
            if TASK_APK_TYPE == apk_type:
                Task(build_id, source, self.mysql_cursor, log).write_task_info_to_database(test_run_id)
        except Exception as e:
            exception = e
        finally:
            location_of_error = NONE_EXCEPTION if exception is None \
                else "%s.%s" % (os.path.split(__file__)[-1], Utils.get__function_name())
            error_info = Utils.exception_to_str(exception)
            log.write_db_log(location_of_error, error_info,
                             Utils.del_str_quotes(sql_for_insert_apk_info), log=log)
            if len(select_build_info) == 0:
                log.write_db_log(location_of_error, error_info,
                                 Utils.del_str_quotes(sql_for_insert_build_and_test_info), log=log)
                log.write_db_log(location_of_error, error_info,
                                 Utils.del_str_quotes(sql_for_insert_commit_and_build_info), log=log)
                log.write_db_log(location_of_error, error_info,
                                 Utils.del_str_quotes(sql_for_insert_build_description), log=log)

    @classmethod
    def get_build_method(cls):
        """获得build的方式 AUTO OR MANUAL"""
        return " "



