#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time : 18-4-18 下午3:35 
# @Author : TangSengLoveRejoiceShampoo  
# @File : hr_tencent_spider.py 
# @Software: PyCharm

from bs4 import BeautifulSoup
import requests
import time
import json
import random


class TencentSpider(object):
    def __init__(self):
        self.start_url = "https://hr.tencent.com/position.php?&start=0"
        self.headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}
        self.item_list = []
        self.page = 0

    def send_request(self,url):
        response = requests.get(url,headers=self.headers)
        return response


    def parse_page(self,response):
        html = response.content
        soup = BeautifulSoup(html,"lxml")
        #获取十个职位的节点列表
        node_list = soup.select(".even, .odd")

        #迭代每个节点，取出每条职位的数据，存储到item里
        for node in node_list:
            item = {}
            item['position_name'] = node.select("td a")[0].get_text()
            item["position_link"] = "https://hr.tencent.com/" + node.select("td a")[0].get("href")
            item["position_type"] = node.select("td")[1].get_text()
            item["people_number"] = node.select('td')[2].get_text()
            item["work_location"] = node.select('td')[3].get_text()
            item["publish_times"] = node.select('td')[4].get_text()

            self.item_list.append(item)
        #如果找到，则返回数据，如果没有找到则返回None
        if soup.find("a",{"class":"noactive","id":"next"}):
            return None
        else:
            #获取下一页链接
            next_link = "https://hr.tencent.com/" + soup.find("a", {"id" : "next"}).get("href")
            print next_link
            return next_link

    def write_page(self):
        json.dump(self.item_list,open("tencent.json","w"))


    def main(self):
        #第一页的url地址请求，程序的入口
        response = self.send_request(self.start_url)
        while self.page < 100:
            next_link = self.parse_page(response)
            if next_link is None:
                print "到了最后一页"
                break
            else:
                try:
                    response = self.send_request(next_link)
                except:
                    print "[ERROR]:请求处理失败" + next_link
                time.sleep(random.randint(1,3))
            self.page += 10
        self.write_page()



if __name__ == "__main__":
    spider = TencentSpider()
    spider.main()



