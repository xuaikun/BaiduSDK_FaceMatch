# encoding: utf-8
# 2018年12月1日：记完成GitHub的入门学习，这是个很好的开源平台，日后好好利用
import Function as A                            # 调用Function.py里面定义的函数
import os
import Face_Match as B                          # 调用Face_Match.py里面定义的函数
import random
import time
import shutil

# 获取当前路径下所以子文件【可以是文件夹，也可以是文件】
# A.fileInFolder()

TestFileName = "D:\\000000Aikun_Xu\\Aikun_Xu\\0000work\\3_result"
BackupFileName = "E:\\000007work\\testdata_backup"
PoolFileName = "D:\\000000Aikun_Xu\\Aikun_Xu\\0000work\\3_pool"
ResulFiletName = "D:\\000000Aikun_Xu\\Aikun_Xu\\0000work\\result"


def RootFilder():
    # 获取测试目录下文件夹的总和
    SecondPath = A.fileInFolder(TestFileName)       # 获取根目录下的文件夹总和 例如：D:\\3_test\\445
    # 统计测试目录下文件夹的数量
    SecondPathFileNum = SecondPath.__len__()
    print ('SecondPathFileNum = ', SecondPathFileNum)
    print ('SecondPath = ', SecondPath)
    for i in range(0, SecondPathFileNum):
        # path 是第二层 文件夹的总和
        # SecondPath[i] 在第二层总和文件夹中表示单个取出来操作
        path = SecondPath[i]                     # 第二层目录单个文件夹路径    例如：path = D:\\3_test\\445
        print ('SecondPath[ ', i, '] = ', SecondPath[i])
        B.DeleteNoneFolder(path)                 # 没有图片的文件夹都被删除了

        SecondFilder(path)           # 里面的文件夹都有图片
    return


