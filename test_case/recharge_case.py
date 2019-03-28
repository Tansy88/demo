# -*- coding: utf-8 -*-
# @Time  : 2019/3/25 15:10
# @Author: Tansy_Xiaoming
# @Email : 279244228@qq.com
# @File  : recharge_case.py
from class_0325_api_practice_5 import test_case as T

wb = T.DoExcel('Recharge')
test_data = wb.read_all_data()
url = T.ReadConfig().get_str('TestData','URL') + '/member/recharge'
login_url = T.ReadConfig().get_str('TestData','URL') + '/member/login'


@T.ddt
class RechargeCase(T.unittest.TestCase):
    '''实现充值的用例逻辑'''
    def setUp(self):
        self.my_logger = T.MyLog()
        self.db = T.CheckDB(session='DBConnect_QA')
        self.my_logger.info_log('---------充值用例开始执行----------')

    def tearDown(self):
        self.my_logger.info_log('-----------充值用例执行结束---------')

    @T.data(*test_data)
    @T.unpack
    def test_recharge(self,caseId,method,params,expectedResult,sql,**kwargs):
        cookie = T.HttpRequest().send_request(url=login_url, method='get',
                                              params={'mobilephone': T.CommonData.register_mobile,
                                                      'pwd': T.CommonData.register_pwd}).cookies  # 使用已注册的手机号登录获取cookie
        setattr(T.CommonData, 'cookie', cookie)  # 将cookie存入全局变量
        params = T.replace_by_re(params) # 使用正则表达式对可替换的值进行替换
        self.my_logger.info_log('第{}条充值用例正在执行中，请求参数为{}'.format(caseId,params))
        actual_result = T.HttpRequest().send_request(url=url,method=method,params=eval(params),
                                                     cookies=T.CommonData.cookie).json() # 发送请求并获取响应正文
        if sql is not None:         # 如果有sql的话，就去查询sql并将结果写入全局变量中
            sql = T.replace_by_re(sql) # 使用正则表达式对sql进行替换
            leave_amount = self.db.get_one_result(sql)[0]
            setattr(T.CommonData, 'leave_amount', str(leave_amount))
            self.my_logger.debug_log('充值后的金额为{}'.format(leave_amount))
        else:
            actual_result.pop('data')    # 如果没有需要替代的数据，则把data去掉不进行比较
        expectedResult = eval(T.replace_by_re(expectedResult))  # 将期望进行替换并转换为字典格式
        try:
            self.assertDictEqual(actual_result,expectedResult)
            test_result = 'Pass'
        except Exception as e:
            test_result = 'Fail'
            self.my_logger.error_log('期望结果与实际结果不一致，错误为{}'.format(e))
            raise e
        finally:
            actual_result = T.json.dumps(actual_result, ensure_ascii=False)  # 将响应转换为字符串格式
            wb.update_excel(int(caseId) + 1, 7, actual_result)
            wb.update_excel(int(caseId) + 1, 8, test_result)  # 将结果写回excel中


if __name__ == '__main__':
    T.unittest.main()


