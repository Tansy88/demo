# -*- coding: utf-8 -*-
# @Time  : 2019/3/23 16:33
# @Author: Tansy_Xiaoming
# @Email : 279244228@qq.com
# @File  : register_case.py
from class_0325_api_practice_5 import test_case as T

wb = T.DoExcel('Register')    # 实例化一个excel对象
test_data = wb.read_all_data() # 读取注册的需要运行的全部用例
url = T.ReadConfig().get_str('TestData','URL') + '/member/register'  # 根绝配置文件定义的URL去调对应地址的注册接口


@T.ddt
class RegisterCase(T.unittest.TestCase):
    '''定义注册用例的逻辑'''
    def setUp(self):
        print('---------注册用例开始执行了----------')
        self.my_logger = T.MyLog()
        self.db = T.CheckDB(session='DBConnect_QA')
        self.new_tel = T.DoExcel('Tel').read_one_data(2, 2)

    def tearDown(self):
        print('----------注册用例执行结束了----------')

    @T.data(*test_data)
    @T.unpack
    def test_register(self,caseId,method,params,expectedResult,sql,**kwargs):
        if sql is not None:    # 如果存在sql的话，就去替换并执行sql
            while True:        # 循环执行
                setattr(T.CommonData, 'unregister_mobile', str(self.new_tel)) # 每次循环都把当时的手机号写入公共参数中
                sql_1 = T.replace_by_re(sql)   # 使用公共参数中的变量进行替换
                res = self.db.get_one_result(sql_1)      # 查询excel中的手机号是否被注册过
                if res is None:                        # 如果没被注册
                    T.DoExcel('Tel').update_excel(2, 2, self.new_tel + 1)  # 就将手机号+1写回excel中并跳出循环
                    break
                else:
                    self.new_tel += 1  # 当查询到已注册时就将数据加1 并再次循环
        params = T.replace_by_re(params)
        self.my_logger.info_log('正在执行第{}条注册用例，参数为{}'.format(caseId,params))
        actual_result = T.HttpRequest().send_request(url=url,method=method,params=eval(params)).json() # 去发起http请求
        actual_result.pop('data') # 注册用例中，data数据无意义，可以不进行比较
        try:
            self.assertDictEqual(actual_result,eval(expectedResult))  # 将实际结果与期望结果进行对比
            if sql is not None:          # 断言成功后检查是否有sql需要查询
                sql = T.replace_by_re(sql) # 使用正则表达式进行替换，并判断注册完成后数据中是否有增加数据
                res = self.db.get_one_result(sql)
                try:
                    self.assertEqual(len(res),1)    # 比较是否已查询到此注册账号
                    test_result = 'Pass'         # 查询到结果为Pass
                    self.my_logger.info_log('{}已注册并保存到数据库中'.format(self.new_tel))
                except Exception as e:
                    test_result = 'Fail'    # 未查询到结果为Fail
                    self.my_logger.error_log('接口返回正确，但数据未插入数据库中')
                    raise e
            else:
                test_result = 'Pass'   # 不需要查询数据库时，结果直接为Pass
        except Exception as e:     # 断言比较错误时，直接不进行数据库查询,直接Fail
            test_result = 'Fail'
            self.my_logger.error_log('接口返回不一致，错误为{}'.format(e))
            raise e
        finally:
            actual_result = T.json.dumps(actual_result,ensure_ascii=False) # 将响应转换为字符串格式
            wb.update_excel(int(caseId)+1,7,actual_result)
            wb.update_excel(int(caseId)+1,8,test_result)  # 将结果写回excel中


if __name__ == '__main__':
    T.unittest.main()



