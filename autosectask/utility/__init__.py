import logging
import os
from autosectask.utility.util_logging import SimpleLogger

# set up project debug level here
logger = SimpleLogger(level=logging.DEBUG).get_logger()
logger.info(f'Set up application log level here: {os.path.join(os.getcwd(), __file__)}')

# 以*导入时，package内的module是受__init__.py限制的(__all__)。
__all__ = ['singleton', 'util_logging', 'util_conn_oracle', 'util_config', 'util_conn_sftp']

# logger.debug(f'Loading utilities entities: {__all__}')

'''
其实，主要是用到Python的包的概念，而__init__.py在包里起着重要作用。要弄明白这个问题，首先要知道，Python在执行import语句时，到底进行了什么操作，按照python的文档，它执行了如下操作：
    第1步，创建一个新的，空的module对象（它可能包含多个module）
    第2步，把这个module对象插入sys.module中
    第3步，装载module的代码（如果需要，首先必须编译）
    第4步，执行新的module中对应的代码。
'''
