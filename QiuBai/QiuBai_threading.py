import threading
import time
from queue import Queue
import requests
from lxml import etree
import random


class QiuBai(object):

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
        }
        self.temp_url = "https://www.qiushibaike.com/8hr/page/{}/"

        self.proxies1 = {"http": "http://39.137.69.7:80"}
        self.proxies2 = {"http": "http://111.7.130.101:8080"}
        self.proxies3 = {"http": "http://39.137.69.10:80"}
        self.proxies4 = {"http": "http://111.7.130.101:80"}
        self.proxies5 = {"http": "http://39.137.69.7:8080"}
        self.proxies6 = {"http": "http://39.137.2.194:8080"}
        self.proxies7 = {"http": "http://39.137.2.214:8080"}
        self.proxies8 = {"http": "http://39.137.2.238:8080"}

        self.url_queue = Queue(maxsize=100)
        self.html_response_queue = Queue(maxsize=100)
        self.content_queue = Queue(maxsize=100)
        self.ele_obj_queue = Queue(maxsize=100)

    def get_url_list(self):
        for i in range(1, 14):
            self.url_queue.put(self.temp_url.format(i))

    def get_requests(self):
        while True:
            url = self.url_queue.get()
            print(url)
            proxies = random.choice(
                [self.proxies1, self.proxies2, self.proxies3, self.proxies4, self.proxies5, self.proxies6,
                 self.proxies7, self.proxies8])
            print(proxies)
            response = requests.get(url=url, headers=self.headers, proxies=proxies)
            time.sleep(1)
            print(response)

            if response.status_code != 200:
                self.url_queue.put(url)
                print("失败一次")
            else:
                self.html_response_queue.put(response.content.decode())
            self.url_queue.task_done()

    def get_xpath_content(self):
        while True:
            response = self.html_response_queue.get()
            ele_obj = etree.HTML(response)
            div_ele_obj_list = ele_obj.xpath("//div[@id='content-left']/div")
            self.ele_obj_queue.put(div_ele_obj_list)
            self.html_response_queue.task_done()

    def get_content(self):
        while True:
            divs = self.ele_obj_queue.get()
            for div in divs:
                item = dict()
                item["name"] = (div.xpath("./div[@class = 'author clearfix']/a[2]/h2/text()"))[0].strip() if len(
                    div.xpath("./div[@class = 'author clearfix']/a[2]/h2/text()")) > 0 else None

                item["avater_url"] = "https:" + \
                                     (div.xpath("./div[@class = 'author clearfix']/a[1]/img/@src"))[0].split("?")[
                                         0] if len(
                    div.xpath("./div[@class = 'author clearfix']/a[1]/img/@src")) > 0 else None

                self.content_queue.put(item)
            self.ele_obj_queue.task_done()

    def save_data(self):
        for i in range(0, self.content_queue.qsize()):
            data = self.content_queue.get()
            with open("./QiuBai/糗事百科.txt", "a+", encoding="utf-8") as file:
                file.write(str(data))
                self.content_queue.task_done()

    def run(self):
        thread_list = []

        url_t = threading.Thread(target=self.get_url_list)
        thread_list.append(url_t)
        for i in range(3):
            requests_t = threading.Thread(target=self.get_requests)
            thread_list.append(requests_t)

        xpath_content_t = threading.Thread(target=self.get_xpath_content)
        thread_list.append(xpath_content_t)

        content_t = threading.Thread(target=self.get_content)
        thread_list.append(content_t)

        for t in thread_list:
            t.setDaemon(True)
            t.start()

        for q in [self.ele_obj_queue, self.html_response_queue, self.url_queue, self.content_queue]:
            q.join()

        self.save_data()


def main():
    qiubai = QiuBai()
    qiubai.run()


if __name__ == '__main__':
    t1 = time.time()
    main()
    print("total_time:{}".format(time.time() - t1))
