import requests


class Tieba_Baidu(object):
    def __init__(self, tieba_name):
        self.tieba_name = tieba_name
        self.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"}
        self.url = "https://tieba.baidu.com/f?ie=utf-8&kw={}&pn={}"

    def generate_url_list(self):
        return [self.url.format(self.tieba_name, i * 50) for i in range(10)]

    def save_html(self, response, page):
        with open("{}吧第{}页".format(self.tieba_name, page), "wb", ) as file:
            file.write(response.content)
            print("保存{}吧第{}页成功".format(self.tieba_name, page))

    def run(self):
        """
        主要业务逻辑
        :return:
        """
        # 1. 构造url_list
        url_list = self.generate_url_list()
        # 2. 发起请求
        for url in url_list:
            response = requests.get(url=url, headers=self.headers)
            if response.status_code != 200:
                print("请确认网络状态或者您输入的贴吧名称")
            # 3. 保存页面
            page = url_list.index(url) + 1
            self.save_html(response, page)


def main():
    tieba = Tieba_Baidu(input("请输入贴吧名称："))
    tieba.run()


if __name__ == '__main__':
    main()
