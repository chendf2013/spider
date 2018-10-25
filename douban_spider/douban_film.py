import requests
import json
import retrying


class DouBanTv(object):
    def __init__(self):
        self.headers = {
            "Referer": "https://m.douban.com/tv/american",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X)   AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
        }
        self.url = "https://m.douban.com/rexxar/api/v2/subject_collection/filter_tv_american_hot/items?start={}&count={}&loc_id=108288&_=1540377169543"

        self.start = 1
        self.count = 18
        self.total = None

    @retrying.retry(stop_max_attempt_number=3)
    def _get_requests(self, url):
        response = requests.get(url=url, headers=self.headers, timeout=3)
        assert response.status_code is 200
        return response

    def get_requests(self, url):
        try:
            response = self._get_requests(url)
            return response
        except Exception as ret:
            print(ret)

    def generate_url_list(self):
        url_list = [self.url.format(self.start * num * 18, self.count) for num in range(self.total // 18)]
        if self.total % self.count is not 0:
            url_list.append(self.url.format(self.total - self.total % 18, self.count))
        return url_list

    def deal_response(self, response):
        dict = json.loads(response.content.decode())
        str_dict = json.dumps(dict, ensure_ascii=False,indent=2)
        return str_dict

    def save_to_file(self, str_dict, page):
        try:
            with open("american.txt", "a+", encoding="utf-8")as file:
                file.write(str_dict+"/n")
            print("写入第{}页成功".format(page))
        except:
            print("写入错误")

    def run(self):
        # 1. 构造url列表集合
        total_response = self.get_requests(self.url.format(self.start-1, self.count))
        total_response = json.loads(total_response.content.decode("utf-8"))
        self.total = total_response["subject_collection"]["subject_count"]
        url_list = self.generate_url_list()
        # 2.爬取数据
        for url in url_list:
            html_response = self.get_requests(url)

            # 3.数据整理
            dict_str = self.deal_response(html_response)

            # 4.数据保存
            self.save_to_file(dict_str, url_list.index(url) + 1)


def main():
    doubantv = DouBanTv()
    doubantv.run()


if __name__ == '__main__':
    main()
