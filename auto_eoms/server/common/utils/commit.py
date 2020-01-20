import requests


class Commit:
    _TOKEN = 's5gfbkrjxck2iwasvoptwdwitjcxojjksmiu4vdhgf37l5e6n7ra'
    MAPA_COMMIT_BASE_URI = r'http://10.1.1.53:8080/tfs/sh-ws-office/Mapa/' \
                           r'_apis/git/repositories/mapa2_arm_mtk_xiaozhuo/commits/'
    ANDROID_PHONE_COMMIT_BASE_URI = r'http://10.1.1.53:8080/tfs/sh-ws-office/Mapa/' \
                                    r'_apis/git/repositories/Mapa2_Android_phone/commits/'

    @staticmethod
    def _get_commit_info(commit_id, base_url):
        """获得commit作者"""
        auth = ("", Commit._TOKEN)
        uri = base_url + commit_id
        params = {'api-version': 5.0}
        r = requests.get(uri, params=params, auth=auth, verify=False)
        return r.json()

    @classmethod
    def get_commit_author(cls, commit_id, base_url) -> str:
        """
        get commit author
        :param commit_id:
        :param base_url:
        :return:
        """
        return Commit._get_commit_info(commit_id, base_url)['author']['email']

    @classmethod
    def get_commit_msg(cls, commit_id, base_url) -> str:
        """
        get commit msg
        :param commit_id:
        :param base_url:
        :return:
        """
        return Commit._get_commit_info(commit_id, base_url)['comment']

    @classmethod
    def get_link_work_item(cls):
        """
        get link work item, 暂时没有实现
        :return:
        """
        return " "
