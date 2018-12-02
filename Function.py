# encoding:utf-8
import os
from aip import AipFace
import base64
import random
import time
import shutil

# 调试标志 Flag = True为调试状态  Flag = False 为不调试状态
Flag = True

""" 你的 APPID AK SK """
APP_ID = '14803185'
API_KEY = '4FmR91rWRKiyxtkvrSNrsDro'
SECRET_KEY = 'Ed4spz5GdjbxfQCfAGfiko8KXd9q0fC4'

client = AipFace(APP_ID, API_KEY, SECRET_KEY)
print(client)


def Face_To_Match(Figure1, Figure2):
    result = client.match(
        [
            {
                'image': base64.b64encode(open(Figure1, 'rb').read()),
                'image_type': 'BASE64',
            },
            {
                'image': base64.b64encode(open(Figure2, 'rb').read()),
                'image_type': 'BASE64',
            }
        ]
    )
    return result

# 这是第一层文件夹
# 读出D:\\test的孩子（低一层文件夹）
def fileInFolder(filepath):
    pathDir = os.listdir(filepath)  # 获取filepath文件夹下的所有的文件
    files = []
    for allDir in pathDir:
        child = os.path.join('%s\\%s' % (filepath, allDir))
        files.append(child.decode('gbk'))  # .decode('gbk')是解决中文显示乱码问题
        # print child
        # if os.path.isdir(child):
        #     print child
        #     simplepath = os.path.split(child)
        #     print simplepath
    return files

#这是第三层文件夹
# 判断同一个文件夹中是否只有一个人的图片
def JudgeSame(Filepath):
    # 返回判断的标志
    Judge_Flag = True
    # 将当前文件夹中所有图片的名字提取出来，放在列表FileName_List中
    FileName_List = fileInFolder(Filepath)
    # 获取列表的长度
    length = FileName_List.__len__()
    # 在当前文件夹中选取两张图片的位置
    a = random.randint(0, length - 1)
    b = random.randint(0, length - 1)
    c = random.randint(0, length - 1)
    d = random.randint(0, length - 1)
    # 随机挑选出4张图片，两两作比较
    Figure1 = FileName_List[a]
    Figure2 = FileName_List[b]
    Figure3 = FileName_List[c]
    Figure4 = FileName_List[d]
    # 获取goal字典，其中保护 id以及评分等
    goal1 = Face_To_Match(Figure1, Figure2)
    time.sleep(0.4)         #延时的目的 防止每秒向服务器发送的请求数qps异常
    goal2 = Face_To_Match(Figure3, Figure4)
    time.sleep(0.4)         #延时的目的 防止每秒向服务器发送的请求数qps异常
    # 获得两个评分Score1 和 Score2
    # print ('goal1 =')
    # print (goal1)
    # print ('goal2 =')
    #print (goal2)
    result1 = dict()
    result2 = dict()
    score1 = 0
    score2 = 0
    try:
        # 测试异常
        result1 = goal1.get('result')  # 得到result这个字典包含的元素
        result2 = goal2.get('result')  # 得到result这个字典包含的元素
        score1  = float(result1.get('score'))  # 从字典result中获得比较分值
        score2  = float(result2.get('score'))  # 从字典result中获得比较分值
    except AttributeError:
        # 异常处理
        print ('路径：')
        print (Filepath)
        print('Not_Sure时出现异常~~~~~~~~~~~~~~~~~~~~~~~~~##################################')
        result1 = {}
        result2 = {}
        score1 = 0
        score2 = 0
    else:
        # 没有异常
        #print ('result1 =')
        #print (result1)
        #print ('reuslt2 =')
        #print (result2)
        # print('score1 = ')
        # print (score1)
        # print('score2 = ')
        # print (score2)
        # 随机选取的4张图片中，两两之间相似度既有超过60%的，又有小于60%的 故将此文件夹的上一层文件夹存入Not_Sure文件夹中
        if((score1 >= 60 and score2 <= 60) or (score1 <= 60 and score2 >= 60)):
            Judge_Flag = True
        else:# 这个里比较明确，只有一种情况
            Judge_Flag = False
        # 判断值
    return Judge_Flag

