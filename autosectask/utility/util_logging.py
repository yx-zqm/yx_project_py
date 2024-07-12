# -*- coding: utf-8 -*-
# @Author : Wei XiLi (wei.xl@asiainfo-sec.com)
# @Date   : 2018-08-23 14:17:36
# @Memo   : Simple logger to console, todo: 1.png. file logger 2. bug: line of src
# @Revision:
#   * 2021-08-12, Wei.xl, change to logger to singleton

import logging
from autosectask.utility.singleton import Singleton


class FileLogger(Singleton):
    """
    todo
    """

    def __init__(self):
        pass


class SimpleLogger(Singleton):
    """
    Simple logger with format stream to console.
    """

    __logger = None

    def __init__(self, name='sh4a', level=logging.INFO):
        if not self.__logger:
            self.__name = name
            self.__level = level
            self.__logger = self._init_logger()

    def _init_logger(self):
        """
        Initiate with name and level
        """
        logger = logging.getLogger(self.__name)
        logger.setLevel(self.__level)

        # Set up handler as well as format
        my_format = '%(asctime)s.%(msecs)03d %(levelname)-8s %(filename)s:%(lineno)03d - %(message)s'
        date_format = '%Y-%m-%d %H:%M:%S'
        simple_formatter = logging.Formatter(fmt=my_format, datefmt=date_format)

        # is using stderr, the default is 0 (stdin) for input, or 1.png (stdout) for output. 2 means stderr.
        handler = logging.StreamHandler()
        handler.setFormatter(simple_formatter)

        logger.addHandler(handler)
        return logger

    def get_logger(self):
        return self.__logger


def test():
    # without Singleton it's false
    s1, s2 = SimpleLogger("log11", logging.INFO).get_logger(), SimpleLogger().get_logger()
    print(s1 == s2)
    s1.info("Hello, Logger")
    s2.debug("Hello, Debug")


if __name__ == '__main__':
    test()
    exit(1)