def SecondFilder(FilePath):
    # 设定判断标志
    # Base_Flag = True 表示当前图片所在文件夹可以充当基准库
    # Base_Flag = False 表示当前图片所在文件夹不可以充当基准库
    # Base_Flag = True
    # ThreePath 表示第三层 文件夹的总和
    ThreePath = A.fileInFolder(FilePath)        # 获取第三层目录下的文件夹总和 例如：D:\\3_test\\445\\49
    # 统计第三层文件夹中有多少个子文件夹
    ThreePathFileNum = ThreePath.__len__()
    # print ('ThreePathFileNum = ', ThreePathFileNum)
    # print ('ThreePath = ', ThreePath)
    for i in range(0, ThreePathFileNum):
        # print ('ThreePathFileNum = ', ThreePathFileNum)
        # 将文件夹一个一个遍历
        path = ThreePath[i]
        print ('ThreePath[ ', i, '] = ', path)
        # 第三层目录下的单个文件夹名称 例如：path = D:\\3_test\\445\\49
        # 将单个文件夹的所有图片提取出来放到Photo中
        # 现在已经到一个文件最深的地方了，并且把所有图片找出来了
        Photo = A.fileInFolder(path)
        # 获取到文件夹下的图片总和 例如：path =  D:\\3_test\\445\\49\\1534601783,1235657667_align.jpg
        # 统计图片数量
        PhotoNum = Photo.__len__()
        # print ('Photo = ', Photo)
        # 应该对照片数量进行判断
        # 1张 2张 大于3张
        # Photo[0] 表示第一张图片
        # Photo[1] 表示第二种图片
        # if PhotoNum == 1:
        #   print ("PhotoNum is 1")
        # elif PhotoNum%2 == 0:   # PhotoNum 为偶数
        # 要取10对照片也就是20张，用来做比较

        # 对每张图片进行遍历
        for k in range(0, PhotoNum):
            # 终止条件为 遍历到最后一张图片
            NewPhoto = A.fileInFolder(path)
            # 获取到文件夹下的图片总和 例如：path =  D:\\3_test\\445\\49\\1534601783,1235657667_align.jpg
            # 每次执行完都得 重新统计 该文件夹中文件的数量
            NewPhotoNum = NewPhoto.__len__()
            print 'NewPhotoNum = ', NewPhotoNum
            # Same 表示 比较的图片是同一个人的的对数
            # Different 表示比较的图片 不是通同一个人的对数
            Same = 0
            Different = 0
            # 再次遍历整个文件夹中文件的数量
            for q in range(0, NewPhotoNum):
                print 'q = ', q
                print 'k = ', k
                # 保证两张图片不是同一张
                if Photo[k] != NewPhoto[q]:
                    print 'Photo[k] =', Photo[k]
                    print 'NewPhoto[q]', NewPhoto[q]
                    # 这两张图片进行比较
                    # print 'Photo[k] = ', Photo[k]
                    # print 'NewPhoto[q] = ', NewPhoto[q]
                    time.sleep(0.4)
                    goal = A.Face_To_Match(Photo[k], NewPhoto[q])
                    time.sleep(0.4)  # 延时0.4s QPS不免费调用接口容易出错
                    # 应该做个异常处理 (必须做)
                    # try:
                    # except:
                    # else :
                    result = dict()
                    score = 0
                    try:
                        # 测试异常
                        result = goal.get('result')
                        # score 是比较得分
                        score = result.get('score')
                    except AttributeError:
                        # 异常处理
                        # result = {}
                        # score = 0
                        print "进行异常处理"
                        print 'Same =', Same
                        print 'Different = ', Different
                        NewPhotoNum = NewPhotoNum - 1
                        # Different = Different + 1
                    else:
                        # 确定基准库的方法以及阈值
                        # 没有异常
                        # score >= 60 表示图片为同一个人
                        if score >= 60:
                            Same = Same + 1
                            # print ('Same = ', Same)
                        elif score < 60:
                            Different = Different + 1
                    # 如果一张图片与文件夹中50%以上图片不相同，则可以直接移除
                    print 'Different = ', Different
                    print 'NewPhotoNum = ', NewPhotoNum
                    print 'Same = ', Same
                    print 'Different/NewPhotoNum = ', float(float(Different)/float(NewPhotoNum))
                    print 'Same/NewPhotoNum = ', float(float(Same)/float(NewPhotoNum))
                    if float(float(Different)/float(NewPhotoNum)) >= 0.5:
                        print '&&&&&&&&&&&&&&&&&&&&删除#######################'
                        # 删除Photo[k]
                        # Photo[k] 应该为图片名称
                        PhotoPath = os.path.split(Photo[k])
                        # PhotoPath[0] = D:\testdata\1253\6791
                        # PhotoPath[1] = m.01mbt1x_44-FaceId-0.jpg
                        NewPhotoPath =  os.path.split(PhotoPath[0])
                        # NewPhotoPath [0] = D:\testdata\1253
                        # NewPhotoPath [1] = 6791
                        oldName = NewPhotoPath[1]
                        NewPhotoPath = os.path.join(NewPhotoPath[0], 'Different')
                        # NewPhotoPath = D:\testdata\1253\Different
                        NewPhotoPath = os.path.join(NewPhotoPath, oldName)
                        print ('NewPhotoPath =', NewPhotoPath)
                        # NewPhotoPath = D:\testdata\1253\Different\6791
                        print "Photo[k] = ", Photo[k]
                        print 'NewPhotoPath = ', NewPhotoPath
                        # os.remove('1.jpg') # 这里可以删除文件
                        # 一定要确认查找的路径是否存在
                        isExist = os.path.exists(NewPhotoPath)
                        if not isExist:
                            print "不存在该路径，创建对应路径"
                            os.makedirs(NewPhotoPath)
                        shutil.move(Photo[k], NewPhotoPath)   # 将不同的图片剪切到 新的文件夹底下 路径一定要判断存在
                        break
                    # 一张图片与其中的60%以上的图片相似，则可以认为其属于该文件夹，进入下一次选择
                    if float(float(Same) / float(NewPhotoNum)) >= 0.6:
                        print '&&&&&&&&&&&&&&&&&&&&保留#######################'
                        break
    # 按道理一对第i个文件夹操作完成，将操作完成的文件夹剪切到目标文件夹
    # 原文件夹为:path 目标文件夹为ResulFiletName
    print 'FilePath = ', FilePath
    shutil.move(FilePath, ResulFiletName)
    # 删除空文件夹
    B.DeleteNoneFolder(TestFileName)
    return

# 程序从这里开始执行

def start():
    if __name__ == "__main__":
        # 程序开始
        start = time.time()
        print ('programming is beginning……')

        # B.MoveChildFolder(BackupFileName, TestFileName, 'copytree')  # 将备份的文件copy到测试文件夹
        B.DeleteNoneFolder(TestFileName)                              # 剔除空当前文件夹中空的文件夹
        RootFilder()                                                  # 对测试文件夹进行操作
        B.DeleteNoneFolder(TestFileName)
        print ('programming is ending……')
        end = time.time()
        print ('spend time = ', end - start, 's')


# 怕出现网络异常，而做的处理

exceptFlag = True
while exceptFlag:
    try:
        print "测试异常"
        start()
        RootPath = A.fileInFolder(TestFileName)
        # 如果目标文件夹中没有文件了，直接退出
        RootPathFileNum = RootPath.__len__()
        if RootPathFileNum == 0:
            exceptFlag = False
    except:
        print "处理异常"
        time.sleep(0.1)
        exceptFlag = True
    else:
        print "没有异常"
        # start()
