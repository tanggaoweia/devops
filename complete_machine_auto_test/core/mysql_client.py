
import pymysql.cursors
from core.config import Config


class MysqlClient(object):

    def __init__(self):

        self.mysql_info = Config.read_config_file(Config.db_config_path)

        self.db = pymysql.connect(host=self.mysql_info['host'],
                                  port=int(self.mysql_info['port']),
                                  user=self.mysql_info['user'],
                                  password=self.mysql_info['password'],
                                  db=self.mysql_info['db_name'],
                                  charset='utf8')
        self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)

    def mysql_select_sql(self, sql):
        """SQL查询"""
        self.db.ping(reconnect=True)
        self.cursor.execute(sql)
        s_result = self.cursor.fetchall()
        self.db.commit()
        return s_result

    def mysql_insert_or_update_sql(self, sql):
        """SQL插入或更新，也可执行删除"""
        self.db.ping(reconnect=True)
        self.cursor.execute(sql)
        self.db.commit()

    def close(self):
        """关闭SQL连接"""
        self.cursor.close()
        self.db.close()


