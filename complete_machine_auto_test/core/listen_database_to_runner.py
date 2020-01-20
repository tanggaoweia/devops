import os
import time
import gc
from core.mysql_client import MysqlClient
from core.test_software import TestSoftware
from core.utils import Utils
from core.test_hardware import TestHardware
from core.test_process import TestProcess
from core.tests import Tests
from core.log import Log
from conf.constant_settings import TEST_RUN_ID_KEY, BUILD_ID_KEY
from core.task import Task


def test_run():
    mysql_cursor = MysqlClient()
    log = Log(mysql_cursor)
    test_run_id = ''
    hardware_loop_num = 5
    process_loop_num = 5
    while True:
        try:
            # 查找可以执行的任务
            task_info = Task.get_an_executable_task(mysql_cursor)

            if len(task_info) == 1:
                print('Perform tasks')
                task_info = task_info[0]
                test_run_id = task_info[TEST_RUN_ID_KEY]
                apk_path = task_info['apk_path']

                # 执行任务
                if os.path.exists(apk_path):

                    TestHardware(test_run_id, mysql_cursor, apk_path, hardware_loop_num).test_runner()

                    TestProcess(test_run_id, mysql_cursor, process_loop_num).test_runner(log)
                    Tests(mysql_cursor).insert_test_total_result(test_run_id, log)

                    TestSoftware(test_run_id).test_runner(log)

                # 修改任务状态
                Task.update_task_status(mysql_cursor, test_run_id)

                # 处理异常路径
                if not os.path.exists(apk_path):
                    raise Exception("apk path : '%s' ,does not exist" % apk_path)
            else:
                time.sleep(3)
        except Exception as e:
            error_key = os.path.basename(__file__)
            Log.write_operation_log(mysql_cursor, test_run_id, error_key, Utils.del_str_quotes(str(e)))

        gc.collect()


if __name__ == '__main__':
    test_run()
