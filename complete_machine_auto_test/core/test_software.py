import os
import time
import json
import platform
from conf.constant_settings import SOFTWARE_TEST_COMMON_FILE_PATH, MAPPING, DAY_CLOUDY_SKYWAY, DAY_CLOUDY_UBRAN, \
    RESPONSE_VALUE_KEY
from core.box import Box
from core.process import Process
from core.test_process import TestProcess
from core.utils import Utils
from core.xml_manager import XMLManager
from core.mysql_client import MysqlClient


class TestSoftware:
    VIDEO_SCENE_MAPPING = {
        r"Mapa_20180426160620_stream0_1_14_clip1.avi": DAY_CLOUDY_SKYWAY,
        r"Mapa_19700107053526_stream0_1_8_clip1.avi": DAY_CLOUDY_UBRAN,
    }
    if platform == 'Windows':
        GT_FILE_PATH = r'E:\test_avi\Mapa_20180426160620_stream0_1_14_clip1\\'
    else:
        GT_FILE_PATH = r'/home/sh-ws-dispatch/wstanggw/test_data/'

    FILE_SPLIT_SEP = '_'

    _test_software_log_key = 'software test is complete'
    _test_software_log_value = ' is completed'
    _test_software_failed_value = 'software test failed'

    def __init__(self, test_run_id):
        self.software_test_file_directory = None
        self.test_run_id = test_run_id
        self.mysql_client = MysqlClient()

    def test_runner(self, log):
        try:
            print("start software test")
            time.sleep(10)

            # 执行软件测试
            print("++++++++++++++")
            os.popen("adb shell am startservice "
                     "--es testrunid %s "
                     "com.wissen.mapa/com.wissen.mapa.AlgorithmFeedDataTestService" %
                     self.test_run_id)
            print("++++++++++")

            time.sleep(2)
            process = Process()
            init_mapa_process_info = process.get_process_pid(TestProcess.MAPA_PROCESS_NAME)
            print(222, init_mapa_process_info)
            print(333, process.get_process_info(TestProcess.MAPA_PROCESS_NAME))

            # 判断软件测试是否完成
            count = 0
            while True:
                count += 1
                now_mapa_process_info = process.get_process_pid(TestProcess.MAPA_PROCESS_NAME)
                time.sleep(60)
                print(444, self.select_test_result())
                if len(self.select_test_result()) > 0:
                    # 记录操作成功的日志
                    log.write_operation_log(self.mysql_client,
                                            self.test_run_id,
                                            TestSoftware._test_software_log_key,
                                            TestSoftware._test_software_log_value,
                                            False)
                    break
                if init_mapa_process_info != now_mapa_process_info or count == 20:
                    # 记录操作失败的日志
                    print(init_mapa_process_info, now_mapa_process_info)
                    time.sleep(10)
                    log.write_operation_log(self.mysql_client,
                                            self.test_run_id,
                                            TestSoftware._test_software_log_key,
                                            TestSoftware._test_software_failed_value,
                                            False)
                    break
        except Exception as e:
            print(e)

    def select_test_result(self):
        sql = "select * from software_test_result where test_run_id = '%s'" % self.test_run_id
        return self.mysql_client.mysql_select_sql(sql)

    def software_test_mkdir(self):
        if not os.path.exists(SOFTWARE_TEST_COMMON_FILE_PATH):
            os.mkdir(SOFTWARE_TEST_COMMON_FILE_PATH)
        date = time.strftime('%Y%m%d/', time.localtime(time.time()))
        self.software_test_file_directory = SOFTWARE_TEST_COMMON_FILE_PATH + date
        if not os.path.exists(self.software_test_file_directory):
            os.mkdir(self.software_test_file_directory)
        return self.software_test_file_directory

    def _get_adas_result(self):
        print(self.test_run_id)
        with open(self.software_test_file_directory + self.test_run_id + '_adas', 'r', encoding='utf-8') as f:
            return json.load(f)

    def _get_mapping_result(self):
        with open(self.software_test_file_directory + self.test_run_id + MAPPING, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def get_video_name(jpg_name: str):
        jpg_name_split = jpg_name.split(TestSoftware.FILE_SPLIT_SEP)
        video_file_name = ""
        for j in range(len(jpg_name_split) - 1):
            video_file_name += jpg_name_split[j] + TestSoftware.FILE_SPLIT_SEP
        return video_file_name[:-1] + '.avi'

    def get_algorithmic_matching_mapping_info(self):
        """获取算法匹配的映射信息"""
        adas_result = self._get_adas_result()
        mapping_result = self._get_mapping_result()
        adas_result_time = []
        useful_mapping_info = {}

        # 獲取adas的時間戳列表
        for i in adas_result:
            for j in i:
                adas_result_time.append(str(j['time']))

        # 獲取映射信息表中對應的文件名
        for i in adas_result_time:
            if platform.system() == 'Windows':
                os.sep = '/'
            useful_mapping_info[i] = mapping_result[i].split(os.sep)[-1]

        for i in range(len(adas_result)):
            for j in range(len(adas_result[i])):
                adas_result[i][j]['time'] = useful_mapping_info[str(adas_result[i][j]['time'])]
        return useful_mapping_info, adas_result

    def get_gt_result(self):
        gt_result = []
        gt_result_dict = {}
        gt_count = 0
        useful_mapping_info = self.get_algorithmic_matching_mapping_info()[0]
        for i in useful_mapping_info:
            gt_file_name = useful_mapping_info[i][:-3] + 'xml'
            gt_file_path = TestSoftware.GT_FILE_PATH + gt_file_name
            gt_result.append(XMLManager.xml_parse(gt_file_path))

        for i in gt_result:
            for j in i.values():
                gt_count += len(j)

        # gt_result 转化为dict，原本为list
        for i in gt_result:
            for j in i:
                gt_result_dict[j] = i[j]

        return gt_count, gt_result_dict

    def get_final_adas_result(self):
        adas_result = self.get_algorithmic_matching_mapping_info()[1]
        new_adas_result = []
        for i in range(len(adas_result)):
            for j in range(len(adas_result[i])):
                result = adas_result[i][j]
                xmin = int(result.get('left'))
                ymin = int(result.get('top'))
                width = int(result.get('right')) - xmin
                high = int(result.get('bottom')) - ymin
                new_adas_result.append({result.get('time'): (xmin, ymin, width, high)})
        return len(new_adas_result), new_adas_result

    def get_count(self):
        gt_result = self.get_gt_result()[1]
        adas_result = self.get_final_adas_result()[1]
        gt_day_cloudy_skyway = 0
        adas_day_cloudy_skyway = 0
        gt_day_cloudy_ubran = 0
        adas_day_cloudy_ubran = 0
        for i in gt_result:
            car_scene = TestSoftware.VIDEO_SCENE_MAPPING.get(TestSoftware.get_video_name(i))
            if car_scene == DAY_CLOUDY_SKYWAY:
                gt_day_cloudy_skyway += len(gt_result[i])
            if car_scene == DAY_CLOUDY_UBRAN:
                gt_day_cloudy_ubran += len(gt_result[i])

        for i in adas_result:
            for j in i:
                car_scene = TestSoftware.VIDEO_SCENE_MAPPING.get(TestSoftware.get_video_name(j))
                if car_scene == DAY_CLOUDY_SKYWAY:
                    adas_day_cloudy_skyway += 1
                if car_scene == DAY_CLOUDY_UBRAN:
                    adas_day_cloudy_ubran += 1

        return {
            DAY_CLOUDY_SKYWAY: (adas_day_cloudy_skyway, gt_day_cloudy_skyway),
            DAY_CLOUDY_UBRAN: (adas_day_cloudy_ubran, gt_day_cloudy_ubran)
        }

    def get_overlapping_count(self):
        gt_result = self.get_gt_result()
        adas_result = self.get_final_adas_result()
        day_cloudy_skyway = 0
        day_cloudy_ubran = 0

        for adas_record in adas_result[1]:
            for record_key in adas_record:
                record_value = adas_record.get(record_key)
                gt_values = gt_result[1].get(record_key.split('.')[0] + '.xml')
                adas_box = Box(record_value[0], record_value[1], record_value[2], record_value[3])
                for gt_value in gt_values:
                    gt_box = Box(gt_value[0], gt_value[1], gt_value[2], gt_value[3])
                    if (Box.overlapping_area(adas_box, gt_box) / (adas_box.get_area() + gt_box.get_area() -
                                                                  Box.overlapping_area(adas_box, gt_box))) > 0.5:

                        car_scene = TestSoftware.VIDEO_SCENE_MAPPING.get(TestSoftware.get_video_name(record_key))

                        if car_scene == DAY_CLOUDY_SKYWAY:
                            day_cloudy_skyway += 1
                        if car_scene == DAY_CLOUDY_UBRAN:
                            day_cloudy_ubran += 1
                        break
        return {
            DAY_CLOUDY_SKYWAY: day_cloudy_skyway,
            DAY_CLOUDY_UBRAN: day_cloudy_ubran
        }

    def get_precision_recall(self):
        try:
            overlapping_result = self.get_overlapping_count()
            rt = self.get_count()
            day_cloudy_skyway_overlapping_result = overlapping_result.get(DAY_CLOUDY_SKYWAY)
            day_cloudy_skyway_rt = rt.get(DAY_CLOUDY_SKYWAY)
            day_cloudy_ubran_overlapping_result = overlapping_result.get(DAY_CLOUDY_UBRAN)
            day_cloudy_ubran_rt = rt.get(DAY_CLOUDY_UBRAN)
            day_cloudy_skyway_precision = day_cloudy_skyway_overlapping_result / day_cloudy_skyway_rt[0]
            day_cloudy_skyway_recall = day_cloudy_skyway_overlapping_result / day_cloudy_skyway_rt[1]
            day_cloudy_ubran_precision = day_cloudy_ubran_overlapping_result / day_cloudy_ubran_rt[0]
            day_cloudy_ubran_recall = day_cloudy_ubran_overlapping_result / day_cloudy_ubran_rt[1]
            self.write_software_result(2,
                                       day_cloudy_skyway_precision,
                                       day_cloudy_skyway_recall,
                                       day_cloudy_skyway_rt[1],
                                       day_cloudy_skyway_rt[0],
                                       day_cloudy_skyway_overlapping_result)
            self.write_software_result(3,
                                       day_cloudy_ubran_precision,
                                       day_cloudy_ubran_recall,
                                       day_cloudy_ubran_rt[1],
                                       day_cloudy_ubran_rt[0],
                                       day_cloudy_ubran_overlapping_result)
            self.write_record_data()
        except Exception as e:
            print(111, e)

    def write_software_result(self, scene_type, precision, recall, manual_count, algorithm_count, overlapping_count):
        sql = "INSERT INTO software_test_result (test_run_id, scene_type, precision_rt , recall_rt, manual_count, " \
              "algorithm_count, overlapping_count, created_time) VALUES " \
              "('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
              (self.test_run_id, scene_type, precision, recall, manual_count, algorithm_count, overlapping_count,
               Utils.get_time())
        print(sql)
        self.mysql_client.mysql_insert_or_update_sql(sql)

    def write_record_data(self):
        sql = "insert into software_test_data (test_run_id, algorithmic_data, created_time) values ('%s', '%s', '%s')" \
              % (self.test_run_id, self.software_test_mkdir() + self.test_run_id + '_adas', Utils.get_time())
        self.mysql_client.mysql_insert_or_update_sql(sql)

    def select_precision_recall_result(self):
        sql = "select * from software_test_result where test_run_id = '%s'" % self.test_run_id
        data = self.mysql_client.mysql_select_sql(sql)
        for i in range(len(data)):
            data[i]['created_time'] = str(data[i].get('created_time'))
            data[i]['recall_rt'] = round(float(data[i].get('recall_rt')), 3)
            data[i]['precision_rt'] = round(float(data[i].get('precision_rt')), 3)
            if data[i].get('scene_type') == '2':
                data[i]['scene_type'] = DAY_CLOUDY_SKYWAY
            if data[i].get('scene_type') == '3':
                data[i]['scene_type'] = DAY_CLOUDY_UBRAN
        return {RESPONSE_VALUE_KEY: data}
