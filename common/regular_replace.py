# -*- coding: utf-8 -*-
# @Time  : 2019/3/26 15:47
# @Author: Tansy_Xiaoming
# @Email : 279244228@qq.com
# @File  : regular_replace.py
import re

default_re = '\$.*?\}+?'   # 根据自己的规则，写的默认正则表达式


class ReplaceByRe:
    '''根据传进来的正则表达式，替换字符串和原字符串进行判断和替换'''
    # def __init__(self,old_str,p=default_re):
    #     '''初始化函数中需传入正则表达式和原字符串'''
    #     self.p = p
    #     self.old_str = old_str

    def has_sub_str(self,old_str,p=default_re):
        '''判断是否含有正则表达式所代表的子字符串，并返回结果'''
        m = re.findall(p,old_str)
        if len(m)> 0:
            # print('当前字符串中包含正则表达式代表的字字符串')
            return m
        else:
            return None

    def replace_all_str(self,old_str,*args,p=default_re):
        '''字符串中有多个字符串需要替换不同值，将待替换的值按顺序传入此函数中'''
        try:
            new_str = old_str
            for str_item in args:
                new_str = re.sub(p,str_item,new_str,count=1)
            return new_str
        except Exception as e:
            print('此字符串中无可替换字符串,错误为{}'.format(e))
            return None

    def replace_one_str(self,sub_str,old_str,p=default_re):
        '''字符传中所有匹配的子字符串，都要替换成同一个值'''
        try:
            new_str = re.sub(p,sub_str,old_str,count=0)
            return new_str
        except Exception as e:
            print('此字符串中无可匹配字符串,错误为{}'.format(e))
            return None



if __name__ == '__main__':
    target = "{'mobile':'${mobile}','pwd':'${pwd}'}"
    s = ReplaceByRe().replace_all_str(target,'15168392262','123456')
    print(s)




