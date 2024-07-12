#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Wei XiLi (wei.xl@asiainfo-sec.com)
# @Date   : 2018-08-12 14:04:55
# @Memo   : wrapper for db connector, todo: 1.png. connection pool not yet implemented 2. Database conn Factory
# @Revision:
#   * 2021-08-12, Wei.xl, extract from config
#


import cx_Oracle
from util_logging import SimpleLogger

logger = SimpleLogger().get_logger()


class ConnOracle(object):
    """ database connection """
    # todo: overload
    def __init__(self, auth):
        self.__db = cx_Oracle.connect(auth)

    # def __init__(self, server, port, user, password, sid):
    #     # password decryption
    #     self.__db = cx_Oracle.connect(f'{user}/{password}@{server}:{port}/{sid}')

    def _get_instance(self):
        return self.__db

    def __enter__(self):
        logger.info("creating db connection..")
        return self._get_instance()

    def __exit__(self, e_t, e_v, t_b):
        logger.info("releasing db connection..")
        self.__db.close()
