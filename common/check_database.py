# -*- coding: utf-8 -*-
# @Time  : 2019/3/23 15:06
# @Author: Tansy_Xiaoming
# @Email : 279244228@qq.com
# @File  : check_database.py
import mysql.connector
from class_0325_api_practice_5.common.read_config import ReadConfig
from class_0325_api_practice_5.common import common_path


class CheckDB:
    '''根据DB设置或配置文件中DB设置链接数据库，并进行数据查询与输出'''
    configfile = common_path.config_path

    def __init__(self,host='127.0.0.1',port=3306,user='',pwd='',database='',configfile=configfile,session=None):
        '''可以使用数据库链接信息或配置文件直接初始化数据库连接对象'''
        if configfile is not None: # 如果存在配置文件，则按照配置文件去读取连接信息
            cf = ReadConfig(configfile)
            self.host = cf.get_str(session,'Host') # 此处将配置文件中option写死为Host
            self.port = cf.get_str(session,'Port')
            self.user = cf.get_str(session,'UserName')
            self.pwd = cf.get_str(session,'Pwd')
            self.database = cf.get_str(session,'Database')
        else:
            self.host = host
            self.port = port
            self.user = user
            self.pwd = pwd
            self.database=database

    def get_one_result(self, sql):
        '''运行sql并返回第一个结果'''
        try:
            db = mysql.connector.connect(host=self.host, port=self.port, user=self.user,
                                         passwd=self.pwd, database=self.database)
        except Exception as e:
            print('数据库连接错误，错误为{}'.format(e))  # 数据库连接错误时，记录错误
            raise e
        else:  # 只有数据库正常连接时，才开始执行sql
            try:
                cursor = db.cursor()
                cursor.execute(sql)
                res = cursor.fetchone()
            except Exception as e:  # 数据库查询错误时，记录错误
                print('数据库查询出错啦，错误是{}'.format(e))
                res = None
                raise e
            finally:
                db.close()  # 无论查询是否成功，都要关闭数据库连接
                return res  # 返回数据类型为元组,没有查询到数据的话返回None

    def get_all_result(self, sql):
        '''运行一个sql并返回所有结果'''
        try:
            db = mysql.connector.connect(host=self.host, port=self.port, user=self.user,
                                         passwd=self.pwd, database=self.database)

        except Exception as e:
            print('数据库连接错误，错误为{}'.format(e))  # 数据库连接错误时，记录错误
            raise e
        else:  # 只有数据库正常连接时，才开始执行sql
            try:
                cursor = db.cursor()
                cursor.execute(sql)
                res = cursor.fetchone()
            except Exception as e:  # 数据库查询错误时，记录错误
                print('数据库查询出错啦，错误是{}'.format(e))
                res = None
                raise e
            finally:
                db.close()  # 无论查询是否成功，都要关闭数据库连接
                return res  # 返回数据类型为列表，列表中数据类型为元组


if __name__ == '__main__':
    # db = CheckDB(user='ellabook',pwd='Ellabook@13579',host='47.98.119.49',database='ellabook_new',configfile=None)
    db = CheckDB(configfile=r'D:\PythonTest\class_0325_api_practice_5\config_file\api_config.conf',session='DBConnect_QA')
    sql = "select LeaveAmount from member where MobilePhone = '15168392262'"
    print(str(db.get_one_result(sql)[0]))
    # db.get_one_reslut()


