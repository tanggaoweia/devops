import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(os.getcwd())))
from threading import Thread
from core.listen_database_to_runner import test_run
from core.listen_query_info import listen_run


if __name__ == '__main__':
    t1 = Thread(target=test_run)
    t2 = Thread(target=listen_run)
    t1.start()
    t2.start()
