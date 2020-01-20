from configparser import ConfigParser


class Config(object):

    db_config_path = r'../conf/db_config.ini'

    @classmethod
    def read_config_file(cls, config_path) -> dict:
        """读取配置文件"""
        config_dict = {}
        cp = ConfigParser()
        cp.read(config_path, encoding='utf-8')
        section = cp.sections()[0]
        for key, value in cp.items(section):
            config_dict[key] = value
        return config_dict