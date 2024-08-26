import requests
import fake_useragent
import os
import re
from baiduImageDownload import *
from urllib.parse import *
# 百度搜索图片抓取

class Crawler:

    params = {                         
    'tn': 'resultjson_com',
    'logid': '',
    'ipn': 'rj',
    'ct': '201326592',
    'is': '',
    'fp': 'result',
    'fr': '',
    'word': '',
    'queryWord': '',
    'cl': '2',
    'lm': '-1',
    'ie': 'utf-8',
    'oe': 'utf-8',
    'adpicid': '',
    'st': '-1',
    'z': '',
    'ic': '',
    'hd': '',
    'latest': '',
    'copyright': '',
    's': '',
    'se': '',
    'tab': '',
    'width': '',
    'height': '',
    'face': '0',
    'istype': '2',
    'qc': '',
    'nc': '1',
    'expermode': '',
    'nojc': '',
    'isAsync': '',
    'pn': '30',             # 页码
    'rn': '30',
    'gsm': '1e',
    # '1724431605644': '',
    }
    
    default_url = "https://image.baidu.com/search/acjson"

 
########################################################################################################

    # 获取网页的logid
    def get_logid(self, entire_url: str) -> int:  
        header = self.set_ua()

        request_url = requests.get(entire_url, headers=header).url

        pattern = re.compile("(?<=logid=)\\d+")     # 后顾正则表达式
        l: list = pattern.findall(request_url)
        logid = int(l[0])

        return logid


    # 获取网页的word
    def get_word(self, entire_url: str) -> str:
        header = self.set_ua()

        request_url = requests.get(entire_url, headers=header).url
                
        pattern1 = re.compile("(?<=word).+?(?=&\\b)")       # 正则表达式匹配文本
        temp = unquote(pattern1.findall(request_url)[0])    # 解码

        pattern2 = re.compile("(?<==).+")                   # 二次匹配
        word = unquote(pattern2.findall(temp)[0])           # 最终转成中文语句

        return word


    # 设置UA
    def set_ua(self):
        ua = fake_useragent.UserAgent()
        ua_t = ua.random
        header = {"user-agent": ua_t}       # 配置UA并设置为随机
        return header


    def get_url_list(self, URL: str) -> list:
        header = self.set_ua()       # 配置ua

        response = requests.get(URL, headers=header, params=self.params)      # get方法得到response对象
        imgs_data: list = response.json()['data']        

        L_url: list = []
        for data in imgs_data:
            if 'hoverURL' in data:
                img_url = data['hoverURL']          # 每个data元素中拿到hoverURL的值
                if img_url != '' and img_url not in L_url:                   # 过滤空值
                    L_url.append(img_url)
        response.close()
        return L_url
        # 至此 获得L_url列表


    # 该方法给download_images方法使用
    def __get_last_image_name(self, directory_path) -> int:     # 获取文件夹中最后一张图片的名字数字，以便追加写入
        images: list = os.listdir(directory_path)

        pattern = re.compile(".+(?=\\.jpg)")    # 正则表达式前瞻 (?=...)
    
        images_num: list = []
        for elem in images:
            l = pattern.findall(elem)
            images_num.append(int(l[0]))
        
        if not images_num:      # 需要先判断列表是否为空，即判断文件夹是否有内容
            return int(0)
        else:
            return max(images_num)                  # 返回最大的数字


    def download_images(self, url_list: list, directory_path: str) -> None:
        header = self.set_ua()

        max_image_num = self.__get_last_image_name(directory_path)

        judge = input("\033[34m确定下载吗?(y/n)\033[0m")
        if judge == 'y' or "Y":
            for i, url in enumerate(url_list,1):               # 遍历L_url
                img_data = requests.get(url, headers=header).content    # 由url获取图片Bytes数据
                # 此处路径需要存在，否则报错，或者可以改为调用os模块创建一个directory
                img_path = directory_path + str(i+max_image_num) + ".jpg"         # 写入图片的路径
             
                with open(img_path, "ab") as fp:                    # 以字节模式追加写入
                    fp.write(img_data)                                  
                print(f"\033[34m下载图片...{i}\033[0m")
            print("\033[32m下载完毕\033[0m")

        elif judge == 'n' or 'N':
            print("\033[34m已取消下载\033[0m")
        else: 
            print("\033[34m非法输入,已退出\033[0m")


