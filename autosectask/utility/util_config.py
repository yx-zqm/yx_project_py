# -*- coding: utf-8 -*-
# @Author : Wei XiLi (wei.xl@asiainfo-sec.com)
# @Date   : 2018-08-23 14:17:36
# @Memo   : reading config
# @Revision:
#   * 2021-08-12, Wei.xl, change to config to singleton && return list of dictionary [dict1, dict2]
#   * 2021-12-28, Wei.xl, 针对通过配置和其他配置的程序, 移除了单例模式的配置class Config(Singleton):
#   * 2022-08-14, wei.xl, 针对windows平台新增编码集self.__config.read(cfg_path,encoding="utf-8")
import logging

from utility.singleton import Singleton
from autosectask.utility.util_logging import SimpleLogger
import configparser
import os

logger = SimpleLogger(level=logging.DEBUG).get_logger()


class Config:
    """config file: 'application.ini'"""

    __config = None

    def __init__(self, cfg='default'):
        # todo validation of config file
        if cfg == 'default':
            root_dir = os.path.dirname(os.path.abspath(''))
            cfg_path = os.path.join(root_dir, "application.ini")
        else:
            cfg_path = cfg
            self.__cfg_path = cfg

        if not self.__config:
            logger.info(f'Loading config file: {cfg_path}')
            self.__config = configparser.ConfigParser()
            self.__config.read(cfg_path, encoding="utf-8")

    def read_with_sub_sec(self, main_sec):
        result = []
        for sec in self.get_sections():
            if sec.startswith(main_sec):
                result.append({sec.title().split(".")[-1]: dict(self.__config.items(sec))})
        return result

    def read_str(self, section, key):
        logger.debug(f'Reading config as string: section={section}, key={key}, value={self.__config[section][key]}')
        return self.__config[section][key]

    def read_int(self, section, key):
        logger.debug(f'Reading config as int: section={section}, key={key}, value={self.__config[section][key]}')
        return int(self.__config[section][key])

    def get_sections(self):
        logger.debug(f'Reading <<{self.get_name()}>>. Sections: {self.__config.sections()}')
        return self.__config.sections()

    def get_keys(self, section):
        keys = [key for key, value in self.__config.items(section)]
        return keys

    def read_section(self, section):
        logger.debug(f'Loading section: {section}, keys={self.get_keys(section)}')
        sec_dict = {}
        for key in self.__config[section].keys():
            sec_dict[key] = self.__config[section][key]
        return sec_dict

    # 没有增加ABCD等级时候的函数
    def read_section_list(self, section):
        values = []
        for key, value in self.read_section(section).items():
            values.append(value)
        return values

    # 增加ABCD等级时候的函数
    def read_section_list_ABCD(self, section):
        values = []
        for key, value in self.read_section(section).items():
            values.append(value)
        keys = []
        for key, value in self.read_section(section).items():
            keys.append(key[0])
        return [keys, values]

    def read_section_list_length(self, section):
        return len(self.__config[section])

    def get_path(self):
        return self.__cfg_path

    def get_name(self):
        return os.path.basename(self.__cfg_path)


def test():
    cfg = Config()
    json2oracle = [section for section in cfg.get_sections() if 'json2oracle_' in section]
    print(json2oracle)
    for sec in json2oracle:
        print(cfg.read_section(sec))
        cfg.read_str(sec, 'db_table_name')


if __name__ == '__main__':
    # test()
    exit(1)
