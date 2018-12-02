# encoding: utf-8
import Function as A                            # 调用Function.py里面定义的函数
import os
import Face_Match as B                          # 调用Face_Match.py里面定义的函数
import random
import time
import shutil
# 2018年12月1日，今天不用上班，在学习里面学习使用GitHub
# 获取当前路径下所以子文件【可以是文件夹，也可以是文件】
# A.fileInFolder()

TestFileName = "D:\\000000Aikun_Xu\Aikun_Xu\\0000work\\3_test"
BackupFileName = "D:\\222222222222222222 - Backup"
PoolFileName = "D:\\000000Aikun_Xu\\Aikun_Xu\\0000work\\3_pool"
ResulFiletName = "D:\\000000Aikun_Xu\\Aikun_Xu\\0000work\\3_result"

def root_folder():
    # 获取测试目录下文件夹的总和
    second_path = A.fileInFolder(TestFileName)       # 获取根目录下的文件夹总和 例如：D:\\3_test\\445
    # 统计测试目录下文件夹的数量
    second_path_file_num = second_path.__len__()
    # print ('SecondPathFileNum = ', second_path_file_num)
    # print ('SecondPath = ', second_path)
    for i in range(0, second_path_file_num):
        B.DeleteNoneFolder(TestFileName)
        # path 是第二层 文件夹的总和
        # SecondPath[i] 在第二层总和文件夹中表示单个取出来操作
        path = second_path[i]                     # 第二层目录单个文件夹路径    例如：path = D:\\3_test\\445
        #  ('second_path[ ', i, '] = ', second_path[i])
        B.DeleteNoneFolder(path)                 # 没有图片的文件夹都被删除了
        second_folder(path)           # 里面的文件夹都有图片
    return


