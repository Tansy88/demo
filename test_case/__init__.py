# -*- coding: utf-8 -*-
# @Time  : 2019/3/23 16:33
# @Author: Tansy_Xiaoming
# @Email : 279244228@qq.com
# @File  : __init__.py.py
import unittest
from ddt import ddt,data,unpack
import json
from class_0325_api_practice_5.common.do_excel import DoExcel
from class_0325_api_practice_5.common.my_log import MyLog
from class_0325_api_practice_5.common.http_request import HttpRequest
from class_0325_api_practice_5.common.check_database import CheckDB
from class_0325_api_practice_5.common.read_config import ReadConfig
from class_0325_api_practice_5.common.common_data import CommonData
from class_0325_api_practice_5.common.common_data import replace_by_re