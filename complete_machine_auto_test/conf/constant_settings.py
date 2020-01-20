"""常量配置文件"""


COMMIT_BASE_URI = r'http://10.1.1.53:8080/tfs/sh-ws-office/Mapa/' \
                  r'_apis/git/repositories/mapa2_arm_mtk_xiaozhuo/commits/'

TOKEN = r's5gfbkrjxck2iwasvoptwdwitjcxojjksmiu4vdhgf37l5e6n7ra'

SQL_COUNT_KEY = 'COUNT(*)'

RESPONSE_VALUE_KEY = 'value'

RESPONSE_TOTAL_NUM_KEY = 'total_num'

PAGE_NUM_KEY = 'page'

TEST_RUN_ID_KEY = 'test_run_id'

APK_GROUP_NAME_KEY = 'apk'

COMMIT_ID_KEY = 'commit_id'

COMMIT_MSG_KEY = 'commit_msg'

COMMIT_AUTHOR_KEY = 'commit_author'

APK_PATH_KEY = 'apk_path'

SOURCE_KEY = 'source'

SOURCE_DEFAULT_VALUE = 'Jenkins'

TYPE_KEY = 'type'

LINK_WORK_ITEMS_KEY = 'link_work_items'

BRANCH_NAME_KEY = 'branch_name'

DEV_PATH_KEY = '/dev/mapa-dev.apk'

DEBUG_PATH_KEY = '/debug/mapa-debug.apk'

RELEASE_PATH_KEY = '/release/mapa-release.apk'

BUILD_AUTHOR_KEY = 'build_author'

BUILD_ID_KEY = 'build_id'

BUILD_METHOD_KEY = 'branch_method'

NONE_EXCEPTION = ' '

REQUEST_FOR_DB_RECORD_ID_TYPE = 'request_id'

TEST_RUN_FOR_DB_RECORD_ID_TYPE = 'test_run_id'

HARDWARE_TEST_DESCRIPTION_KEY = 'description'

HARDWARE_TEST_RECORDLIST_KEY = 'recordList'

HARDWARE_TEST_RECORDLIST_VALUE_KEY = 'recordMap'

AIRPLANE_OFF_TO_ON_KEY = 'AIRPLANE_OFFTOON'

AIRPLANE_ON_TO_OFF_KEY = 'AIRPLANE_ONTOOFF'

MOBILE4G_OFF_TO_ON_KEY = 'MOBILE4G_OFFTOON'

MOBILE4G_ON_TO_OFF_KEY = 'MOBILE4G_ONTOOFF'

NOT_FIND_KEY = 'null'

GPS_STATUS_KEY = 'GPS_STATUS'

ACC_STATUS_KEY = 'ACC_STATUS'

HAS_RESTARTED_KEY = 'HAS_RESTARTED'

CPU_TEMP_KEY = 'CPU_TEMP'

SDCARD_STATUS_KEY = 'SDCARD_STATUS'

WIFI_STATUS_KEY = 'WIFI_STATUS'

TABLE_TEST_RUN_ID_KEY = 'testRunId'

SOFTWARE_TEST_FILE_PATH = '../result/'

TASK_APK_TYPE = 2

UUID_KEY = 'uuid'

TOTAL_IS_NONE = {'process_total_num': None, 'process_pass_num': None, 'hardware_total_num': None, 'hardware_pass_num': None}

MAPPING = "_mapping"


DAY_CLOUDY_SKYWAY = "day-cloudy-skyway"

DAY_CLOUDY_UBRAN = "day-cloudy-ubran"

SOFTWARE_TEST_COMMON_FILE_PATH = '../result/'
