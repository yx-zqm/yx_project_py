# -*- coding: utf-8 -*-
# @Author : Wei XiLi (wei.xl@asiainfo-sec.com)
# @Date   : 2018-08-23 14:17:36
# @Memo   : reading config
# @Revision:
#   * 2022-08-14, Wei.xl, 缩减工单文件目录名, 删除工单描述避免windows下文件夹过长

from autosectask.utility.util_logging import SimpleLogger
from autosectask.utility.util_config import Config
from autosectask.utility.util_datetime import DateUtils

logger = SimpleLogger().get_logger()


class RoutingConfigDAO:

    # 用来读取模板文件YYYY\XX-YYYY-NNNN.ini中的每个配置的字段
    def __init__(self, service_cfg):
        self.__service_cfg = Config(service_cfg)

        # 读取业务服务.ini [default]

        smc_upload = self.__service_cfg.read_section("smc_upload")
        self.__template_path = smc_upload.get("template_path")
        self.__output_path = smc_upload.get("output_path")
        self.__output_file = smc_upload.get("output_file")
        self.__sheet_name = smc_upload.get("sheet_name")
        self.__command = smc_upload.get("command")

        self.__server = self.__service_cfg.read_section("smc_upload.server")

    def get_sheet_name(self):
        return self.__sheet_name

    def get_command(self):
        return self.__command

    def get_server_cfg(self):
        return self.__server

    def get_template_path(self):
        return self.__template_path

    def get_output_path(self):
        return self.__output_path

    def get_output_file(self):
        current_month, previous_month = DateUtils.get_current_and_previous_month()
        return self.__output_file.format(F_CUR_MONTH=current_month)
