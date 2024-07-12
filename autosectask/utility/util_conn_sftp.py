#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Wei XiLi (wei.xl@asiainfo-sec.com)
# @Date   : 2018-08-14 17:55:55
# @Memo   : wrapper for db connector
# @Revision:
#   * 2021-08-12,
#

import paramiko
from autosectask.utility.util_logging import SimpleLogger
from autosectask.utility.util_alarm import notify

logger = SimpleLogger().get_logger()


class ConnSftp(object):
    """ sftp connection """

    def __init__(self, host, port, user, password):
        # password decryption
        try:
            self.__transport = paramiko.Transport((host, port))
            self.__transport.connect(username=user, password=password)
            self.__client = paramiko.SFTPClient.from_transport(self.__transport)
            self.__ssh = None
        except Exception as exp:
            notify(f'33004-Json采集入库sftp初始化异常：{exp}')

    def upload(self, local_path, remote_path):
        try:
            self.__client.put(local_path, remote_path)
        except Exception as exp:
            notify(f'33004-Json采集入库sftp-upload文件报错{exp}')
            logger.error(exp)

    def download(self, local_path, remote_path):
        try:
            self.__client.get(remote_path, local_path)
        except Exception as exp:
            notify(f'33004-Json采集入库sftp-download文件报错{exp}')
            logger.error(exp)

    def rename(self, old_path, new_path):
        try:
            self.__client.rename(old_path, new_path)
        except Exception as exp:
            notify(f'33004-Json采集入库sftp-rename文件报错{exp}')
            logger.error(exp)

    def listdir(self, remote_dir):
        try:
            file_list = self.__client.listdir(remote_dir)
        except Exception as exp:
            notify(f'33004-Json采集入库sftp-listdir文件报错{exp}')
            logger.error(exp)
        # logger.debug(f'List of remote dir: {file_list}')
        return file_list

    # todo: 其他需要的sftp功能可以在需要的时候写在此处

    def exec_cmd(self, cmd):
        try:
            self.__ssh = paramiko.SSHClient()
            self.__ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            self.__ssh._transport = self.__transport
            stdin, stdout, stderr = self.__ssh.exec_command(cmd)
            logger.info(stdout.read())
        except Exception as exp:
            notify(f'33004-Json采集入库执行远程主机命令报错{exp}')
            logger.error(exp)
        finally:
            self.__ssh.close()

    def _get_instance(self):
        return self

    def __enter__(self):
        logger.info("creating sftp connection..")
        return self._get_instance()

    def __exit__(self, e_t, e_v, t_b):
        logger.info("releasing sftp connection..")
        self.__client.close()
        self.__transport.close()
