# -*- coding: utf-8 -*-
# @Time  : 2019/3/26 10:32
# @Author: Tansy_Xiaoming
# @Email : 279244228@qq.com
# @File  : bidloan_case.py
from class_0325_api_practice_5 import test_case as T


wb = T.DoExcel('BidLoan')
test_data = wb.read_all_data()
url = T.ReadConfig().get_str('TestData','URL') + '/member/bidLoan'
login_url = T.ReadConfig().get_str('TestData','URL') + '/member/login'


@T.ddt
class BidLoanCase(T.unittest.TestCase):
    '''定义投资的用例实现'''
    def setUp(self):
        self.my_logger = T.MyLog()
        self.db = T.CheckDB(session='DBConnect_QA')
        self.my_logger.info_log('---------投资用例开始执行----------')

    def tearDown(self):
        self.my_logger.info_log('---------投资用例结束执行-----------')

    @T.data(*test_data)
    @T.unpack
    def test_bidloan(self,caseId,method,params,expectedResult,sql,**kwargs):
        cookie = T.HttpRequest().send_request(url=login_url, method='get',
                                              params={'mobilephone': T.CommonData.register_mobile,
                                                      'pwd': T.CommonData.register_pwd}).cookies  # 使用公共参数中的手机号和密码进行登录
        setattr(T.CommonData, 'cookie', cookie)  # 将cookie存入全局变量
        if sql is not None:  # 有需要执行的sql就去执行
            sql = eval(sql)               # 将sql从字符串还原到字典格式
            loanid = self.db.get_one_result(sql['sql_1'])[0]  # 字典中sql_1对应的是loanid的查询语句
            setattr(T.CommonData,'loanId',str(loanid))  # 将参数写入公共参数中
            sql_2 = T.replace_by_re(sql['sql_2']) # 使用正则表达式对数据进行替换
            memberid = self.db.get_one_result(sql_2)[0]     # 获取当前登录账号的memberId
            setattr(T.CommonData,'memberId',str(memberid))
            before_amount = self.db.get_one_result(sql_2)[1]  # 获取当前登录账号的起始余额
            setattr(T.CommonData,'before_amount',before_amount)
        params = T.replace_by_re(params)  # 将params中的参数进行替换
        self.my_logger.info_log('正在执行第{}条用例，参数为{}'.format(caseId, params))
        actual_result = T.HttpRequest().send_request(url=url, method=method,
                                                     params=eval(params), cookies=cookie).json()   # 替换完成后发起请求
        if sql is not None:
            sql_2 = T.replace_by_re(sql['sql_2'])  # 使用正则表达式对数据进行替换
            after_amount = self.db.get_one_result(sql_2)[1]  # 获取当前登录账号的当前余额
            expected_amount = before_amount - eval(params)['amount']  # 计算期望余额
            try:
                self.assertEqual(after_amount,expected_amount)       # 在进行接口返回对比前，先进行数据校验
                self.my_logger.debug_log('投资前金额为{}，投资后期望金额为{}，投资后实际金额为{}'
                                         .format(before_amount,expected_amount,after_amount))
            except Exception as e:
                self.my_logger.error_log('充值后，期望余额和数据库中余额不一致，期望余额为{}，实际余额为{},错误为{}'
                                         .format(expected_amount,after_amount,e))
                raise e

        actual_result.pop('data')
        try:
            self.assertDictEqual(actual_result,eval(expectedResult))
            self.my_logger.info_log('实际结果与期望结果一致')
            test_result = 'Pass'
        except Exception as e:
            self.my_logger.error_log('实际结果与期望结果不一致，错误为{}'.format(e))
            test_result = 'Fail'
            raise e
        finally:
            actual_result = T.json.dumps(actual_result,ensure_ascii=False)
            wb.update_excel(int(caseId)+1,7,actual_result)
            wb.update_excel(int(caseId)+1,8,test_result)


if __name__ == '__main__':
    T.unittest.main()



