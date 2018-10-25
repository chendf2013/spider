import re

import requests
import json
from lxml import etree


class BaiDu(object):

    def __init__(self, name):
        self.total_page = None
        self.tieba_name = name
        self.headers = {
            "User-Agent": "Mozilla/5.0 (compatible; MSIE 10.0; Windows Phone 8.0; Trident/6.0; IEMobile/10.0; ARM; Touch; NOKIA; Lumia 520)"
        }
        self.common_tieba_url = "https://tieba.baidu.com/mo/q---EBDD98DD1001882FCB6C56EFABE26A36:FG=1--1-3-0----wapp_1540457754558_774/m?word={}&tn6=bdISP&tn4=bdKSW&tn7=bdPSB&lp=1050&sub4=进吧"  # (贴吧名称)
        self.common_index_url = "https://tieba.baidu.com/mo/q---EBDD98DD1001882FCB6C56EFABE26A36:FG=1--1-3-0----wapp_1540457754558_774/m?kw={}&lp=5011&lm=&pn={}"  # （贴吧名称，分页，每页十条）
        # self.index_url_list = []
        # self.profile_url_list = []

    def get_requests(self, url):
        response = requests.get(url=url, headers=self.headers)
        return response

    def get_data_use_xpath(self, xpath_str, response):
        el_obj = etree.HTML(response.content)
        ret_list = el_obj.xpath(xpath_str)
        return ret_list if ret_list else None

    def save_data(self, dict):
        with open("{}贴吧的标题与之对应的详情页链接".format(self.tieba_name), "w", encoding="utf-8") as file:
            file.write(json.dumps(dict, ensure_ascii=False, indent=2))

    def run(self):
        """
        主要逻辑
        """

        # 获取页数
        total_page_response = self.get_requests(self.common_tieba_url.format(self.tieba_name))
        self.total_page = self.get_data_use_xpath('//form//div[@class="bc p"]/text()', total_page_response)[-1][3:-1]

        # 获取url_list
        self.index_url_list = [self.common_index_url.format(self.tieba_name, str(num * 10)) for num in
                               range(int(self.total_page) // 10)]

        # 遍历发起请求
        content = {}
        for url in self.index_url_list[0:10]:
            response = self.get_requests(url)
            ele_obj_list = self.get_data_use_xpath('//div[@class="i"]/a', response)
            for ele in ele_obj_list:
                content[ele.xpath("./text()")[0]] = "https://tieba.baidu.com" + ele.xpath("./@href")[0]
        self.save_data(content)

        # 处理请求
        for name, url in content.items():
            profile_response = self.get_requests(url)
            ele_list = self.get_data_use_xpath("//div[@class='i']", profile_response)
            if ele_list:
                for ele in ele_list:
                    name = ele.xpath(".//a[text()='图']/@href")
                    if len(name) is 1:
                        with open("./image/"+name[0].split("src=")[-1], 'wb') as file:
                            file.write(self.get_requests(requests.utils.unquote(name[0])).content)


def main():
    # baidu = BaiDu(input("请输入贴吧名称："))
    baidu = BaiDu("李毅")

    baidu.run()


if __name__ == '__main__':
    main()