########################################################################################################

    # 单页抓取方法        参数为:   本地文件夹路径       百度图片网页链接    第几页
    def singlePage_download(self, directory_path: str, Entire_url: str, page: int) -> None:
        # 配置参数
        word = self.get_word(Entire_url)
        self.params['word'] = word
        self.params['queryWord'] = word
        self.params['logid'] = self.get_logid(Entire_url)
        self.params['pn'] = 30*page
        # 通过参数以及百度图片网页url获取图片列表
        L_url: list = self.get_url_list(self.default_url)

        print(f"\033[34m本次抓取到{len(L_url)}张图片\033[0m")
        self.download_images(L_url, directory_path)
      

    # 多页抓取方法           参数为:   本地文件夹路径       百度图片网页链接   爬取的总页数
    def multiplePage_download(self, directory_path: str, Entire_url: str, total_page: int) -> None:
        # 配置参数
        word = self.get_word(Entire_url)
        self.params['word'] = word
        self.params['queryWord'] = word
        self.params['logid'] = self.get_logid(Entire_url)

        total_url: list = []
        for page in range(1, total_page+1): # 获取所有页的url    
            self.params['pn'] = 30*page         # 翻页
            L_url: list = self.get_url_list(self.default_url)   # 更新L_url
            total_url += L_url              

        final_url: list = []    
        for url in total_url: # 过滤相同的url并得到最终的列表
            if url not in final_url:
                final_url.append(url)

        print(f"\033[34m本次抓取到{len(final_url)}张图片\033[0m")
        self.download_images(final_url, directory_path)

########################################################################################################

    # 用于打包成exe的方法

    def singlePage_download_p(self) -> None:
        print("\033[35m【请先准备好一个空文件夹】\033[0m")
        # 配置参数
        Entire_url = input("\033[34m请输入百度图片搜索网址:\033[0m")
        directory_path = input("\033[34m请输入本地文件夹路径(注意最后的\\)【如D:\\image\】:\033[0m")
        page = int(input("\033[34m请输入下载的单页:\033[0m"))

        word = self.get_word(Entire_url)
        self.params['word'] = word
        self.params['queryWord'] = word
        self.params['logid'] = self.get_logid(Entire_url)
        self.params['pn'] = 30*page
        # 通过参数以及百度图片网页url获取图片列表
        L_url: list = self.get_url_list(self.default_url)

        print(f"\033[34m本次抓取到{len(L_url)}张图片\033[0m")
        self.download_images(L_url, directory_path)
      

    def multiplePage_download_p(self) -> None:
        print("\033[35m【请先准备好一个空文件夹】\033[0m")
        # 配置参数
        Entire_url = input("\033[34m请输入百度图片搜索网址:\033[0m")
        directory_path = input("\033[34m请输入本地文件夹路径(注意最后的\\)【如D:\\image\】:\033[0m")
        total_page = int(input("\033[34m请输入要下载的总页数:\033[0m"))

        word = self.get_word(Entire_url)
        self.params['word'] = word
        self.params['queryWord'] = word
        self.params['logid'] = self.get_logid(Entire_url)

        total_url: list = []
        for page in range(1, total_page+1): # 获取所有页的url    
            self.params['pn'] = 30*page         # 翻页
            L_url: list = self.get_url_list(self.default_url)   # 更新L_url
            total_url += L_url              

        final_url: list = []    
        for url in total_url: # 过滤相同的url并得到最终的列表
            if url not in final_url:
                final_url.append(url)

        print(f"\033[34m本次抓取到{len(final_url)}张图片\033[0m")
        self.download_images(final_url, directory_path)
 


if __name__ == '__main__':

    # test_url = "https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1724596676270_R&pv=&ic=&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&dyTabStr=MCwzLDEsMiwxMyw3LDYsNSwxMiw5&ie=utf-8&sid=&word=%E7%88%B1%E8%8E%89%E5%B8%8C%E9%9B%85"

    c1 = Crawler()

    c1.multiplePage_download_p()



# for i, url in enumerate(L_url,1):
#     print(i,url)

# print(f"\033[34m有{len(L_url)}个图片\033[0m")
