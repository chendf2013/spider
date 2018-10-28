# 网易云音乐使用的是包含了js的elements,因此使用selenium
# 注意 这里面使用的是iframe
import requests
from selenium import webdriver
import time

class Music(object):
    def __init__(self,singer=None,music_name=None):
        self.singer = singer
        self.music_name = music_name
        self.search_url = "https://music.163.com/#/discover/playlist"
        self.style_list = []

    def run(self):

        # 1.获取歌单类型对应的链接
        # 进入歌单页面,进入iframe
        driver = webdriver.Chrome()
        driver.get(self.search_url)
        driver.switch_to.frame("g_iframe")

        # 获取所有的风格
        style_dd_ele_list = driver.find_elements_by_xpath("//div[@id='cateListBox']//dd//a")

        for style_ele in style_dd_ele_list[1:2]:
            item = {}
            item["name"]=style_ele.get_attribute("data-cat")
            item["url"]=style_ele.get_attribute("href")
            item["list"]=[]
            self.style_list.append(item)
        driver.quit()

        # 2.进入歌单类型页面，获取歌曲分类以及对应的链接
        for style in self.style_list[:5]:

            driver = webdriver.Chrome()
            driver.get(style["url"])
            driver.switch_to.frame("contentFrame")
            songs_list = driver.find_elements_by_xpath("//div[@id='m-disc-pl-c']//li")
            for songs in songs_list:
                item = {}
                item["name"]=(songs.find_element_by_xpath("./p[1]/a")).text
                item["url"] = (songs.find_element_by_xpath("./p[1]/a")).get_attribute("href")
                item["user"] = (songs.find_element_by_xpath("./p[2]/a")).get_attribute("title")
                item["list"] = []
                style["list"].append(item)

            driver.quit()


        # 3.获取歌曲链接
        for item in self.style_list[:5]:
            for style_menu in item["list"]:
                print(style_menu["url"])
                driver = webdriver.Chrome()
                driver.get(style_menu["url"])
                driver.switch_to.frame("contentFrame")
                tr_list_ele = driver.find_elements_by_xpath("//table[@class='m-table ']/tbody/tr")
                # tr_list_ele = driver.find_elements_by_class_name("even ")
                for tr_ele in tr_list_ele:
                    item={}
                    item["url"]= "http://music.163.com/song/media/outer/url?"+(tr_ele.find_element_by_xpath(".//span[@class='txt']/a").get_attribute("href")).split("?")[-1]+".mp3"
                    item["song_name"] = tr_ele.find_element_by_xpath(".//span[@class='txt']/a/b").get_attribute("title")

                    try:
                        with open(item["song_name"]+".mp3", "wb") as file:
                            file.write(requests.get(url=item["url"]).content)
                        print(item["song_name"]+".MP3下载成功")
                    except:
                        print(item["song_name"] + ".MP3下载失败")

                    style_menu["list"].append(item)
                driver.quit()



        with open("./网易云音乐.txt","a+",encoding="utf-8") as file:
            file.write(str(self.style_list))


def main():
    music = Music()
    music.run()

if __name__ == '__main__':
    main()