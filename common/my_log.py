# -*- coding: utf-8 -*-
# @Time  : 2019/3/23 15:00
# @Author: Tansy_Xiaoming
# @Email : 279244228@qq.com
# @File  : my_log.py
import logging
from class_0325_api_practice_5.common.read_config import ReadConfig
from class_0325_api_practice_5.common import common_path


class MyLog:
    '''从配置文件中读取日志收集器的配置'''
    def __init__(self, configfile=common_path.config_path, logfile=common_path.log_path):
        '''configefile:配置文件地址
           logFile:写入日志文件的地址,默认和当前文件在同一地址下，文件名为logger.log'''
        cf = ReadConfig(configfile)
        self.logger_name = cf.get_str('Log','LogName')
        self.log_level = cf.get_str('Log','LogLevel')
        self.handler_type = cf.get_str('Log','HandlerType')
        self.handler_level = cf.get_str('Log','HandlerLevel')
        self.format = cf.get_str('Log','Format')

        self.logger= logging.getLogger(self.logger_name)  # 创建一个新的日志接收器
        self.logger.setLevel(self.log_level)             # 给日志接收器设置接收等级
        if self.handler_type == 'StreamHandler':         # 根据配置文件中输出渠道的设置，创建不同的输出渠道
            self.handler=logging.StreamHandler()
        else:
            self.handler=logging.FileHandler(logfile,'a',encoding='utf-8')
        self.handler.setLevel(self.handler_level)           # 给输出渠道设置输出等级
        self.handler_format = logging.Formatter(self.format)  # 根据配置生成输出渠道输出模板
        self.handler.setFormatter(self.handler_format)         # 将模板与输出渠道挂接

    def add_log(self,level,msg):
        self.logger.addHandler(self.handler)      # 在调用添加日志方法时才将日志收集器与输出渠道挂接
        if level == 'DEBUG':
            self.logger.debug(msg)
        elif level == 'INFO':
            self.logger.info(msg)
        elif level == 'WARNING':
            self.logger.warning(msg)
        elif level == 'ERROR':
            self.logger.error(msg)
        else:
            self.logger.critical(msg)
        # print(self.logger.handlers)
        self.logger.handlers[0].close()   # 关闭输出渠道
        self.logger.removeHandler(self.handler)    # 在调用添加日志方法结束时将输出渠道移除

    def debug_log(self, msg):
        # 输出debug类型的日志
        self.add_log('DEBUG',msg)

    def info_log(self, msg):
        # 输出info类型的日志
        self.add_log('INFO',msg)

    def warning_log(self, msg):
        '''输出warning类型的日志'''
        self.add_log('WARNING',msg)

    def error_log(self, msg):
        '''输出error类型的日志'''
        self.add_log('ERROR',msg)

    def critical_log(self, msg):
        '''输出critical类型的日志'''
        self.add_log('CRITICAL',msg)


if __name__ == '__main__':
    logger = MyLog()
    logger.debug_log('debug msg')
    logger.critical_log('critical msg')