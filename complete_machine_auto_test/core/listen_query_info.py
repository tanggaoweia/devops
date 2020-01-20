"""build消息通知 result结果查询"""
import simplejson
import json
import os
import re
from wsgiref.simple_server import make_server
from webob import Request, Response, dec, exc
from core.mysql_client import MysqlClient
from core.commit import Commit
from core.build import Build
from core.test_software import TestSoftware
from core.tests import Tests
from core.utils import Utils
from core.log import Log
from conf.constant_settings import *
from core.test_hardware import TestHardware
from core.task import Task


class Application:

    ROUTETABLE = {}

    @staticmethod
    def not_found(request: Request):
        """请求路径不存在"""
        res = Response()
        res.status_code = 404
        res.body = 'Not found'.encode()
        return res

    @classmethod
    def register(cls, path):
        def _register(handler):
            cls.ROUTETABLE[path] = handler
            return handler
        return _register

    @dec.wsgify
    def __call__(self, request) -> Response:
        return self.ROUTETABLE.get(request.path, self.not_found)(request)

    @classmethod
    def get_request_params(cls, request: Request) -> dict:
        """请求的参数解析，返回键值对"""
        try:
            params_key_value_format = {}
            request_method = request.method
            if request_method == 'GET':
                params = request.params.items()
                for i in params:
                    params_key_value_format[i[0]] = i[1]
            if request_method == 'POST':
                params = request.json
                for i in params:
                    params_key_value_format[i] = params[i]
            return params_key_value_format
        except simplejson.errors.JSONDecodeError as ei:
            print(111, ei)
        except Exception as ex:
            print(ex)

    @classmethod
    def response_json(cls, params: dict):
        response_headers = [('Content-type', 'application/json'),
                            ('Access-Control-Allow-Origin', '*'),
                            ('Access-Control-Allow-Methods', 'GET'),
                            ('Access-Control-Allow-Headers', 'x-requested-with,content-type'),
                            ]
        return Response(json.dumps(params).encode(encoding='utf-8'), headerlist=response_headers)

    @classmethod
    def get_url(cls, request: Request):
        return request.url

    @classmethod
    def get_method(cls, request: Request):
        return request.method

    @classmethod
    def get_headers(cls, request: Request):
        headers = {}
        for i in request.headers.items():
            headers[i[0]] = i[1]
        return headers

    @classmethod
    def get_query_info_params(cls, request: Request):
        params = Application.get_request_params(request)
        if PAGE_NUM_KEY in params.keys() and params[PAGE_NUM_KEY].isdigit():
            page_num = int(params[PAGE_NUM_KEY])
        else:
            page_num = 1
        cid_value = params[COMMIT_ID_KEY] if COMMIT_ID_KEY in params.keys() else None
        bid_value = params[BUILD_ID_KEY] if BUILD_ID_KEY in params.keys() else None
        tid_value = params[TEST_RUN_ID_KEY] if TEST_RUN_ID_KEY in params.keys() else None
        return {PAGE_NUM_KEY: page_num, COMMIT_ID_KEY: cid_value, BUILD_ID_KEY: bid_value, TEST_RUN_ID_KEY: tid_value}

    @classmethod
    def get_test_info_all(cls, request: Request):
        try:
            params = Application.get_request_params(request)
            if BUILD_ID_KEY in params.keys() and \
                    COMMIT_ID_KEY in params.keys() and \
                    BUILD_AUTHOR_KEY in params.keys() and \
                    APK_PATH_KEY in params.keys() and \
                    BRANCH_NAME_KEY in params.keys() and \
                    TYPE_KEY in params.keys():
                bid_value = params[BUILD_ID_KEY] + '--' + params[COMMIT_ID_KEY]
                cid_value = params[COMMIT_ID_KEY]
                b_author_value = params[BUILD_AUTHOR_KEY]
                apk_path_value = params[APK_PATH_KEY]
                bch_value = params[BRANCH_NAME_KEY]
                apk_type_value = params[TYPE_KEY]
                source_value = params[SOURCE_KEY] if SOURCE_KEY in params.keys() else SOURCE_DEFAULT_VALUE
                commit_msg = Commit.get_commit_msg(cid_value)
                commit_author = Commit.get_commit_author(cid_value)
                link_work_item = Commit.get_link_work_item()
                branch_method = Build.get_build_method()
                test_run_id = Task.get_test_run_id()
            else:
                raise IndexError
            return {COMMIT_ID_KEY: cid_value,
                    BUILD_ID_KEY: bid_value,
                    BUILD_AUTHOR_KEY: b_author_value,
                    APK_PATH_KEY: apk_path_value,
                    TYPE_KEY: apk_type_value,
                    BRANCH_NAME_KEY: bch_value,
                    COMMIT_MSG_KEY: commit_msg,
                    COMMIT_AUTHOR_KEY: commit_author,
                    LINK_WORK_ITEMS_KEY: link_work_item,
                    TEST_RUN_ID_KEY: test_run_id,
                    BUILD_METHOD_KEY: branch_method,
                    SOURCE_KEY: source_value
                    }
        except IndexError as ie:
            print(ie)
        except Exception as ex:
            print(ex)


