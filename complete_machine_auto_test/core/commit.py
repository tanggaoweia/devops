import requests
import os
from core.utils import Utils
from core.mysql_client import MysqlClient
from conf.constant_settings import SQL_COUNT_KEY, TOKEN, COMMIT_BASE_URI, NONE_EXCEPTION


class Commit(object):

    SELECT_COMMIT_TOTAL_RESULT_NUM = "SELECT COUNT(*) FROM commit_and_build_info;"

    def __init__(self, page, mysql_cursor: MysqlClient):
        self.page = page
        self.mysql_cursor = mysql_cursor

    def query_commits(self, log) -> dict:
        """查询总的commit信息"""
        page_start, page_end = Utils.page_rule(self.page)
        sql = "SELECT DISTINCT(a.commit_id),a.created_time,c.commit_msg,c.commit_author,c.linked_work_item,c.branch " \
              "FROM commit_and_build_info a " \
              "INNER JOIN build_and_test_info b ON a.build_id = b.build_id " \
              "INNER JOIN build_description c ON b.build_id = c.build_id  " \
              "ORDER BY a.created_time desc " \
              "LIMIT %d, %d;" % (page_start, page_end)
        exception = None
        try:
            select_value_result = self. mysql_cursor.mysql_select_sql(sql)
            select_total_num = self._query_commit_total_num()
            return Utils.sql_result_converted_to_json(select_value_result, select_total_num)
        except Exception as e:
            exception = e
        finally:
            location_of_error = NONE_EXCEPTION if exception is None \
                else "%s.%s" % (os.path.split(__file__)[-1], Utils.get__function_name())
            error_info = Utils.exception_to_str(exception)
            log.write_db_log(location_of_error, error_info, Utils.del_str_quotes(sql), log=log)

    def _query_commit_total_num(self):
        return int(self.mysql_cursor.mysql_select_sql(Commit.SELECT_COMMIT_TOTAL_RESULT_NUM)[0][SQL_COUNT_KEY])

    @staticmethod
    def _get_commit_info(commit_id):
        """获得commit作者"""
        auth = ("", TOKEN)
        uri = COMMIT_BASE_URI + commit_id
        params = {'api-version': 5.0}
        r = requests.get(uri, params=params, auth=auth, verify=False)
        return r.json()

    @classmethod
    def get_commit_author(cls, commit_id) -> str:
        return Commit._get_commit_info(commit_id)['author']['email']

    @classmethod
    def get_commit_msg(cls, commit_id) -> str:
        return Commit._get_commit_info(commit_id)['comment']

    @classmethod
    def get_link_work_item(cls):
        return " "

    def query_select_info(self, select_info):
        """搜索框内容查询"""
        page_start, page_end = Utils.page_rule(self.page)
        sql = "SELECT DISTINCT(a.commit_id),a.created_time,c.commit_msg,c.commit_author,c.linked_work_item,c.branch " \
              "FROM commit_and_build_info a " \
              "INNER JOIN build_and_test_info b ON a.build_id = b.build_id " \
              "INNER JOIN build_description c ON b.build_id = c.build_id  " \
              "WHERE (a.commit_id like '%%%s%%') or (c.commit_author like '%%%s%%')" \
              "ORDER BY a.created_time desc " \
              "LIMIT %d, %d;" % (select_info, select_info, page_start, page_end)

        select_value_result = self.mysql_cursor.mysql_select_sql(sql)
        select_total_num = self._query_select_total_num(select_info)
        return Utils.sql_result_converted_to_json(select_value_result, select_total_num)

    def _query_select_total_num(self, select_info: str):
        if select_info.isalpha() and len(select_info) > 5:
            sql = "SELECT COUNT(*) FROM build_description WHERE  commit_author like '%%%s%%'" % select_info
        else:
            sql = "SELECT COUNT(*) FROM commit_and_build_info WHERE commit_id like '%%%s%%';" % select_info
        return int(self.mysql_cursor.mysql_select_sql(sql)[0][SQL_COUNT_KEY])
