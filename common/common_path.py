# -*- coding: utf-8 -*-
# @Time  : 2019/3/23 10:46
# @Author: Tansy_Xiaoming
# @Email : 279244228@qq.com
# @File  : common_path.py
import os
import time

current_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) # 输出当前时间
base_path = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
excel_path = os.path.join(base_path,'test_data','前程贷_用例.xlsx')
log_name = 'Log' + current_time + '.log'
log_path = os.path.join(base_path,'test_result','test_log',log_name)
report_name = current_time + '测试报告.html'
report_path = os.path.join(base_path,'test_result','test_report',report_name)
config_path = os.path.join(base_path,'config_file','api_config.conf')

if __name__ == '__main__':
    print(base_path)
    print(excel_path)
    print(log_path)
    print(report_path)
    print(config_path)