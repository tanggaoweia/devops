from utils.constant_key import CODE_KEY, MSG_KEY, DATA_KEY, TOTAL_KEY


class FormatData:

    SUCCESS_CODE = 1
    FAILED_CODE = 2
    ERROR_CODE = 3
    SUCCESS_MSG = '成功'
    FAILED_MSG = '失败'
    ERROR_MSG = '出错了'
    DEFAULT_DATA = ""

    @classmethod
    def response_data(cls, code=SUCCESS_CODE, msg=SUCCESS_MSG, data=DEFAULT_DATA, total=0) -> dict:
        if total == 0:
            return {CODE_KEY: code, MSG_KEY: msg, DATA_KEY: data}
        return {CODE_KEY: code, MSG_KEY: msg, DATA_KEY: data, TOTAL_KEY: total}