# 这是第二层文件夹
def Second_Folder(filepath):
    Second_Folder_Flag = True
    # FileName_List 有两个文件名集为列表
    FileName_List = fileInFolder(filepath)

    # 对其中的两个子文件夹进行判断
    if(JudgeSame(FileName_List[0]) == True or JudgeSame(FileName_List[1]) == True):
        Second_Folder_Flag = True
    else:
        Second_Folder_Flag = False

    return Second_Folder_Flag

def Same_Different(filepath):       #这里还是输入 第二层文件夹也就是包含两个文件夹的子文件夹
    # 返回文件操作标志
    SD_Flag = True
    # FileName_List 有n个文件名集为列表
    FileName_List = fileInFolder(filepath)  #  例如：重新读取 D:\\test\\Two\\1911其中的1911已经明确不是Not_Sure
    # 每个FileName_List中有两个子文件夹
    # 例如：FileName_List[0] D:\\test\\Two\\1911\\1
    # 例如：FileName_List[1] D:\\test\\Two\\1911\\2
    # print (FileName_List[0])
    # print (FileName_List[1])

    pathA = fileInFolder(FileName_List[0])  # pathA 中包含n张图片
    # print (path)
    pathB = fileInFolder(FileName_List[1])  # pathB 中包含n张图片
    # print (path)
    # 将两个文件夹中文件数量读取出来
    lengthA = pathA.__len__()
    lengthB = pathB.__len__()
    # 定义列表用于保存10张随机图片
    pathASum = []
    pathBSum = []
    for i in range(0, 10): # 在当前文件夹的所有图片中随机抽取10张图片
        # 随机选取筛选的图片位置
        a = random.randint(0, lengthA - 1)
        b = random.randint(0, lengthB - 1)
        pathASum.append(pathA[a])  # 成功将第一个文件夹中10张图片保存起来了
        pathBSum.append(pathB[b])  # 有些文件夹中图片未达到10张也不要紧
    # print (pathASum)
    # print (pathBSum)
    # 每次初始化 这两个数 它们比较谁先超过5 先超过5者 分到对应的 文件夹中
    Same_Num = 0
    Different_Num = 0
    for i in range(0, 10):  # 10张图片一一比较
        # time.sleep(0.4)
        goal = Face_To_Match(pathASum[i], pathBSum[i])      # 这里的操作很容易出现异常
        # try:
        #     # 运行代码——测试异常
        # except AttributeError:
        #     # 异常处理
        # else:
        #     # 如果没有发生异常
        time.sleep(0.4)             # 一定要延时， 不然qps异常（主要是百度的一些API不免费，理解就好）
        result = dict()
        score = 0
        try:
            # 测试异常
            result = goal.get('result')
            score = result.get('score')
        except AttributeError:
            print ('路径：')
            print (filepath)
            print ('出现异常~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~############################')

            result = {}
            score = 0
        else:
            # print ('score = ')
            # print (score)
            if (score >= 60):
                Same_Num = Same_Num + 1
            elif(score < 60):
                Different_Num = Different_Num + 1
            # 看谁先到5 谁先到 放谁的文件夹里面
            if (Same_Num > 5):  # 把文件放到Same文件夹
                SD_Flag = True
                # print ('放到Same 文件夹')
                break
            elif(Different_Num > 5):   # 把文件放大 Different文件夹
                # print ('放到Different 文件夹')
                SD_Flag = False
                break
    # print ('SD_Flag = ')
    # print (SD_Flag)
    return SD_Flag


