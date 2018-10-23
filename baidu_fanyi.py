import json
import sys
import requests


class BaiduTranslation(object):
    def __init__(self, word):
        self.word = word

        self.check_language_url = "https://fanyi.baidu.com/langdetect"
        self.translate_url = "https://fanyi.baidu.com/basetrans"

        self.headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"}

    def params_post(self, url, data, headers):
        """
        发起post请求，获取参数
        :param url:
        :param params:
        :param headers:
        :return:
        """
        response = requests.post(url=url, data=data, headers=headers)
        return response

    def run(self):
        """
        主要业务逻辑
        :return:
        """
        # 1. 发起请求
        json_temp = self.params_post(self.check_language_url, {"query": self.word}, self.headers)

        # 2. 获取要翻译文字语言类型
        dict_temp = json.loads(json_temp.content.decode("utf-8"))
        language_type = dict_temp["lan"]

        # 3. 发起翻译请求
        ret_json_temp = self.params_post(self.translate_url, {"from": language_type, "to": "en", "query": self.word},
                                         self.headers)
        # 4. 获取翻译结果
        ret_dict_temp = json.loads(ret_json_temp.content.decode("utf-8"))
        translate_ret = ret_dict_temp["trans"][0]["dst"]
        print("{}：{}".format(self.word, translate_ret))


def main():
    try:
        word_to_translate = sys.argv[1]
    except:
        print("请输入要翻译的内容")
        return
    word = BaiduTranslation(word_to_translate)
    word.run()


if __name__ == "__main__":
    main()