def write_request_log_common_operation(request, log: Log, exception, location_of_error):
    """write request log 的通用操作"""
    error_info = Utils.exception_to_str(exception)
    url_info = Utils.del_str_quotes(Application.get_url(request))
    method = Utils.del_str_quotes(Application.get_method(request))
    params = Utils.del_str_quotes(str(Application.get_request_params(request)))
    headers = Utils.del_str_quotes(str(Application.get_headers(request)))
    log.write_request_log(location_of_error, error_info, url_info, method, params, headers)


@Application.register('/api/v1/builds')
def post_build_info(request: Request) -> Response:
    log = Log(mysql_cursor)
    exception = None
    try:
        build_info = Application.get_test_info_all(request)
        Build(mysql_cursor).write_build_info_to_database(build_info, log)
        return Application.response_json(build_info)
    except Exception as e:
        exception = e
    finally:
        location_of_error = NONE_EXCEPTION if exception is None \
            else "%s.%s" % (os.path.split(__file__)[-1], Utils.get__function_name())
        write_request_log_common_operation(request, log, exception, location_of_error)


@Application.register('/api/v1/commits')
def query_overview(request: Request) -> Response:
    """查看所有commit信息"""
    log = Log(mysql_cursor)
    exception = None
    try:
        page_num = Application.get_query_info_params(request)[PAGE_NUM_KEY]
        result_info = Commit(page_num, mysql_cursor).query_commits(log)
        return Application.response_json(result_info)
    except Exception as e:
        exception = e
    finally:
        location_of_error = NONE_EXCEPTION if exception is None \
            else "%s.%s" % (os.path.split(__file__)[-1], Utils.get__function_name())
        write_request_log_common_operation(request, log, exception, location_of_error)


@Application.register('/api/v1/commits/builds')
def query_commit_detail(request: Request) -> Response:
    """查看某一个commit下面的所有build信息，参数 commit-id """
    log = Log(mysql_cursor)
    exception = None
    try:
        params_info = Application.get_query_info_params(request)
        page_num = params_info[PAGE_NUM_KEY]
        commit_id = params_info[COMMIT_ID_KEY]
        result_info = Build(mysql_cursor).query_builds(page_num, commit_id, log)
        return Application.response_json(result_info)
    except Exception as e:
        exception = e
    finally:
        location_of_error = NONE_EXCEPTION if exception is None \
            else "%s.%s" % (os.path.split(__file__)[-1], Utils.get__function_name())
        write_request_log_common_operation(request, log, exception, location_of_error)


@Application.register('/api/v1/commits/builds/tests')
def query_build_detail(request: Request) -> Response:
    """查看某一个build下面所有test_run_id信息，参数 build-id"""
    log = Log(mysql_cursor)
    exception = None
    try:
        params_info = Application.get_query_info_params(request)
        page_num = params_info[PAGE_NUM_KEY]
        build_id = params_info[BUILD_ID_KEY]
        result_info = Tests(mysql_cursor).query_tests(page_num, build_id, log)
        return Application.response_json(result_info)
    except Exception as e:
        exception = e
    finally:
        location_of_error = NONE_EXCEPTION if exception is None \
            else "%s.%s" % (os.path.split(__file__)[-1], Utils.get__function_name())
        write_request_log_common_operation(request, log, exception, location_of_error)


@Application.register('/api/v1/commits/builds/tests/process')
def query_process_detail(request: Request) -> Response:
    """查看某一个具体的process result, 参数 test-run-id"""
    log = Log(mysql_cursor)
    exception = None
    try:

        params_info = Application.get_query_info_params(request)
        page_num = params_info[PAGE_NUM_KEY]
        test_run_id = params_info[TEST_RUN_ID_KEY]
        result_info = Tests(mysql_cursor).query_process(page_num, test_run_id, log)
        return Application.response_json(result_info)
    except Exception as e:
        exception = e
    finally:
        location_of_error = NONE_EXCEPTION if exception is None \
            else "%s.%s" % (os.path.split(__file__)[-1], Utils.get__function_name())
        write_request_log_common_operation(request, log, exception, location_of_error)


