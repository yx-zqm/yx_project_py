# -*- coding: utf-8 -*-
# @Author : Wei XiLi (wei.xl@asiainfo-sec.com)
# @Date   : 2018-08-23 14:17:36
# @Memo   : reading config
# @Revision:
#   * 2022-08-14, Wei.xl, 新增word临时文件关闭,解决windows平台问题：PermissionError: [WinError 32] 另一个程序正在使用此文件，进程无法访问。

import os

from mailmerge import MailMerge
from utility.util_logging import SimpleLogger

logger = SimpleLogger().get_logger()


class DocxFS:
    def __init__(self, path):
        self.__path = path

        # 先移动到临时文件
        self.__temp_path = path + '.temp.docx'
        os.rename(path, self.__temp_path)
        self.__doc = MailMerge(self.__temp_path)

    def merge_require(self, requirement_desc):
        logger.info(f"更新需求描述中【{requirement_desc}】...")
        self.__doc.merge(req_desc=requirement_desc)

    def merge_system(self, sysname):
        logger.info(f"更新应用系统名中【{sysname}】...")
        self.__doc.merge(system_name=sysname)

    def merge_rows(self, anchor, anchor_data, test_suite):
        logger.info(f"更新{anchor}清单中...")
        rows = self.gen_rows(anchor, anchor_data, test_suite)
        self.__doc.merge_rows(anchor, rows)

    @staticmethod
    def gen_rows(anchor, anchor_data, suite):
        logger.info(f"生成{anchor}的记录中...")
        rows = []
        for i, case in zip(range(1, len(suite) + 1), suite):
            row = {anchor: str(i), anchor_data: case}
            logger.debug(f"已生成记录中：{row}")
            rows.append(row)
        return rows

    def __enter__(self):
        logger.info(f"opening docx file {self.__path}")
        return self

    def __exit__(self, e_t, e_v, t_b):
        logger.info("writing docx file...")
        self.__doc.write(self.__path)
        if os.path.exists(self.__temp_path):
            logger.info("closing docx file and remove temp file...")
            self.__doc.close()
            os.remove(self.__temp_path)
