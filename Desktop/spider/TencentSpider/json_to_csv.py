#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time : 18-4-18 下午4:01 
# @Author : TangSengLoveRejoiceShampoo  
# @File : json_to_csv.py 
# @Software: PyCharm

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


import json
import csv



def json_to_csv():
    json_file = open("tencent.json","r")
    csv_file = open("tencent.csv","w")

    #读取json文件的字符串，并返回Python数据类型
    item_list = json.load(json_file)

    #创建一个csv文件读写操作对象，数据读写和文件交互
    csv_writer = csv.writer(csv_file)

    #keys = 返回所有键的列表    [a, b, c]
    #values 返回所有值的列表    [1, 2, 3]
    #items 返回所有键值对的列表 [(a, 1), (b, 2), (c, 3)]

    #表头是一层嵌套的列表
    sheet_head = item_list[0].keys()
    #表数据是两层嵌套的列表
    sheet_data = [item.values() for item in item_list]

    #先写一行表头部分
    csv_writer.writerow(sheet_head)
    #再写多行表数据部分
    csv_writer.writerows(sheet_data)

    #关闭文件，保存数据
    csv_file.close()
    json_file.close()

if __name__ == "__main__":
    json_to_csv()