# 对Two文件夹进行操作里面存在Not_Sure的文件
def PreocessTwoFloder(filepath):
    # FileName_List 有n个文件名集为列表
    FileName_List = fileInFolder(filepath)
    # 获取此文件夹下有多少文件
    lenght = FileName_List.__len__()
    # print('lenght is ')
    # print(lenght)
    for path in FileName_List:
        # print (path)   # 获得要操作的第三层文件夹名称
        SplitPath = os.path.split(path)   # 将文件路径的前半部分与最后一级分割开
        # SplitPath[0]  为前半部分路径
        # SplitPath[1]  为最后一级路径名称

        # 将目标目录与操作目录最后一级拼接获得JoinPath
        SplitPath_New = os.path.split(filepath)  # 将文件路径的前半部分与最后一级分割开
        NewPath = os.path.join(SplitPath_New[0], 'Not_sure')
        JoinPath = os.path.join(NewPath ,SplitPath[1])  # 修改成为你自己 Not_Sure文件夹路径
        #print(JoinPath)

        result = Second_Folder(path)
        # print ('Judge result = ' )
        # print (result)
        #  result = True  --> Not_Sure
        #  result = False --> Same or Different

        if(result == True): #说明此文件夹中的图片不明确，将其上一层文件夹剪切入Not_Sure中
            # print("放到Not_Sure文件夹")
            # 将含有不明确的图片的文件夹的第二层文件夹剪切到Not_Sure中
            shutil.move(path, JoinPath)  # 回去好好想想 新的路径该怎么修改  已经关闭自动筛选 Not_Sure
            # print ('已经放到Not_Sure文件夹中了')
        elif(result == False): # 说明此文件夹相对明确~，继续判断
            # 当前已经在第二层文件夹中 此文件夹的路径为path此文件夹中有两个文件夹即第三层文件夹
            # 现在要对该文件夹的 两个子文件夹进行操作
            # print("Same or Different")
            SD_Flag = Same_Different(path)
            # print ('path = ')
            # print (path)
            # path 为第二层文件夹  D:\test\Two\1208  将1208文件夹 移动到D:\test\Same  Same文件夹中
            # SD_Flag = True       将此 当前的文件夹path的最后一级目录文件夹，剪切到D:\test\Same\最后一级 中
            # SD_Flag = False      将此 当前的文件夹path的两个子文件夹，剪切到D:\test\Different\最后一级 中并且删除path文件夹
            if(SD_Flag == True):  # 移动到Same文件夹
                SplitPath = os.path.split(path)  # 将文件路径的前半部分与最后一级分割开
                # SplitPath[0]  为前半部分路径
                # SplitPath[1]  为最后一级路径名称
                # print ('SplitPath[1] = ')
                # print (SplitPath[1])

                # 将目标目录与操作目录最后一级拼接获得JoinPath
                SplitPath_New = os.path.split(filepath)  # 将文件路径的前半部分与最后一级分割开
                NewPath = os.path.join(SplitPath_New[0], 'Same')
                JoinPath = os.path.join(NewPath, SplitPath[1])  # 修改成为你自己 Not_Sure文件夹路径
                # print(JoinPath)
                shutil.move(path, JoinPath)      # 将图片相似度大的文件夹剪切到 D:\test\Same\本身文件夹名字
                # print ('已经放到Same文件夹中了')

            elif(SD_Flag == False):
                # print ('path = ')
                # print (path)                       # D:\test\Two\1193
                # FileName_List 有n个文件名集为列表
                FileName_List = fileInFolder(path) #这里应该到第三层文件夹了
                # FileName_List = D:\test\Two\1193\15640
                # FileName_List = D:\test\Two\1193\67017
                for i in range(0,2):
                    SplitPath = os.path.split(FileName_List[i])  # 将文件路径的前半部分与最后一级分割开
                    # SplitPath[0]  为前半部分路径
                    # SplitPath[1]  为最后一级路径名称
                    # print ('SplitPath[1] = ')
                    # print (SplitPath[1])
                    # 将目标目录与操作目录最后一级拼接获得JoinPath
                    SplitPath_New = os.path.split(filepath)  # 将文件路径的前半部分与最后一级分割开
                    NewPath = os.path.join(SplitPath_New[0], 'Different')
                    JoinPath = os.path.join(NewPath, SplitPath[1])  # 修改成为你自己 Not_Sure文件夹路径
                    # print(JoinPath)
                    shutil.move(FileName_List[i], JoinPath)  # 将图片相似度大的文件夹剪切到 D:\test\Different\本身文件夹名字
                os.rmdir(path)       # 删除 当前目录  D:\test\Two\1193
                # print ('已经放到Different文件夹中了')
    return
