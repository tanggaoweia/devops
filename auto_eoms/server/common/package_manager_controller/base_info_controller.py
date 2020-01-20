from common.utils.key_constant import *


class BaseInfoController(object):
    _BUILD_INFO_KEYS = ('commitId', 'branch', 'requestedForEmail', 'buildId', 'sourceBranch',
                        'targetBranch', 'jobName', 'name', 'buildNumber')

    _PULL_REQUEST_ID_IS_NONE_STR = "$(System.PullRequest.PullRequestId)"
    _TARGET_BRANCH_IS_NONE_STR = "$(System.PullRequest.TargetBranch)"
    _SOURCE_BRANCH_IS_NONE_STR = "$(System.PullRequest.SourceBranch)"

    def __init__(self, data):
        """
        构造函数
        :param data:  jenkins 取到的信息
        """
        self._data = data
        self._commit_id = data.get(self._BUILD_INFO_KEYS[0])
        self._branch_name = data.get(self._BUILD_INFO_KEYS[1])
        self._build_author = data.get(self._BUILD_INFO_KEYS[2])
        self._build_id = data.get(self._BUILD_INFO_KEYS[3]) + '--' + self._commit_id
        self._build_number = data.get(self._BUILD_INFO_KEYS[-1])
        self._job_name = data.get(self._BUILD_INFO_KEYS[-3]).split('_')[-1]
        self._source_branch = data.get(self._BUILD_INFO_KEYS[4])
        if self._source_branch == self._SOURCE_BRANCH_IS_NONE_STR:
            self._source_branch = ""
        else:
            self._source_branch = self._source_branch.split('/')[-1]
        self._target_branch = data.get(self._BUILD_INFO_KEYS[-4])
        if self._target_branch == self._TARGET_BRANCH_IS_NONE_STR:
            self._target_branch = ""
        else:
            self._target_branch = self._target_branch.split('/')[-1]
        self._common_path_header = '/home/sh-ws-dispatch/releasewindows'
        self._apk_common_path = '{}/{}/{}/{}@{}@{}@{}@{}@{}/'.format(
            self._common_path_header,
            self._build_number.split('.')[0],
            self._data.get(self._BUILD_INFO_KEYS[-2]),
            self._branch_name,
            self._build_author.split('@')[0],
            self._source_branch,
            self._target_branch,
            self._build_number,
            self._commit_id
        )
        self._pull_request_id = data.get(const.PULL_REQUEST_ID_KEY)
        self._pull_request_id = None if self._pull_request_id == self._PULL_REQUEST_ID_IS_NONE_STR \
            else self._pull_request_id
        self._jenkins_info = {
            const.DATA_KEY: self._data,
            const.BUILD_ID_KEY: self._build_id,
            const.COMMIT_ID_KEY: self._commit_id,
            const.BUILD_AUTHOR_KEY: self._build_author,
            const.BRANCH_NAME_KEY: self._branch_name,
            const.APK_COMMON_PATH_KEY: self._apk_common_path,
            const.PULL_REQUEST_ID_KEY: self._pull_request_id
        }