@Application.register('/api/v1/commits/builds/tests/hardware')
def query_hardware_detail(request: Request) -> Response:
    """查看某一个具体的hardware result, 参数 test-run-id"""
    log = Log(mysql_cursor)
    exception = None
    try:
        params_info = Application.get_query_info_params(request)
        page_num = params_info[PAGE_NUM_KEY]
        test_run_id = params_info[TEST_RUN_ID_KEY]
        result_info = Tests(mysql_cursor).query_hardware(page_num, test_run_id, log)
        return Application.response_json(result_info)
    except Exception as e:
        exception = e
    finally:
        location_of_error = NONE_EXCEPTION if exception is None \
            else "%s.%s" % (os.path.split(__file__)[-1], Utils.get__function_name())
        write_request_log_common_operation(request, log, exception, location_of_error)


@Application.register('/api/v1/commits/builds/tests/software')
def query_software_detail(request: Request):
    params_info = Application.get_query_info_params(request)
    test_run_id = params_info[TEST_RUN_ID_KEY]
    result_info = TestSoftware(test_run_id).select_precision_recall_result()
    return Application.response_json(result_info)


@Application.register('/api/v1/hardware')
def post_hardware_result(request: Request):
    """硬件测试完成后的结果输入"""
    log = Log(mysql_cursor)
    exception = None
    try:
        print(request.json)
        log = Log(mysql_cursor)
        TestHardware.write_hardware_result_to_database(request.json, log)
        return Response(json.dumps(request.json).encode(encoding='utf-8'))
    except Exception as e:
        exception = e
    finally:
        location_of_error = NONE_EXCEPTION if exception is None \
            else "%s.%s" % (os.path.split(__file__)[-1], Utils.get__function_name())
        write_request_log_common_operation(request, log, exception, location_of_error)


@Application.register('/api/v1/task')
def hand_build_test(request: Request) -> Response:
    log = Log(mysql_cursor)
    exception = None
    try:
        build_info = request.json
        Task(build_info[BUILD_ID_KEY], build_info[SOURCE_KEY], mysql_cursor, log).\
            write_task_info_to_database(is_manual=True)
        return Response('task created, please waiting...'.encode(encoding='utf-8'))
    except Exception as e:
        exception = e
    finally:
        location_of_error = NONE_EXCEPTION if exception is None \
            else "%s.%s" % (os.path.split(__file__)[-1], Utils.get__function_name())
        write_request_log_common_operation(request, log, exception, location_of_error)


@Application.register('/api/v1/software')
def post_software_result(request: Request) -> Response:

    request_json = request.json
    test_run_id = request_json[TEST_RUN_ID_KEY]
    file_type = "_" + request_json[TYPE_KEY]
    test_software = TestSoftware(test_run_id)
    software_test_file_directory = test_software.software_test_mkdir()

    file_path = software_test_file_directory + test_run_id + file_type
    data = request_json["data"][:-2] + request_json["data"][-1]

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(data)
    print(file_type)
    if file_type == "_adas":
        test_software.get_precision_recall()
        import time
        time.sleep(10)

    return Response(json.dumps(data).encode(encoding='utf-8'))


@Application.register('/api/v1/latest_apk_version')
def get_latest_apk_version(request: Request) -> Response:
    data = {"version": 200, "path": "/mapa-release-20190711.5.apk"}
    return Response(json.dumps(data).encode(encoding='utf-8'))


@Application.register('/api/beta/latest_apk_version')
def get_latest_apk_version_beta(request: Request) -> Response:
    data = {"version": 204, "path": "/mapa-release-20190711.5.apk"}
    return Response(json.dumps(data).encode(encoding='utf-8'))


@Application.register('/api/v1/download')
def get_apk_path(request: Request):
    parent_path = request.GET.get('path')
    apk_names = os.listdir(parent_path)
    apk_list = []
    for i in apk_names:
        apk_dict = {}
        apk_dict['apk_name'] = i
        apk_list.append(apk_dict)
    ret = {'apk_names': apk_list}
    return Application.response_json(ret)


@Application.register('/api/v1/query')
def get_query(request: Request):
    select_info = request.GET.get('select_info')
    page_num = Application.get_query_info_params(request)[PAGE_NUM_KEY]
    result_info = Commit(page_num, mysql_cursor).query_select_info(select_info)
    return Application.response_json(result_info)


@Application.register('/api/v1/software_mapping')
def get_software_mapping_test(request: Request):

    request_json = request.json
    print(request_json)
    test_run_id = request_json.get(TEST_RUN_ID_KEY)
    request_json.pop(TEST_RUN_ID_KEY)
    software_test_file_directory = TestSoftware(test_run_id).software_test_mkdir()
    file_path = software_test_file_directory + test_run_id + MAPPING
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(request_json, f)
    f.close()
    return Response(json.dumps(request_json).encode(encoding='utf-8'))


def listen_run():
    global mysql_cursor
    mysql_cursor = MysqlClient()
    ip = '0.0.0.0'
    port = 9999
    server = make_server(ip, port, Application())
    try:
        server.serve_forever()
    except KeyboardInterrupt as e:
        pass
    finally:
        server.shutdown()
        server.server_close()


if __name__ == '__main__':
    listen_run()