def Root_Choose(FilePath): # 要处理的文件的路径  D:\1_test
    # FileName_List 有n个文件名集为列表
    FileName_List = fileInFolder(FilePath)   # path = D:\1_test\ 1184
    for path in FileName_List:
        Second_List = fileInFolder(path)     # Second_List = D:\1_test\ 1184 \21465
        # 统计第二层文件夹中子文件夹数量
        lenght = Second_List.__len__()
        # print (Second_List)
        # print (lenght)
        if lenght == 0: # 如果文件数量为 0 把文件夹删除
            os.rmdir(path)
            #print ('文件夹为空，删除')
        elif lenght == 1: # 如果文件数量为1 则保存入Same文件夹
            # D:\1_test  和 1184 分开
            SplitPath = os.path.split(path)  # 将文件路径的前半部分与最后一级分割开
            # SplitPath[0] = D:\1_test 为前半部分路径
            # SplitPath[1] = 1184 为最后一级路径名称
            # print ('SplitPath[1] = ')
            # print (SplitPath[1])
            # 将目标目录与操作目录最后一级拼接获得JoinPath
            NewPath = os.path.join(FilePath,'Same')
            JoinPath = os.path.join(NewPath, SplitPath[1])  # 修改成为你自己 Same文件夹路径
            # print(JoinPath)
            shutil.move(path, JoinPath)  # 将图片相似度大的文件夹剪切到 D:\test\Same\本身文件夹名字
            # print ('已经放到Same文件夹中了')
        elif lenght > 2: # 如果文件数量大于2，则保存入Wait文件夹
            # D:\1_test  和 1184 分开
            SplitPath = os.path.split(path)  # 将文件路径的前半部分与最后一级分割开
            # SplitPath[0] = D:\1_test 为前半部分路径
            # SplitPath[1] = 1184 为最后一级路径名称
            # print ('SplitPath[1] = ')
            # print (SplitPath[1])
            # 将目标目录与操作目录最后一级拼接获得JoinPath
            NewPath = os.path.join(FilePath, 'Wait')
            JoinPath = os.path.join(NewPath, SplitPath[1])  # 修改成为你自己 Wait文件夹路径
            # print(JoinPath)
            shutil.move(path, JoinPath)  # 将图片相似度大的文件夹剪切到 D:\1_test\Wait\本身文件夹名字
            #print ('放入Wait文件夹')
        else: # 如果文件数量等于2，则保存入Two文件夹
            # D:\1_test  和 1184 分开
            SplitPath = os.path.split(path)  # 将文件路径的前半部分与最后一级分割开
            # SplitPath[0] = D:\1_test 为前半部分路径
            # SplitPath[1] = 1184 为最后一级路径名称
            # print ('SplitPath[1] = ')
            # print (SplitPath[1])
            # 将目标目录与操作目录最后一级拼接获得JoinPath
            NewPath = os.path.join(FilePath, 'Two')
            JoinPath = os.path.join(NewPath, SplitPath[1])  # 修改成为你自己 Two文件夹路径
            # print(JoinPath)
            shutil.move(path, JoinPath)  # 将图片相似度大的文件夹剪切到 D:\1_test\Two\本身文件夹名字
            # print ('放入Two文件夹')
    return


