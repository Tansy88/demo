# -*- coding: utf-8 -*-
# @Time  : 2019/3/25 9:41
# @Author: Tansy_Xiaoming
# @Email : 279244228@qq.com
# @File  : login_case.py
from class_0325_api_practice_5 import test_case as T

wb = T.DoExcel('Login')
test_data = wb.read_all_data()
url = T.ReadConfig().get_str('TestData','URL') + '/member/login'


@T.ddt
class LoginCase(T.unittest.TestCase):
    '''定义登录用例的逻辑'''
    def setUp(self):
        self.my_logger = T.MyLog()
        self.my_logger.info_log('-------登录用例开始执行了-------')
        print('-----------登录用例开始执行了-----------')

    def tearDown(self):
        # self.my_logger = MyLog()
        self.my_logger.info_log('--------登录用例执行结束了--------')
        print('-----------登录用例执行结束了-----------')

    @T.data(*test_data)
    @T.unpack
    def test_login(self,caseId,method,params,expectedResult,**kwargs):
        params = T.replace_by_re(params) # 使用正则表达式进行替换
        self.my_logger.info_log('正在执行第{}条用例，参数为{}'.format(caseId,params))
        actual_result = T.HttpRequest().send_request(url=url,params=eval(params),method=method).json()
        actual_result.pop('data')
        try:
            self.assertDictEqual(actual_result,eval(expectedResult))
            test_result = 'Pass'
        except Exception as e:
            self.my_logger.error_log('实际结果与期望结果一致，错误为{}'.format(e))
            test_result = 'Fail'
            raise e
        finally:
            actual_result = T.json.dumps(actual_result, ensure_ascii=False)  # 将响应转换为字符串格式
            wb.update_excel(int(caseId) + 1, 7, actual_result)
            wb.update_excel(int(caseId) + 1, 8, test_result)  # 将结果写回excel中


if __name__ == '__main__':
    T.unittest.main()