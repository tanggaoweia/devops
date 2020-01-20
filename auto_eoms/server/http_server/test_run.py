import uuid


class TestRun:

    @classmethod
    def get_test_run_id(cls):
        """
        get test run id
        :return:
        """
        return str(uuid.uuid4())
