import multiprocessing
from multiprocessing.dummy import JoinableQueue as Queue
import time
import requests
from lxml import etree


class QiuBai(object):

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
        }
        self.temp_url = "https://www.qiushibaike.com/8hr/page/{}/"

        self .content = []
        self.url_queue = Queue(maxsize=100)
        self.html_response_queue = Queue(maxsize=100)
        self.content_queue = Queue(maxsize=100)
        self.ele_obj_queue = Queue(maxsize=100)



    def get_url_list(self):
        for i in range(1, 3):
            self.url_queue.put(self.temp_url.format(i))
            print(self.temp_url.format(i))



    def get_requests(self):
        # for i in range(1,self.url_queue.qsize()+1):
        while True:
            url = self.url_queue.get()
            response = requests.get(url=url, headers=self.headers)
            print(response)
            if response.status_code != 200:
                self.url_queue.put(url)
                print("失败一次")
            else:
                self.html_response_queue.put(response.content.decode())
            self.url_queue.task_done()





    def get_xpath_content(self):
        # for i in range(1,self.html_response_queue.qsize()+1):
        while True:
            ele_obj = etree.HTML(self.html_response_queue.get())
            div_ele_obj_list = ele_obj.xpath("//div[@id='content-left']/div")
            self.ele_obj_queue.put(div_ele_obj_list)
            self.html_response_queue.task_done()




    def get_content(self):
        for i in range(0,self.ele_obj_queue.qsize()):
            divs = self.ele_obj_queue.get()
            for div in divs:
                item = dict()
                item["gender"]=None
                item["name"] = (div.xpath("./div[@class = 'author clearfix']/a[2]/h2/text()"))[0].strip() if len(div.xpath("./div[@class = 'author clearfix']/a[2]/h2/text()")) >0 else None

                item["avater_url"] = "https:"+(div.xpath("./div[@class = 'author clearfix']/a[1]/img/@src"))[0].split("?")[0] if len(div.xpath("./div[@class = 'author clearfix']/a[1]/img/@src")) > 0 else None

                if len(div.xpath("./div[@class = 'author clearfix']/div/@class")) is 1:
                    item["gender"] = "woman" if "articleGender womenIcon" in div.xpath("./div[@class = 'author clearfix']/div/@class") else "man"



                item["level"] = div.xpath("./div[@class = 'author clearfix']/div/text()")[0] if len(div.xpath("./div[@class = 'author clearfix']/div/text()")) is 1 else None

                item["content"] = div.xpath("./a[@class = 'contentHerf']/div[@class = 'content']/span/text()")[0].strip()



                item["picture_url"] = "https:"+div.xpath("./div[@class = 'thumb']/a/img/@src")[0] if len(div.xpath("./div[@class = 'thumb']/a/img/@src")) is 1 else None


                item["count_comments"] = div.xpath(
                    "./div[@class = 'stats']/span[@class = 'stats-vote']/i[@class='number']/text()")[0]


                item["likes"] = div.xpath(
                    "./div[@class = 'stats']/span[@class = 'stats-comments']/a[@class='qiushi_comments']/i/text()")[0]

                item["hot_comment_user"] = div.xpath(
                    "./a[@class = 'indexGodCmt']/div[@class = 'cmtMain']/span[@class='cmt-name']/text()")[0][:-2] if len(div.xpath(
                    "./a[@class = 'indexGodCmt']/div[@class = 'cmtMain']/span[@class='cmt-name']/text()")) is 1 else None


                item["hot_comment_info"] = div.xpath(
                    "./a[@class = 'indexGodCmt']/div[@class = 'cmtMain']/div[@class='main-text']/text()")[0].strip() if len( div.xpath(
                    "./a[@class = 'indexGodCmt']/div[@class = 'cmtMain']/div[@class='main-text']/text()")) is 2 else None


                item["hot_comment_like_num"] = div.xpath(
                    "./a[@class = 'indexGodCmt']/div[@class = 'cmtMain']/div[@class='main-text']/div[@class='likenum']/text()")[1].strip() if len(div.xpath(
                    "./a[@class = 'indexGodCmt']/div[@class = 'cmtMain']/div[@class='main-text']/div[@class='likenum']/text()")) is 2 else None
                self.content.append(item)


    def save_data(self):
        with open("糗事百科.txt", "a+", encoding="utf-8") as file:
            file.write(str(self.content))
            print("写入成功")
        print("长度是：{}".format(len(self.content)))

    def run(self):
        process_list = []

        url_t = multiprocessing.Process(target=self.get_url_list)
        process_list.append(url_t)

        for i in range(3):
            requests_t =multiprocessing.Process(target=self.get_requests)
            process_list.append(requests_t)

        xpath_content_t = multiprocessing.Process(target=self.get_xpath_content)
        process_list.append(xpath_content_t)

        content_t = multiprocessing.Process(target=self.get_content)
        process_list.append(content_t)

        for p in process_list:
            p.setDaemon=True
            p.start()

        time.sleep(10)

        for q in [self.ele_obj_queue, self.html_response_queue, self.url_queue, self.content_queue]:
            q.join()

        self.save_data()
def main():
    qiubai = QiuBai()
    qiubai.run()


if __name__ == '__main__':
    t1 = time.time()
    main()
    print("total_time:{}".format(time.time()-t1))