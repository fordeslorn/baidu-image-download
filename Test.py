from baiduImageDownload import *
# # 网页链接
url = "https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1724596676270_R&pv=&ic=&nc=1&z=&hd=&latest=&copyright=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&dyTabStr=MCwzLDEsMiwxMyw3LDYsNSwxMiw5&ie=utf-8&sid=&word=%E7%88%B1%E8%8E%89%E5%B8%8C%E9%9B%85"

# 创建一个百度图片爬虫crl1
crl1 = Crawler()

# 调用多页抓取方法  参数为:   本地文件夹路径       百度图片网页链接   爬取的总页数
crl1.multiplePage_download("E:/album/images/", Entire_url = url, total_page=2)