def second_folder(filepath):

    # 设定判断标志
    # Base_Flag = True 表示当前图片所在文件夹可以充当基准库
    # Base_Flag = False 表示当前图片所在文件夹不可以充当基准库
    # Base_Flag = True
    # ThreePath 表示第三层 文件夹的总和
    ThreePath = A.fileInFolder(filepath)        # 获取第三层目录下的文件夹总和 例如：D:\\3_test\\445\\49
    # 统计第三层文件夹中有多少个子文件夹
    ThreePathFileNum = ThreePath.__len__()
    # print ('ThreePathFileNum = ', ThreePathFileNum)
    # print ('ThreePath', ThreePath)
    # 定义StorePath用于保存，被选中的路径
    StorePath = []
    # 当目前文件夹没有文件时 直接退出，遍历另一个文件夹
    while ThreePathFileNum:
    # for i in range(0, ThreePathFileNum):
        # print ('ThreePathFileNum = ', ThreePathFileNum)
        # 将文件夹一个一个遍历
        ThreePath = A.fileInFolder(filepath)  # 获取第三层目录下的文件夹总和 例如：D:\\3_test\\445\\49
        # 统计第三层文件夹中有多少个子文件夹
        ThreePathFileNum = ThreePath.__len__()
        if ThreePathFileNum == 0:
            # 若文件夹里面没有文件了，直接退出
            print ('ThreePathFileNum =', ThreePathFileNum )
            print ('退出while')
            break
        # print ('ThreePathFileNum = ', ThreePathFileNum)
        # print ('ThreePath', ThreePath)
        # 每次都从第一个开始遍历
        i = 0
        print ('i =', i)
        path = ThreePath[i]
        print ('ThreePath[ ', i, '] = ', path)
        # print ('ThreePath = ')                 # 第三层目录下的单个文件夹名称 例如：path = D:\\3_test\\445\\49
        # print (path)
        # Photo = A.fileInFolder(path)
        # 获取到文件夹下的图片总和 例如：path =  D:\\3_test\\445\\49\\1534601783,1235657667_align.jpg
        # 统计图片数量
        # PhotoNum = Photo.__len__()
        # 主要是为了获得它的最后一级目录名称，以充当它新的目录的名称
        StorePath.append(path)
        new_path = os.path.split(path)
        result_path = os.path.join(ResulFiletName, new_path[1])
        print ("选中第一个文件夹作为基准库，检查该文件夹所在文件夹还有其他文件夹与它文件相似")
        # ThreePath 表示第三层 文件夹的总和
        NewThreePath = A.fileInFolder(filepath)  # 获取第三层目录下的文件夹总和 例如：D:\\3_test\\445\\49
        # 统计第三层文件夹中有多少个子文件夹
        NewThreePathFileNum = NewThreePath.__len__()
        for i in range(0, NewThreePathFileNum):
            # 重新将文件夹一个一个遍历 但是比较的时候，作为基准库的文件夹不需要再一一比较，忽略它
            Newpath = NewThreePath[i]
            # 保证选取的文件夹与基准文件夹不相同
            if Newpath != path:
                print ('Newpath = ', Newpath)
                # 如果两次路径不一样，则进行操作
                # 从当前两个文件夹里面各任意抽出10张图片，即：10对进行比较
                # BaseFolder 和 CompFolder包含了所有图片
                # BaseFolder = A.fileInFolder(result_path)
                BaseFolder = A.fileInFolder(path)
                CompFolder = A.fileInFolder(Newpath)
                # 统计两个文件夹中图片数量
                BaseFolderNum = BaseFolder.__len__()
                CompFolderNum = CompFolder.__len__()
                # 将比较的两个计数值进行初始化
                BaseComp_Same = 0
                BaseComp_Different = 0
                #两个文件夹各取出10张照片进行比较
                for i in range(0, 10):
                    # 随机取位置
                    a = random.randint(0, BaseFolderNum - 1)
                    b = random.randint(0, CompFolderNum - 1)
                    # 取出图片
                    BasePhoto = BaseFolder[a]
                    CompPhoto = CompFolder[b]
                    # 调用接口 获取分数
                    time.sleep(1)
                    BaseComp_goal = A.Face_To_Match(BasePhoto, CompPhoto)
                    time.sleep(1)
                    BaseComp_result = {}
                    BaseComp_Score = 0
                    # 要做异常处理，主要防止QPS出现异常
                    try:
                        # 异常测试
                        BaseComp_result = BaseComp_goal.get('result')
                        BaseComp_Score = BaseComp_result.get('score')
                    except AttributeError:
                        # 异常处理
                        BaseComp_result = {}
                        BaseComp_Score = 0
                    else:
                        # BaseComp_Score  程序正常
                        # print ('BaseComp_Score = ',BaseComp_Score)
                        if BaseComp_Score > 60:
                            BaseComp_Same = BaseComp_Same + 1
                        else:
                            BaseComp_Different = BaseComp_Different + 1
                print ('BaseComp_Same = ', BaseComp_Same )
                print ('BaseComp_Different', BaseComp_Different)
                # 这里主要比较两个文件夹中图片的相似度
                if BaseComp_Same > BaseComp_Different:
                    # 两个文件夹及其相似 放到同一个文件夹底下
                    StorePath.append(Newpath)   # 将相似的文件夹保存到一起
                    print 'StorePath = ', StorePath

        # 可以剪切 StorePath 到目标文件夹了
        StorePathLen = StorePath.__len__()
        print 'StorePathLen = ', StorePathLen
        print '以下的文件夹应该剪切到一块去'
        for p in range(0, StorePathLen):
            print 'StorePath[p] = ', StorePath[p]
            # result_path 是目标文件夹的根
            # SplitPathNew 主要为了获得 它的最后一级目录
            SplitPathNew = os.path.split(StorePath[p])
            goal_path = os.path.join(result_path, SplitPathNew[1])
            # 创建目标目录
            shutil.move(StorePath[p], goal_path)   # 将相似的文件夹全部剪切到目标文件夹下

        # 路径数据重新初始化
        StorePath = []
    return

# 程序从这里开始执行

def start():
    if __name__ == "__main__":
        # 程序开始
        start = time.time()
        print ('programming is beginning……')

        # B.MoveChildFolder(BackupFileName, TestFileName, 'copytree')  # 将备份的文件copy到测试文件夹
        B.DeleteNoneFolder(TestFileName)                              # 剔除空当前文件夹中空的文件夹
        root_folder()                                                  # 对测试文件夹进行操作
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
        # 统计目标文件夹的文件数量 作为终止条件
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

