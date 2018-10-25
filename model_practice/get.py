import requests

class Practice(object):
    def __init__(self,url):
        self.url = "http://www.renren.com/PLogin.do"
        self.http_proxy = {"http":"http://www.baidu.com/"}
        self.https_proxy = {"https":"https://www.baidu.com/"}
        self.data = {
            "email": "972944926@qq.com",
            "password": "kanzi10-4"
        }
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
        }



    def requests_get(self):
        response = requests.get(url=,verify=False)

    def requests_post(self):
        response = requests.post(url=self.url,headers = self.headers,proxies = self.http_proxy,data=self.data,)