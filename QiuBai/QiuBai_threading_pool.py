import time
from queue import Queue
from multiprocessing.dummy import Pool
import requests
from lxml import etree


class QiuBai(object):

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
        }
        self.temp_url = "https://www.qiushibaike.com/8hr/page/{}/"
        self.queue = Queue()
        self.pool = Pool(5)
        self.is_running = True
        self.total_request_num = 0
        self.total_response_num = 0

        self.content = []

    def get_url_list(self):
        for i in range(1, 14):
            self.queue.put(self.temp_url.format(i))
            self.total_request_num += 1

    def get_requests(self, url):
        response = requests.get(url=url, headers=self.headers)
        if response.status_code is 200:
            return response.content.decode()

    def get_xpath_content(self, ele_obj, xpath):
        div_ele_obj_list = ele_obj.xpath(xpath)
        return div_ele_obj_list

    def get_content(self, div):
        item = dict()
        item["gender"] = None
        item["name"] = (div.xpath("./div[@class = 'author clearfix']/a[2]/h2/text()"))[0].strip() if len(
            div.xpath("./div[@class = 'author clearfix']/a[2]/h2/text()")) > 0 else None

        item["avater_url"] = "https:" + (div.xpath("./div[@class = 'author clearfix']/a[1]/img/@src"))[0].split("?")[
            0] if len(div.xpath("./div[@class = 'author clearfix']/a[1]/img/@src")) > 0 else None

        if len(div.xpath("./div[@class = 'author clearfix']/div/@class")) is 1:
            item["gender"] = "woman" if "articleGender womenIcon" in div.xpath(
                "./div[@class = 'author clearfix']/div/@class") else "man"

        item["level"] = div.xpath("./div[@class = 'author clearfix']/div/text()")[0] if len(
            div.xpath("./div[@class = 'author clearfix']/div/text()")) is 1 else None

        item["content"] = div.xpath("./a[@class = 'contentHerf']/div[@class = 'content']/span/text()")[0].strip()

        item["picture_url"] = "https:" + div.xpath("./div[@class = 'thumb']/a/img/@src")[0] if len(
            div.xpath("./div[@class = 'thumb']/a/img/@src")) is 1 else None

        item["count_comments"] = div.xpath(
            "./div[@class = 'stats']/span[@class = 'stats-vote']/i[@class='number']/text()")[0]

        item["likes"] = div.xpath(
            "./div[@class = 'stats']/span[@class = 'stats-comments']/a[@class='qiushi_comments']/i/text()")[0]

        item["hot_comment_user"] = div.xpath(
            "./a[@class = 'indexGodCmt']/div[@class = 'cmtMain']/span[@class='cmt-name']/text()")[0][:-2] if len(
            div.xpath(
                "./a[@class = 'indexGodCmt']/div[@class = 'cmtMain']/span[@class='cmt-name']/text()")) is 1 else None

        item["hot_comment_info"] = div.xpath(
            "./a[@class = 'indexGodCmt']/div[@class = 'cmtMain']/div[@class='main-text']/text()")[0].strip() if len(
            div.xpath(
                "./a[@class = 'indexGodCmt']/div[@class = 'cmtMain']/div[@class='main-text']/text()")) is 2 else None

        item["hot_comment_like_num"] = div.xpath(
            "./a[@class = 'indexGodCmt']/div[@class = 'cmtMain']/div[@class='main-text']/div[@class='likenum']/text()")[
            1].strip() if len(div.xpath(
            "./a[@class = 'indexGodCmt']/div[@class = 'cmtMain']/div[@class='main-text']/div[@class='likenum']/text()")) is 2 else None
        return item

    def save_data(self):
        with open("./糗事百科.txt", "a+", encoding="utf-8") as file:
            file.write(str(self.content))

    def _excute_run(self):

        # while True:
        url = self.queue.get()

        html_response = self.get_requests(url)
        self.total_response_num += 1

        ele_obj = etree.HTML(html_response)

        div_list = self.get_xpath_content(ele_obj, "//div[@id='content-left']/div")

        for div in div_list:
            item_dict = self.get_content(div)
            self.content.append(item_dict)

    def _callback(self, temp):
        if self.is_running:
            self.pool.apply_async(self._excute_run, callback=self._callback)

    def run(self):
        # 1. 准备url列表
        self.get_url_list()
        for i in range(3):
            self.pool.apply_async(self._excute_run, callback=self._callback)
        while True:
            time.sleep(0.0001)
            if self.total_response_num >= self.total_request_num:
                self.is_running = False
                break
        self.save_data()


def main():
    qiubai = QiuBai()
    qiubai.run()


if __name__ == '__main__':
    t1 = time.time()
    main()
    print("total_time:{}".format(time.time() - t1))
