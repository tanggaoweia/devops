import os
import re
import time


class Process(object):
    """进程操作类"""
    STATUS_WITH_NOT_FOUND_PROCESS = 'FF'

    def get_process_status(self, process_name):
        """获取进程的状态"""
        process_info = self.get_process_info(process_name)
        return process_info[-2]

    def kill_process(self, process_name):
        """adb命令杀掉进程      adb shell kill pid"""
        process_pid = self.get_process_pid(process_name)
        os.popen("adb shell kill %s" % process_pid)

    def get_process_info(self, process_name):
        """adb命令获得一条进程信息   adb shell ps | grep process"""
        time.sleep(5)
        process_info = os.popen('adb shell "ps | grep %s"' % process_name).readlines()
        if len(process_info) == 0:
            return self.STATUS_WITH_NOT_FOUND_PROCESS
        for i in range(len(process_info)):
            for j in process_info[i].split(' '):
                if j == 'com.wissen.mapa\n':
                    return re.split(" ", process_info[i])

    def get_process_pid(self, process_name):
        """获得进程的PID号"""
        try:
            # process_info = re.split(" ", os.popen('adb shell "ps | grep %s"' % process_name).readlines())
            process_info = self.get_process_info(process_name)
            print(111, process_info)
            for i in range(len(process_info)):
                if i > 0 and len(process_info[i]) > 0:
                    print(process_info[i])
                    return process_info[i]
        except Exception as e:
            return e


# if __name__ == '__main__':
#     process = Process()
#     print(process.get_process_info("com.wissen.mapa"))
#     print(process.get_process_pid("com.wissen.mapa"))
