# -*- coding: utf-8 -*-
# @Time  : 2019/3/25 11:10
# @Author: Tansy_Xiaoming
# @Email : 279244228@qq.com
# @File  : run_case.py
import unittest
import HTMLTestRunnerNew
from class_0325_api_practice_5.common import common_path
from class_0325_api_practice_5.common.read_config import ReadConfig
from class_0325_api_practice_5.test_case import register_case
from class_0325_api_practice_5.test_case import login_case
from class_0325_api_practice_5.test_case import recharge_case
from class_0325_api_practice_5.test_case import bidloan_case


run_flag = ReadConfig().get_str('TestSet','RunCase') # 读取运行用例配置
suite = unittest.TestSuite()
loader = unittest.TestLoader()
if run_flag == 'ALL':
    suite.addTests(loader.loadTestsFromModule(register_case))
    suite.addTests(loader.loadTestsFromModule(login_case))
    suite.addTests(loader.loadTestsFromModule(recharge_case))
    suite.addTests(loader.loadTestsFromModule(bidloan_case))
else:
    run_flag = eval(run_flag)
    for item in run_flag:              # 根据用例配置，加载不同的用例实现类
        if item == 'Register':
            run_case = getattr(register_case, 'RegisterCase') # 将字符串转换为class类型
        elif item == 'Login':
            run_case = getattr(login_case, 'LoginCase')
        elif item == 'Recharge':
            run_case = getattr(recharge_case,'RechargeCase')
        elif item == 'BidLoan':
            run_case = getattr(bidloan_case,'BilLoanCase')
        else:
            run_case = None
        suite.addTests(loader.loadTestsFromTestCase(run_case))
with open(common_path.report_path, 'wb') as file:   # 每次运行输出不同的测试报告
    title = ReadConfig().get_str('Report', 'Title')  # 从配置文件中读取，测试报告的配置
    description = ReadConfig().get_str('Report', 'Description')
    tester = ReadConfig().get_str('Report', 'Tester')
    runner = HTMLTestRunnerNew.HTMLTestRunner(stream=file, verbosity=2, title=title,
                                              description=description, tester=tester)
    runner.run(suite)
