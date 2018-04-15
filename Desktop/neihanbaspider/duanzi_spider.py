#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time : 18-4-15 下午7:39 
# @Author : TangSengLoveRejoiceShampoo  
# @File : duanzi_spider.py 
# @Software: PyCharm


import requests
import re


class NeiHanSpider(object):
    def __init__(self):
        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}
        self.base_url = "http://www.neihan8.com/article/list_5_"
        #页码
        self.page = 1
        #正则匹配网页文本
        self.pattern_page = re.compile('<div class="f18 mb20">(.*?)</div>',re.S)
        # self.pattern_result = re.compile("<.*?>|&.*?;|\s|　")
        # 用来处理无用字符
        # <.*?> 表示标签
        # &.*?; 表示匹配HTML实体字符
        # \s 表示匹配空白字符
        # u"\u3000".encode("utf-8") 表示匹配全角中文空格
        self.pattern_result = re.compile("<.*?>|&.*?;|\s|" + u"\u3000".encode("utf-8"))

    def send_request(self,url):
        #发送请求，获取网页html并转为utf-8字符串
        print "[INFO]正在发送请求" + url
        proxy = {"http":"http://maozhaojun:ntkn0npx@114.67.224.167:16819"}
        html = requests.get(url,headers=self.headers,proxies=proxy).content
        html = html.decode("gbk").encode("utf-8")
        return html


    def parse_page(self,html):
        #提取所有段子内容，返回列表
        result_list = self.pattern_page.findall(html)
        return result_list


    def write_page(self,result_list):
        with open("duanzi.txt","a") as f:
            f.write("第" + str(self.page) + "页:\n")
            for result in result_list:
                #迭代每一页的每条段子，并去除无用字符
                content = self.pattern_result.sub("",result)
                print "[INFO]正在保存文本"
                f.write(content + "\n")
            f.write("\n\n")


    def main(self):
        while True:
            full_url = self.base_url + str(self.page) + ".html"
            try:
                html = self.send_request(full_url)
                result_list = self.parse_page(html)
                self.write_page(result_list)
                self.page += 1
            except Exception as e:
                print e
                print "[ERROR]:页面抓取失败" + full_url

            command = raw_input("按回车键继续爬取，退出输入q")
            if command == "q":
                print "[INFO]:谢谢使用，再见"
                break
if __name__ == "__main__":
    spider = NeiHanSpider()
    spider.main()
