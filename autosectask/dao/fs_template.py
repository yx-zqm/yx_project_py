from autosectask.utility.util_logging import SimpleLogger
import os
import shutil

logger = SimpleLogger().get_logger()


class TemplateDAO:

    def __init__(self, temp_dict, path_dict):
        self.__temps = temp_dict
        self.__paths = path_dict

    def copy_files(self):
        logger.info("[2] 根据模板文件创建工单相关文件...")
        for key, temp_path in self.__temps.items():
            logger.debug(self.__temps)
            logger.debug(self.__paths)
            self.copy_template(temp_path, self.__paths[key])

    @staticmethod
    def copy_template(source, target):
        if os.path.exists(source):
            logger.info(f"copy file from [{os.path.basename(source)}] to [{target}]")
            shutil.copyfile(source, target)
        else:
            logger.error(f"[{source}]模板文件不存在, 无法复制.")
