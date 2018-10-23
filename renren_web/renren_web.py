import requests


class RenRen(object):
    def __init__(self, email, password):
        self.login_url = "http://www.renren.com/PLogin.do"
        self.profile_url = "http://zhibo.renren.com/top"
        self.email = email
        self.password = password


    @staticmethod
    def save_html(html):
        with open("./renren_web/人人网个人主页.html", "w", encoding="utf-8") as  file:
            file.write(html)
            print("保存人人网个人主页成功")

    def run(self):
        """主逻辑函数"""
        # 1.构造session

        session = requests.Session()
        # 2. 获取cookie

        session.post(url=self.login_url, data={"email": self.email, "password": self.password})
        # 3. 获取主页面

        html = session.get(url=self.profile_url).content.decode()

        # 4. 保存主页面
        self.save_html(html)


def main():
    renren = RenRen(input("请输入登录邮箱："), input("请输入登录密码："))
    renren.run()


if __name__ == '__main__':
    main()


# 请输入登录邮箱：972944926@qq.com
# 请输入登录密码：kanzi10-4