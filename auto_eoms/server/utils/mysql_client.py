
import pymysql.cursors


class MysqlClient(object):
    """数据库操作类"""

    _AUTO_EOMS_DB_CONFIG = {
        "host": "10.1.1.76",
        "user": "root",
        "password": "abc123!",
        "port": 3306,
        "db_name": "test_mapa_machine",
    }

    def __init__(self):

        self.db_config = self._AUTO_EOMS_DB_CONFIG

        self.db = pymysql.connect(host=self.db_config['host'],
                                  port=self.db_config['port'],
                                  user=self.db_config['user'],
                                  password=self.db_config['password'],
                                  db=self.db_config['db_name'],
                                  charset='utf8')
        self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)

    def mysql_select(self, sql) -> dict:
        self.db.ping(reconnect=True)
        self.cursor.execute(sql)
        s_result = self.cursor.fetchall()
        self.db.commit()
        return s_result

    def mysql_insert_update_delete(self, sql):
        self.db.ping(reconnect=True)
        self.cursor.execute(sql)
        self.db.commit()

    def close(self):
        self.cursor.close()
        self.db.close()


