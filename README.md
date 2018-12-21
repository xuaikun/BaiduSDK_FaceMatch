# BaiduSDK_FaceMatch
利用百度人脸识别SDK，进行筛图
# 环境：win10 pychram 百度人脸识别sdk
### 记得把公司的程序copy回来，不让后面根本无法进行工作
主要用于人脸对比（识别）：
API接口包含我的AppID、API Key、Secret Key： https://console.bce.baidu.com/ai/?_=1542208053975&fromai=1#/ai/face/overview/index

Python SDK解释文档（总的）：
http://ai.baidu.com/docs#/Face-Python-SDK/top

python SDK解释文档（部分）：
https://cloud.baidu.com/doc/FACE/Face-Python-SDK.html#.E9.85.8D.E7.BD.AEAipFace

python sdk 安装包下载：
aip-python-sdk-2.2.4 下载  https://ai.baidu.com/sdk#bfr

安装python SDK的方法有两种：
第一种：
安装python-sdk时
aip-python-sdk-2.2.4  需要放到python环境安装的的磁盘底下（或者若python环境默认安装，则放在用户文件夹），进入添加环境变量，Path里面添加
c:\user\aip-python-sdk-2.2.4\bin(安装路径为你python环境的安装路径)
如文档所示：https://www.cnblogs.com/szy123618/p/4264451.html

设置好环境变量后：通过cmd命令行模式，进入c:\user\aip-python-sdk-2.2.4  通过命令python setup.py install  编译安装python SDK

完成后可以在命令行里面输入：
from aip import AipFace
进行测试
对于在pychram里面运行程序，可能需要修改python运行的环境（anconada 好像包含了python2，python3 百度的python环境常用python2）
https://jingyan.baidu.com/article/a3a3f81126031e8da3eb8a63.html
切换环境就是等待~

实测已经成功

第二种:（这是百度SDK操作文档给的，好像对环境要求，第一种方法基本OK）
在执行安装python-sdk过程中执行：pip baidu-aip 出现以下问题：
twisted 18.7.0 requires PyHamcrest>=1.9.0, which is not installed.
grin 1.2.1 requires argparse>=1.1, which is not installed.
可以参考下文：
http://www.cnblogs.com/xiaoxuebiye/p/9890205.html


由于百度提供的SDK接口的QPS不能超过一定值，所以使用人脸比对API时需要稍微延时一下（因为我们使用的是免费的）

python文件以及目录操作可以参考：https://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/0013868321590543ff305fb9f9949f08d760883cc243812000

在程序运行过程中出现以下异常：
goal = 
{u'log_id': 1345050723414412131L, u'timestamp': 1542341441, u'cached': 0, u'result': None, u'error_code': 222202, u'error_msg': u'pic not has face'}
result = 
None
没有找到图片，尴尬啦
不过没事，写个异常处理应该就可以了~
try:
   异常测试
except AttributeError:
   异常处理
else:
   没有异常
  
对于多台电脑在调用百度SDK时，应该考虑多创建几个应用，不然两个程序运行时可能会冲突
尽量不让电脑休眠，不然会断网，导致不能访问网络也会导致程序崩溃
解决电脑崩溃的原因，直接把程序进行死循环，并做异常处理

## 人脸检测（Face_Detection.py）:
其中获取options["face_field"] = "age,gender,landmark"; 注意：age和gender之间只能有逗号，不能存在空格
目前实现了比较准确的抠图
python环境中添加opecv环境：
1、首先下载安装opencv
2、按照这个链接设置调用opencv： https://blog.csdn.net/cumtml/article/details/50575408