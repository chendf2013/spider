import random

import requests
import json


class BoXueGu(object):
    def __init__(self, name, password, suggestion):
        self.name = name
        self.password = password
        self.login_data = {
            "loginName": self.name,
            "password": self.password
        }
        self.suggestion = suggestion
        self.feedback_id = None

        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"}

        self.login_url = "http://ntlias-stu.boxuegu.com/user/login"
        self.feedback_id_url = "http://ntlias-stu.boxuegu.com/feedback/queryTodayFeedback"
        self.feedback_info_url = "http://ntlias-stu.boxuegu.com/feedback/getFeedbackInfo"
        self.save_feedback_url = "http://ntlias-stu.boxuegu.com/feedback/save"

        self.session = requests.Session()

    def session_post(self, url, data, headers):
        response = self.session.post(url=url, data=data, headers=headers)
        return response

    def session_get(self, url, params, headers):
        response = self.session.get(url=url, params=params, headers=headers)
        return response

    def parse_feedback_id(self, response):
        response = json.loads(response.content.decode())
        if not response["success"]:
            print("今天没有反馈要做")
        feedback_id = response["resultObject"]["list"][0]["feedbackId"]
        return feedback_id

    def parse_feedback_info(self, response):
        response = json.loads(response.content.decode())
        if not response["success"]:
            print("今天没有反馈要做")
        feedback_info = len(response["resultObject"]["targets"])
        return feedback_info

    def save_feedback_info(self, response):
        response = json.loads(response.content.decode())
        print(response)
        if response["success"]:
            print("提交反馈成功")
        else:
            print("提交反馈失败")

    def run(self):
        # 1. 登录
        login_response = self.session_post(self.login_url, self.login_data, self.headers)
        if login_response:
            print("登录成功")
        else:
            print("登录失败")

        # 2. 获取反馈id
        feedback_id_response = self.session_get(self.feedback_id_url, {}, self.headers)
        if feedback_id_response:
            print("获取id成功")
        else:
            print("获取id失败")
        self.feedback_id = self.parse_feedback_id(feedback_id_response)

        # 2. 获取个人的反馈信息
        feedback_info_response = self.session_post(self.feedback_info_url, {"feedbackId": self.feedback_id},
                                                   self.headers)
        if feedback_id_response:
            print("获取反馈信息成功")
        else:
            print("获取反馈信息失败")

        feedback_info_count = self.parse_feedback_info(feedback_info_response)
        # 3. 提交反馈信息
        feedback_data = {
            "feedbackId": str(self.feedback_id),
            "suggest": self.suggestion,
            "targetArr":
                [
                    {
                        "questionNo": "{}".format(n),
                        "questionVal": "{0}"
                        # "questionVal": "{}".format(random.randint(0,3))
                    } for n in range(1, feedback_info_count + 1)
                ],
            "anonymity": 0
        }

        print(feedback_data)
        # 提交的字典的值是字符串
        feedback_data_str = json.dumps(feedback_data)

        headers = self.headers
        headers["Referer"] = "http://ntlias-stu.boxuegu.com/"

        save_feedback_response = self.session_post(self.save_feedback_url, {"data": feedback_data_str}, headers)
        self.save_feedback_info(save_feedback_response)


def main():
    # my_boxuegu = BoXueGu(input("请输入登录账号"),input("请输入登录密码"),input("请输入建议内容："))
    # my_boxuegu = BoXueGu("A180501084", "kanzi10-4","无")
    my_boxuegu = BoXueGu("A180501084", "kanzi10-4", input("请输入建议内容："))
    my_boxuegu.run()


if __name__ == '__main__':
    main()
