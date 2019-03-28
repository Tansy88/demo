# -*- coding: utf-8 -*-
# @Time  : 2019/3/23 17:57
# @Author: Tansy_Xiaoming
# @Email : 279244228@qq.com
# @File  : common_data.py
import re
from class_0325_api_practice_5.common.read_config import ReadConfig

cf = ReadConfig()


class CommonData:
    '''存放公共参数'''
    cookie = None
    register_mobile=cf.get_str('Regular_Expression','register_mobile')
    register_pwd = cf.get_str('Regular_Expression','register_pwd')


default_p = cf.get_str('Regular_Expression','Format')


def replace_by_re(target,p=default_p):
    while re.search(p,target):
        key = re.search(p,target).group(1)
        re_str = getattr(CommonData,key)
        target = re.sub(p,re_str,target,count=1)
    return target


if __name__ == '__main__':
    # setattr(CommonData,'end_leave_amount','123456')
    # print(CommonData.end_leave_amount)
    target = "{'mobile':'${register_mobile}','pwd':'${register_pwd}'}"
    r = replace_by_re(target)
    print(r)
    print(target)