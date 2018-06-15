# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# import logging
#
# #日志输入到文件，此定义会把level定义的和高于warn级别的日志写入文件
# logging.basicConfig(filename='logtest.log',level=logging.INFO)
#
# ##只有高于等于warn基本的日志才打印到stdout上
# logging.debug("debug message")
# logging.info("info message")
# logging.warn("warn message")
# logging.error('error message')
# logging.critical('critical message')



import logging
import logging.handlers

LOG_FILE = 'tst.log'

handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5) # 实例化handler
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'

formatter = logging.Formatter(fmt)   # 实例化formatter
handler.setFormatter(formatter)      # 为handler添加formatter

logger = logging.getLogger('tst')    # 获取名为tst的logger
logger.addHandler(handler)           # 为logger添加handler
logger.setLevel(logging.DEBUG)

logger.info('first info message')
logger.debug('first debug message')