# encoding:utf-8
import Function as A   #将相关不变的函数进行打包引用
import os
import shutil
import time
TestFileName = "D:\\000000Aikun_Xu\\Aikun_Xu\\0000work\\3_test"
BackupFileName = "D:\\000000Aikun_Xu\\Aikun_Xu\\0000work\\3_test_backup"
PoolFileName = "D:\\000000Aikun_Xu\\Aikun_Xu\\0000work\\3_pool"
# 删除子文件夹
def DeleteChildFolder(folderName):
    PoolFile = A.fileInFolder(folderName)  # 查看备份Pool文件夹文件
    # print(BackupFile)
    for path in PoolFile:
        # print (path)
        shutil.rmtree(path)  # 将Pool文件夹的文件移除
    return
# 删除操作文件夹中的空文件夹
def DeleteNoneFolder(fileName):
    DeleteFile = A.fileInFolder(fileName)

    # 删除空的文件夹
    for path in DeleteFile:
        Test_File = A.fileInFolder(path)
        lenght = Test_File.__len__()  # 检测文件夹中文件的数量
        # print (lenght)
        if lenght == 0:
            os.rmdir(path)
    return
# 移动子文件夹(有copy和剪切两种方式)
def MoveChildFolder(srefileName,disfileName,op):
    BackupFile = A.fileInFolder(srefileName)  # 查看备份文件夹文件
    # print(BackupFile)
    for path in BackupFile:
        # print (path)
        SplitPath = os.path.split(path)  # 将需要处理的文件夹的名字提取出来
        # SplitPath[0] 前半部分目录
        # SplutPath[1] 最后一级目录
        # print (SplitPath[1])
        NewPath = os.path.join(disfileName, SplitPath[1])  # 新拼接的文件夹路径 只要最后一级名称
        # print (NewPath)
        # 返回新的路径
        if 'copytree' == op:
            shutil.copytree(path, NewPath)  # copy文件到新的路径下
        elif 'move' == op:
            shutil.move(path, NewPath)       # 剪切文件到新的路径下
    return
if __name__ == "__main__":

    # 程序运行前 先将D:\\000000Aikun_Xu\\Aikun_Xu\\0000work\\3_test_backup 备份文件夹
    # 的文件夹copy到 D:\\000000Aikun_Xu\\Aikun_Xu\\0000work\\3_test中 程序处理文件夹
    DeleteChildFolder(TestFileName)         # 先将TestFile 的子文件夹进行删除
    MoveChildFolder(BackupFileName,TestFileName, 'copytree')
    # 将D:\\000000Aikun_Xu\\Aikun_Xu\\0000work\\3_pool中的文件进行删除  存放供查看的文件
    DeleteChildFolder(PoolFileName)

    time_start=time.time()                  # 程序运行开始计时
    A.Root_Choose(TestFileName)
    ProcessFile = os.path.join(TestFileName,'Two')
    A.PreocessTwoFloder(ProcessFile)        # 输入你要操作的文件夹 （相当于第一层文件夹）
                                            # Two文件夹下面有n个需要判断的文件夹，n个文件夹下面有两个文件夹需要处理
    DeleteNoneFolder(TestFileName)          # 删除操作文件夹中的空文件夹
    time_end=time.time()  # 程序结束
    print('time cost = ',time_end-time_start,'s')

    # 程序结束后，将D:\\000000Aikun_Xu\\Aikun_Xu\\0000work\\3_test中的文件夹
    # 剪切到 D:\\000000Aikun_Xu\\Aikun_Xu\\0000work\\3_pool中 供查看
    MoveChildFolder(TestFileName, PoolFileName, 'move')





