# -*- coding: utf-8 -*-
# @Time  : 2019/3/23 15:00
# @Author: Tansy_Xiaoming
# @Email : 279244228@qq.com
# @File  : http_request.py
import requests
from class_0325_api_practice_5.common.do_excel import DoExcel


class HttpRequest:
    '''根据传入的方法去发送请求并返回结果'''

    def send_request(self,url,method,params,**kwargs):
        if method.lower() == 'get':       # 如果传入方法是get请求，就去调用get方法
            # print('----------正在进行get请求-----------')
            result = requests.get(url,params=params,**kwargs)
        elif method.lower() == 'post':   # 如果是post请求，就调用post方法
            try:
                result = requests.post(url,data=params,**kwargs)
            except Exception as e:
                print('传入请求参数类型不对，请求参数类型为{}'.format(type(params)))
                result = None
        else:
            print('请输入正确的请求方法')
        return result


if __name__ == '__main__':
    # res = HttpRequest().send_request(url='http://47.107.168.87:8080/futureloan/mvc/api/member/register', method='post',
    #                                  params={'mobilephone':'15168392262','pwd':'123456'})
    register_tel = DoExcel('Tel').read_one_data(3, 2)
    register_pwd = DoExcel('Tel').read_one_data(3, 3)
    print(register_tel)
    params = {'mobilephone': register_tel, 'pwd': register_pwd}
    print(params)
    res = HttpRequest().send_request(url='http://47.107.168.87:8080/futureloan/mvc/api/member/login',
                                     method='post', params={'mobilephone':register_tel,'pwd':register_pwd})
    cookies = res.cookies
    # print(cookies)
    # params = {'mobilephone':'14168392262','amount':'123456'}
    # print(type(params))
    # res_1 = HttpRequest().send_request('http://47.107.168.87:8080/futureloan/mvc/api/member/recharge','post',{'mobilephone':'14168392262','amount':'123456'},cookies=cookies)
    # print(res_1.text)
    # # print(res.json())
    # 加标请求
    res = HttpRequest().send_request(url='http://47.107.168.87:8080/futureloan/mvc/api/loan/add', method='post',
                                     params={'memberId':1123390,'title':'Tansy的测试项目','amount':1000,'loanRate':10.0,'loanTerm':6,'LoanDateType':2,'repaymemtWay':4,'biddingDays':4},cookies=cookies)
    print(res.text)
    # 审核请求
    # res = HttpRequest().send_request(url='http://47.107.168.87:8080/futureloan/mvc/api/loan/audit', method='post',
    #                                  params={'id': 18474, 'status': 4},
    #                                  cookies=cookies)
    # print(res.text)
    # 投资请求
    # res = HttpRequest().send_request(url='http://47.107.168.87:8080/futureloan/mvc/api/member/bidLoan', method='post',
    #                                  params={'loanId': 18474, 'amount': 100,'memberId':1123405,'password':'123456'},
    #                                  cookies=cookies)
    # print(res.text)
