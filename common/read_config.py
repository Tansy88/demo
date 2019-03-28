# -*- coding: utf-8 -*-
# @Time  : 2019/3/23 11:20
# @Author: Tansy_Xiaoming
# @Email : 279244228@qq.com
# @File  : read_config.py
from configparser import ConfigParser
from class_0325_api_practice_5.common import common_path


class ReadConfig:
    '''读取配置文件'''
    def __init__(self,file=common_path.config_path):
        self.cf = ConfigParser()
        self.cf.read(file,encoding='utf-8')

    def get_str(self,section,option):
        '''读取字符串类型的数据'''
        try:
            res = self.cf.get(section,option)
        except Exception as e:
            print('读取字符串时报错，错误为{}'.format(e))
            raise e
        else:
            return res                        # 报错时返回None

    def get_others(self,section,option):
        '''读取元组、字典、列表类型数据、整数和浮点数'''
        try:
            res = eval(self.cf.get(section,option))
        except Exception as e:
            print('读取给字符串数据时报错，错误为{}'.format(e))
            raise e
        else:
            return res


if __name__ == '__main__':
    cf = ReadConfig()
    print(cf.get_str('DBConnect_QA','Host'))
    print(type(cf.get_str('TestSet','RunCase')))
    print(cf.get_others('TestSet','RunCase'))
    print(type(cf.get_others('TestSet','RunCase')))
