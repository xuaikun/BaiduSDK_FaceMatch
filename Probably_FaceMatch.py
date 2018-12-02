# encoding:utf-8
import Function as A                            # 调用Function.py里面定义的函数
import os
import Face_Match as B                          # 调用Face_Match.py里面定义的函数
import random
import time
import shutil

# 获取当前路径下所以子文件【可以是文件夹，也可以是文件】
# A.fileInFolder()

TestFileName = "D:\\000000Aikun_Xu\\Aikun_Xu\\0000work\\3_test"
BackupFileName = "D:\\000000Aikun_Xu\\Aikun_Xu\\0000work\\3_test_backup"
PoolFileName = "D:\\000000Aikun_Xu\\Aikun_Xu\\0000work\\3_pool"
def RootFilder():
    # 获取测试目录下文件夹的总和
    SecondPath = A.fileInFolder(TestFileName)       # 获取根目录下的文件夹总和 例如：D:\\3_test\\445
    # 统计测试目录下文件夹的数量
    SecondPathFileNum = SecondPath.__len__()
    # print ('SecondPathFileNum = ', SecondPathFileNum)
    # print ('SecondPath = ', SecondPath)
    for i in range(0, SecondPathFileNum):
        # path 是第二层 文件夹的总和
        # SecondPath[i] 在第二层总和文件夹中表示单个取出来操作
        path = SecondPath[i]                     # 第二层目录单个文件夹路径    例如：path = D:\\3_test\\445
        # print ('SecondPath[ ',i ,'] = ' ,SecondPath[i])
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
    # print (ThreePathFileNum)
    # print (ThreePath)
    for i in range(0, ThreePathFileNum):
        # print ('ThreePathFileNum = ', ThreePathFileNum)
        # 将文件夹一个一个遍历
        path = ThreePath[i]
        # print ('ThreePath[ ', i, '] = ', path)
        # print ('ThreePath = ')                 # 第三层目录下的单个文件夹名称 例如：path = D:\\3_test\\445\\49
        # print (path)
        # 将单个文件夹的所有图片提取出来放到Photo中
        # 现在已经到一个文件最深的地方了，并且把所有图片找出来了
        Photo = A.fileInFolder(path)             # 获取到文件夹下的图片总和 例如：path =  D:\\3_test\\445\\49\\1534601783,1235657667_align.jpg
        # 统计图片数量
        PhotoNum = Photo.__len__()
        # 应该对照片数量进行判断
        # 1张 2张 大于3张
        # Photo[0] 表示第一张图片
        # Photo[1] 表示第二种图片
        # if PhotoNum == 1:
        #   print ("PhotoNum is 1")
        # elif PhotoNum%2 == 0:   # PhotoNum 为偶数
        # 要取10对照片也就是20张，用来做比较
        # Same 表示 比较的图片是同一个人的的对数
        # Different 表示比较的图片 不是通同一个人的对数
        Same = 0
        Different = 0
        for j in range(0,10):
            a = 0
            b = 0
            # 如果就是一张图片就选这张图片来比较
            if PhotoNum == 1:
                break
            else:
                # a 任意从前半部分取照片的位置
                a = random.randint(0, PhotoNum/2 - 1)
                # b 任意从后半部分取照片位置
                b = random.randint(PhotoNum/2, PhotoNum - 1)
            # Photo1 为前半部分的照片
            Photo1 = Photo[a]
            # Photo2 为后半部分的照片
            Photo2 = Photo[b]
            # 当前这对照片进行比较获取得分
            goal = A.Face_To_Match(Photo1,Photo2)
            time.sleep(0.4)                   # 延时0.4s QPS不免费调用接口容易出错
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
                result = {}
                score = 0
            else:
                # 确定基准库的方法以及阈值
                # 没有异常
                # score >= 60 表示图片为同一个人
                if score >= 60:
                    Same = Same + 1
                    # print ('Same = ', Same)
                elif score < 60:
                    Different = Different + 1
        # print ('Same = ', Same)
        # print ('Different = ', Different)
        # 这里相当于阈值控制，看你需要多大
        if Same > Different:
            print ("已经确定，该图片所在文件夹已经可以作为基准图库")
            print ('BaseRute path = ',path)
            # path 基准
            # ThreePath 表示第三层 文件夹的总和
            NewThreePath = A.fileInFolder(FilePath)  # 获取第三层目录下的文件夹总和 例如：D:\\3_test\\445\\49
            # 统计第三层文件夹中有多少个子文件夹
            NewThreePathFileNum = NewThreePath.__len__()
            for i in range(0, NewThreePathFileNum):
                # 重新将文件夹一个一个遍历 但是比较的时候，作为基准库的文件夹不需要再一一比较，忽略它
                Newpath = NewThreePath[i]
                # 如果两次路径不一样，则进行操作
                if path != Newpath:
                    # 从当前两个文件夹里面各任意抽出10张图片，即：10对进行比较
                    # BaseFolder 和 CompFolder包含了所有图片
                    BaseFolder = A.fileInFolder(path)
                    CompFolder = A.fileInFolder(Newpath)
                    # 统计两个文件夹中图片数量
                    BaseFolderNum = BaseFolder.__len__()
                    CompFolderNum = CompFolder.__len__()
                    # 将比较的两个计数值进行初始化
                    BaseComp_Same = 0
                    BaseComp_Different = 0
                    #两个文件夹各取出10张照片进行比较
                    for i in range(0,10):
                        # 随机取位置
                        a = random.randint(0, BaseFolderNum - 1)
                        b = random.randint(0, CompFolderNum - 1)
                        # 取出图片
                        BasePhoto = BaseFolder[a]
                        CompPhoto = CompFolder[b]
                        # 调用接口 获取分数
                        BaseComp_goal = A.Face_To_Match(BasePhoto, CompPhoto)
                        time.sleep(0.4)
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
                        # 说明与基准库一样，暂时不动，到时候和基准库一起剪切到Same
                        print ("######################################")
                        print (Newpath)
                        print ("能和基准库一起放到Same文件夹")
                        print ("######################################")
                    elif BaseComp_Same <= BaseComp_Different:
                         # print ("将NewPath放入Different文件夹")
                         SplitNewpath = os.path.split(Newpath)
                         # SplitNewpath[0] = D:\\000000Aikun_Xu\\Aikun_Xu\\0000work\\3_test\\461
                         # SplitNewpath[1] = 5028927
                         DifferentFolder = os.path.join(TestFileName, 'Different')    # D:\\000000Aikun_Xu\\Aikun_Xu\\0000work\\3_test\\Different

                         DifferentFolder = os.path.join(DifferentFolder,SplitNewpath[1]) # D:\\000000Aikun_Xu\\Aikun_Xu\\0000work\\3_test\\Different\\5028927
                         # Newpath = ', u'D:\\000000Aikun_Xu\\Aikun_Xu\\0000work\\3_test\\461\\502892
                         # print ('#############################来这里删除了~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                         # print ('Newpath = ', Newpath)
                         # print ('DifferentFolder', DifferentFolder)
                         #B.MoveChildFolder(Newpath, DifferentFolder, 'move')
                         shutil.move(Newpath, DifferentFolder)
                         print ("######################################")
                         print ("将")
                         print (Newpath)
                         print ("放入")
                         print (DifferentFolder)
                         print ("######################################")
                         B.DeleteNoneFolder(SplitNewpath[0])                        # 删除空文件夹
                    #如果两次路径一下，则不操作，进入下一次
                # else:
            # end for 到此为止 第一个文件已经处理完 D:\\000000Aikun_Xu\\Aikun_Xu\\0000work\\3_test\\1 第二层文件夹的一个文件
            # 将这个第二层的文件夹 剪切到Same文件夹中
            SplitPath = os.path.split(path)
            # path = D:\\000000Aikun_Xu\\Aikun_Xu\\0000work\\3_test\\445\\14463
            # SplitPath[0] = D:\\000000Aikun_Xu\\Aikun_Xu\\0000work\\3_test\\445
            # SplitPath[1] = 14463
            # print ('SplitPath = ', SplitPath)
            NewSplitPath = os.path.split(SplitPath[0])
            # NewSplitPath[0] = D:\\000000Aikun_Xu\\Aikun_Xu\\0000work\\3_test
            # NewSplitPath[1] = 445
            # print ('NewSplitPath = ', NewSplitPath)
            SameFolder = os.path.join(TestFileName, 'Same')
            SameFolder = os.path.join(SameFolder, NewSplitPath[1])
            # TestFileName = "D:\\000000Aikun_Xu\\Aikun_Xu\\0000work\\3_test"
            # SameFolder = "D:\\000000Aikun_Xu\\Aikun_Xu\\0000work\\3_test\\Same
            # print ('SplitPath[0] = ', SplitPath[0])
            # print ('SameFolder = ', SameFolder)
            shutil.move(SplitPath[0], SameFolder)
            print ("######################################")
            print ("将")
            print (SplitPath[0])
            print ("放入")
            print (SameFolder)
            print ("######################################")
            # B.DeleteNoneFolder(TestFileName)
            # 因为没有goto之类的跳转语句，只能跳出了
            break
        elif Same <= Different:
            # 还得考虑这种情况？ 如果直到结束都找不到 基准图库，则这个文件夹得移除到Different文件夹
            print ("######################################")
            print ("路径：")
            print ('i = ',i)
            print ('path = ', path)
            print ("非常不确定，该图片所在文件夹不能作为基准图库")
            print ("######################################")
            # 直到最后一个文件夹都是不确定的文件，直接将这个文件夹中的文件剪切到Different文件夹
            if i == (ThreePathFileNum - 1):
                # print ("此文件夹太糟糕了！！！都没有相似的")
                Not_Sure_SplitPath = os.path.split(path)
                # Not_Sure_SplitPath [0] = D:\\000000Aikun_Xu\\Aikun_Xu\\0000work\\3_test\\461
                # Not_Sure_SplitPath [1] = 57396
                Not_SureFolder = A.fileInFolder(Not_Sure_SplitPath[0])
                for Not_SurePath in Not_SureFolder:
                    # Not_SurePath = D:\\000000Aikun_Xu\\Aikun_Xu\\0000work\\3_test\\461\\111
                    Delete_Not_SureFlie = os.path.split(Not_SurePath)
                    # Delete_Not_SureFlie[0] = D:\\000000Aikun_Xu\\Aikun_Xu\\0000work\\3_test\\461
                    # Delete_Not_SureFlie[1] = 1111
                    goalFolder = os.path.join(TestFileName, 'Different')
                    goalFolder = os.path.join(goalFolder, Delete_Not_SureFlie[1])
                    shutil.move(Not_SurePath, goalFolder)   # 将不确定的文件夹里的文件一个个剪切到Different文件夹
                    print ("######################################")
                    print ("将")
                    print (Not_SurePath)
                    print ("放入")
                    print (goalFolder)
                    print ("######################################")
                B.DeleteNoneFolder(TestFileName)    # 在第二层目录下检查是否存在空文件夹
        # print (path)
            # 继续在本次循环里面在可以充当基准库的文件夹
            # Base_Flag = True
        #print ("PhotoNum is 偶数")
        # elif PhotoNum%2 == 1 and PhotoNum != 1:   # PhotoNum 为奇数
        #   print ("PhotoNum is 奇数")
    return

# 程序从这里开始执行
if __name__ == "__main__":
    # 程序开始
    print ('programming is begining……')
    # B.MoveChildFolder(BackupFileName ,TestFileName ,'copytree')  # 将备份的文件copy到测试文件夹
    B.DeleteNoneFolder(TestFileName )                              #  剔除空当前文件夹中空的文件夹
    RootFilder()                                                   # 对测试文件夹进行操作
    print ('programming is ending……')
