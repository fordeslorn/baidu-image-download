# *百度图片下载脚本，python小白也能使用的爬虫*

# 注意：该脚本依赖第三方库，可通过在命令行中分别输入以下命令并回车后下载
pip install fake_useragent 

pip install requests
 
# 使用方法(先确保安装好第三方库)：

1.在一个文件夹中创建一个py文件，如：test.py

2.将下载好的baiduImageDownload.py文件也放在该文件夹中

3.在test.py中输入以下几行代码并运行，运行后根据提示操作即可

from baiduImageDownload import *

crl1 = Crawler()

crl1.multiplePage_download_p()
