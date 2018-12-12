# encoding: utf-8
# 这个函数主要是检测一张图片中有多少个人
from aip import AipFace
import base64

""" 你的 APPID AK SK """
APP_ID = '14803185'
API_KEY = '4FmR91rWRKiyxtkvrSNrsDro'
SECRET_KEY = 'Ed4spz5GdjbxfQCfAGfiko8KXd9q0fC4'

client = AipFace(APP_ID, API_KEY, SECRET_KEY)
print(client)


def face_detection_face_num(image_name):
    image = base64.b64encode(open(image_name, 'rb').read())
    image_type = "BASE64"
    """调用人脸检测"""
    options = {}
    options["max_face_num"] = 10

    result = client.detect(image, image_type, options)
    return result


if __name__ == "__main__":
    image1 = "E:\\000007work\\laji\\m.0b4q0d_35-FaceId-0.jpg"
    result = face_detection_face_num(image1)
    goal = result.get('result')         # 获取result部分的值
    face_num = goal.get('face_num')     # 获取face_num部分的值
    print "face_num =", face_num        # 打印face_num的值

