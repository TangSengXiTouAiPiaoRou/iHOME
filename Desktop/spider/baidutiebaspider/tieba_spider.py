#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time : 18-4-16 下午3:31 
# @Author : TangSengLoveRejoiceShampoo  
# @File : tieba_spider.py 
# @Software: PyCharm


import requests
from lxml import etree
import os
import urllib


class TiebaSpider(object):
    '''
    爬取百度贴吧的爬虫程序
    '''
    def __init__(self):
        '''初始化方法，设置base_url,headers等'''
        self.base_url = "http://tieba.baidu.com"
        self.headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}

        self.tieba_name = raw_input("请输入要爬取的贴吧的名字")
        self.begin_page = int(raw_input("请输入起始页"))
        self.end_page = int(raw_input("请输入结束页"))


    def send_request(self,url,query={}):
        #发送请求获取响应，并返回响应
        response = requests.get(url,params=query,headers=self.headers)
        return response


    def parse_page(self,response):
        #获取每一页中帖子的链接，并返回
        html = response.content

        html_obj = etree.HTML(html)

        page_link_list = html_obj.xpath("//a[@class='j_th_tit ']/@href")

        return page_link_list


    def parse_image(self,response):
        #获取每一个帖子中图片的链接，并返回
        html = response.content

        html_obj = etree.HTML(html)

        image_link_list = html_obj.xpath("//img[@class='BDE_Image']/@src")

        return image_link_list



    def write_image(self,image_link,filename):
        '''
        将图片写入磁盘文件
        :param response:
        :param filename:
        :return:
        '''
        print "[TIPS]:正在保存图片" + filename
        # with open(filename,'wb') as f:
        #     f.write(response.content)

        _path = os.getcwd()
        new_path = _path + "/" + self.tieba_name + "/"
        if not os.path.isdir(new_path):
            os.mkdir(new_path)

        def callback(dbnum, dbsize, size):
            '''''回调函数
            dbnum: 已经下载的数据块
            dbsize: 数据块的大小
            size: 远程文件的大小
            '''
            percent = 100.0 * dbnum * dbsize / size
            if percent > 100:
                percent = 100
            print "%.2f%%" % percent


        urllib.urlretrieve(image_link,new_path + '%s' % filename,callback)



    def main(self):
        #处理业务逻辑的调度函数
        for page in range(self.begin_page,self.end_page + 1):
            pn = (page - 1) * 50
            query ={"kw":self.tieba_name,"pn":pn}
            url = self.base_url + "/f?"
            try:
                #处理每个帖子列表页的请求
                response = self.send_request(url,query)

                #每个帖子的请求处理
                page_link_list = self.parse_page(response)
                for page_link in page_link_list:
                    url = self.base_url + page_link
                    try:
                        response = self.send_request(url)
                        image_link_list = self.parse_image(response)
                        #每个图片的请求处理
                        for image_link in image_link_list:
                            # response = self.send_request(image_link
                            try:
                                self.write_image(image_link,image_link[-15:])
                            except:
                                print "[ERROR]:图片解析失败" + image_link
                    except:
                        print "[ERROR]:帖子解析失败" + page_link
            except Exception as e:
                print "[ERROR]:帖子列表页解析失败"
                print e
        print "[TIPS]:图片下载结束，快去欣赏吧！"

if __name__ == "__main__":

    tieba_spider = TiebaSpider()
    tieba_spider.main()