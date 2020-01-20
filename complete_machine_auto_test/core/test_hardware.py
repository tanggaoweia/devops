import os
import time
from core.test_process import TestProcess
from core.utils import Utils
from core.log import Log
from conf.constant_settings import *


class TestHardware(object):

    order_of_fields_in_record = [
        'UUID',
        'ANDROID_VERSION',
        'APP_VERSION',
        'ACC_STATUS',
        'AIRPLANE_OFFTOON',
        'AIRPLANE_ONTOOFF',
        'CPU_TEMP',
        'GPS_STATUS',
        'HAS_RESTARTED',
        'MOBILE4G_OFFTOON',
        'MOBILE4G_ONTOOFF',
        'SDCARD_STATUS',
        'WIFI_STATUS',
        'GENERIC_INFO'
    ]

    _test_hardware_log_key = 'hardware test is complete'
    _test_hardware_log_value = ' is completed'
    _test_hardware_log_too_long_value = 'hardware test is too long'

    def __init__(self, test_run_id,
                 mysql_cursor,
                 apk_path,
                 loop_num,
                 do_reboot=False):
        self.test_run_id = test_run_id
        self.mysql_cursor = mysql_cursor
        self.apk_path = apk_path
        self.loop_num = loop_num
        self.do_reboot = do_reboot
        self._uninstall_log_key = 'apk uninstall result'
        self._install_log_key = 'apk install result'

    def test_runner(self):
        # 卸载已有安装包

        apk_uninstall_info = os.popen("adb uninstall " + TestProcess.MAPA_PROCESS_NAME).readlines()[0]
        Log.write_operation_log(self.mysql_cursor,
                                self.test_run_id,
                                self._uninstall_log_key,
                                apk_uninstall_info,
                                is_error=False)

        # 安装最新安装包
        apk_install_info = os.popen("adb install  -t -r %s" % self.apk_path).readlines()[-2]
        Log.write_operation_log(self.mysql_cursor,
                                self.test_run_id,
                                self._install_log_key,
                                apk_install_info,
                                is_error=False)

        # 执行硬件测试
        os.popen("adb shell am startservice "
                 "--es testrunid %s"
                 " --ei loopnum %s"
                 " --ez doreboot %s  "
                 "com.wissen.mapa/com.wissen.mapa.HardwareInterfaceStatusAutoTestService" %
                 (self.test_run_id, self.loop_num, 'false'))

        # 判断硬件测试是否完成
        test_is_completed = self._is_test_execution_completed()
        start_time = time.time()
        while not test_is_completed:
            print(2, not self._is_test_execution_completed())
            time.sleep(60)
            test_is_completed = self._is_test_execution_completed()
            print('hardware test not completed!')
            end_time = time.time()
            if end_time - start_time >= 600:
                Log.write_operation_log(self.mysql_cursor,
                                        self.test_run_id,
                                        TestHardware._test_hardware_log_key,
                                        TestHardware._test_hardware_log_too_long_value,
                                        is_error=False)
                return

    def _is_test_execution_completed(self):
        select_hardware_test_result_sql = "select * from hardware_test_result where test_run_id = '%s' " % \
                                          self.test_run_id
        hardware_test_result = self.mysql_cursor.mysql_select_sql(select_hardware_test_result_sql)
        if len(hardware_test_result) > 0:
            return True
        return False

    @classmethod
    def write_hardware_result_to_database(cls, hardware_result: dict, log):
        print('开始写log了')
        common_info = hardware_result[HARDWARE_TEST_RECORDLIST_KEY][0][HARDWARE_TEST_RECORDLIST_VALUE_KEY]
        uuid = common_info[cls.order_of_fields_in_record[0]]
        android_version = common_info[cls.order_of_fields_in_record[1]]
        app_version = common_info[cls.order_of_fields_in_record[2]]
        test_run_id = hardware_result[HARDWARE_TEST_DESCRIPTION_KEY][TABLE_TEST_RUN_ID_KEY]
        build_id = cls.get_build_id(test_run_id, log)

        update_test_run_description_sql = "update build_description set uuid='%s'," \
                                          " android_version='%s', app_version='%s' " \
                                          "where build_id = '%s'" % \
                                          (uuid, android_version, app_version, build_id)
        exception = None
        try:
            if cls.is_update_build_description(build_id, log):
                log.mysql_cursor.mysql_insert_or_update_sql(update_test_run_description_sql)
        except Exception as e:
            exception = e
        finally:
            location_of_error = NONE_EXCEPTION if exception is None \
                            else "%s.%s" % (os.path.split(__file__)[-1], Utils.get__function_name())
            error_info = Utils.exception_to_str(exception)
            log.write_db_log(location_of_error, error_info,
                             Utils.del_str_quotes(update_test_run_description_sql), test_run_id=test_run_id)

        hardware_record_list = hardware_result[HARDWARE_TEST_RECORDLIST_KEY]
        for i in range(len(hardware_record_list)):
            result_list = hardware_record_list[i][HARDWARE_TEST_RECORDLIST_VALUE_KEY]
            airplan_off_to_on = result_list.get(AIRPLANE_OFF_TO_ON_KEY, NOT_FIND_KEY)
            airplan_on_to_off = result_list.get(AIRPLANE_ON_TO_OFF_KEY, NOT_FIND_KEY)
            mobile4g_off_to_on = result_list.get(MOBILE4G_OFF_TO_ON_KEY, NOT_FIND_KEY)
            mobile4g_on_to_off = result_list.get(MOBILE4G_ON_TO_OFF_KEY, NOT_FIND_KEY)
            gps_status = result_list.get(GPS_STATUS_KEY, NOT_FIND_KEY)
            acc_status = result_list.get(ACC_STATUS_KEY, NOT_FIND_KEY)
            sdcard_status = result_list.get(SDCARD_STATUS_KEY, NOT_FIND_KEY)
            wifi_status = result_list.get(WIFI_STATUS_KEY, NOT_FIND_KEY)
            has_restarted = result_list.get(HAS_RESTARTED_KEY, NOT_FIND_KEY)
            cpu_temp = result_list.get(CPU_TEMP_KEY, NOT_FIND_KEY)

            insert_hardware_test_result_sql = "insert into hardware_test_result (test_run_id, airplan_off_to_on, " \
                                              "airplan_on_to_off, mobile4g_off_to_on, mobile4g_on_to_off, gps_status," \
                                              "acc_status, sdcard_status, wifi_status, has_restarted, cpu_temp, " \
                                              "created_time) values" \
                                              "('%s', '%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
                                              % (test_run_id,
                                                 airplan_off_to_on,
                                                 airplan_on_to_off,
                                                 mobile4g_off_to_on,
                                                 mobile4g_on_to_off,
                                                 gps_status,
                                                 acc_status,
                                                 sdcard_status,
                                                 wifi_status,
                                                 has_restarted,
                                                 cpu_temp,
                                                 Utils.get_time())
            print(22222)
            print(i, insert_hardware_test_result_sql)
            exception = None
            try:
                log. mysql_cursor.mysql_insert_or_update_sql(insert_hardware_test_result_sql)
            except Exception as e:
                exception = e
            finally:
                location_of_error = NONE_EXCEPTION if exception is None \
                    else "%s.%s" % (os.path.split(__file__)[-1], Utils.get__function_name())
                error_info = Utils.exception_to_str(exception)
                log.write_db_log(location_of_error, error_info,
                                 Utils.del_str_quotes(insert_hardware_test_result_sql), test_run_id=test_run_id)

        Log.write_operation_log(log.mysql_cursor,
                                test_run_id,
                                TestHardware._test_hardware_log_key,
                                TestHardware._test_hardware_log_value,
                                is_error=False)

    @classmethod
    def get_build_id(cls, test_run_id, log):
        sql = "select build_id from build_and_test_info where test_run_id = '%s'" % test_run_id
        return log.mysql_cursor.mysql_select_sql(sql)[0][BUILD_ID_KEY]

    @classmethod
    def is_update_build_description(cls, build_id, log):
        try:
            sql = "select uuid from build_description where build_id = '%s'" % build_id
            return log.mysql_cursor.mysql_select_sql(sql)[0][UUID_KEY] is None
        except Exception as e:
            print(e)


# if __name__ == '__main__':
#     build_id = '1--40107ac69fd38bce155d199e99cc12b60e6e3815'
#     log = Log(MysqlClient())
#     print(TestHardware.is_update_build_description(build_id, log))
