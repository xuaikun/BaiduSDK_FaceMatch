# encoding: utf-8
# Face_Detection.py文件主要用于从一张图片中抠出人脸

from aip import AipFace
import base64
import cv2
import os
import shutil
import time

""" 你的 APPID AK SK """

APP_ID = '14803185'
API_KEY = '4FmR91rWRKiyxtkvrSNrsDro'
SECRET_KEY = 'Ed4spz5GdjbxfQCfAGfiko8KXd9q0fC4'

client = AipFace(APP_ID, API_KEY, SECRET_KEY)
print(client)


def face_detection(image_name):
    image = base64.b64encode(open(image_name, 'rb').read())
    image_type = "BASE64"
    """调用人脸检测"""
    options = {}
    options["max_face_num"] = 10
    options["face_field"] = "location"  # age和gender之间只能存在英文逗号不能存在空格

    result = client.detect(image, image_type, options)
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

def cut_photo(photo_name):
    #  将一张图片放进来就能将图片进行处理成单个头像的图片
    #  image1 = "F:\\photo_test\\mul_face\\00000.jpg"
    error_Falg = True
    image1 = photo_name
    result = face_detection(image1)
    try:
        result = result.get("result")
        face_list = result.get("face_list")
    except :
        print "进行任意异常处理"
        error_Falg = False
    else:
        # 没有异常
        count = 0
        SplitPath = os.path.split(image1)   # 将需要处理的文件夹的名字提取出来
        # SplitPath[0]  路径名称的前半部分
        # SplitPath[1]  路径名称的最后一级

        SplitPath_new = os.path.split(SplitPath[0])  # 将需要处理的文件夹的名字提取出来

        img = cv2.imread(image1)    # 读取图片
        # print "img.shape[0] =", img.shape[0]  # 622 y ~ top
        # print "img.shape[1] =", img.shape[1]  # 534 x ~ left

        if img.shape[0] <= 500 or img.shape[1] <= 500:
            # 图片已经在之前被处理过了，不需要再次处理，直接剪切到对应文件夹中
            single_face = os.path.join(SplitPath_new[0], 'single_face')
            isExist = os.path.exists(single_face)
            if not isExist:
                print "不存在该路径，创建对应路径"
                os.makedirs(single_face)
            shutil.move(image1, single_face)
        else:
            # 图片未经过操作，需要进行抠图
            # face_list 保存着几个人脸的位置信息
            for i in range(0, len(face_list)):
                get_list = face_list[i]
                # 获取某个人的人脸位置信息
                location = get_list.get("location")
                # 将人脸位置信息具体化
                width   = location.get("width")     # w
                top     = location.get("top")       # y
                height  = location.get("height")    # h
                left    = location.get("left")      # x

                # 将图像的相关像素整形化
                x = int(left)
                y = int(top)
                w = int(width)
                h = int(height)

                try:
                    # 测试异常
                    # 为了避免操作图片时超过像素
                    Y = y - int(y*0.2)
                    if Y < 0:
                        Y = 0;
                    Y_H = y + h + int(y*0.18)
                    if Y_H > img.shape[0]:
                        Y_H = img.shape[0]

                    X = x - int(x*0.03)
                    if X < 0:
                        X = 0
                    X_W = x + w + int(x*0.03)
                    if X_W > img.shape[1]:
                        X_W = img.shape[1]

                    # 将图片从原图上抠出来，把外部边框扩大一点
                    f = img[Y:Y_H, X:X_W]

                except :
                    print "进行任意异常处理"
                    # 说明这个图像不清晰，先暂时不处理
                    break
                else:
                    # 未发生异常
                    # 重新命名时，可以用时间戳+计数值
                    partPath = [str(int(time.time())), str(count)]
                    NewPath  = os.path.join(SplitPath_new[0], 'single_face')
                    isExist = os.path.exists(NewPath)
                    if not isExist:
                        print "不存在该路径，创建对应路径"
                        os.makedirs(NewPath)
                    # 新的图片命名
                    New_Name = partPath[0] + partPath[1] + SplitPath[1]
                    NewPath = os.path.join(NewPath, New_Name)
                    # 将抠出的图片进行保存
                    cv2.imwrite(NewPath, f)
                    count = count + 1
            operation_ok = os.path.join(SplitPath_new[0], 'operation_ok')
            isExist = os.path.exists(operation_ok)
            if not isExist:
                print "不存在该路径，创建对应路径"
                os.makedirs(operation_ok)
            shutil.move(image1, operation_ok)
    return error_Falg


if __name__ == "__main__":
    # path 表示要操作的文件夹
    path = "E:\\000007work\\photo_test\\1"
    error_Flag = True
    print "program begin……"
    start = time.time()
    end_Flag = True
    fore_fileInfolderNum = 0
    while end_Flag is True:
        # 再次操作时，可以先延时0.5s
        time.sleep(0.5)
        print "延时了0.5s"
        fileInfolderName = fileInFolder(path)
        fileInfolderNum = fileInfolderName.__len__()
        print "fileInfolderNum =", fileInfolderNum  # 统计图片数目
        print "fore_fileInfolderNum =", fore_fileInfolderNum  # 上一次统计图片的数目
        if fore_fileInfolderNum == fileInfolderNum:  # 如果前后两次图片数量相同，终止程序
            end_Flag = False
            break
        fore_fileInfolderNum = fileInfolderNum  # 如果前后两次图片数量不同，则继续对该文件夹操作

        for i in range(0, fileInfolderNum):
            print "fileInfoldeName[", i, "] =", fileInfolderName[i]
            error_Flag = cut_photo(fileInfolderName[i])
    end = time.time()
    print "program end ……"
    print ('spend time =', end - start, 's')
