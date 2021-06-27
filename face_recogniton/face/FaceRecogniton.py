import cv2
import os
import numpy as np
import win32com.client  # 用于tts，很难听
from MysqlControl import *
import datetime
from PIL import Image, ImageDraw, ImageFont


# 用于添加文字(解决cv2不能写中文的问题)
def cv2ImgAddText(img, text, left, top, textColor, textSize):
    if isinstance(img, np.ndarray):  # 判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img)
    # 字体的格式
    fontStyle = ImageFont.truetype(
        "font/simsun.ttc", textSize, encoding="utf-8")
    # 绘制文本
    draw.text((left, top), text, textColor, font=fontStyle)
    # 转换回OpenCV格式
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


def face_detect(img):
    face_detector = cv2.CascadeClassifier('./file/haarcascade_frontalface_alt2.xml')  # 人脸的级联分类器，训练根据haar特征
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 灰度
    faces = face_detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)     # 检测人脸的矩阵,前两个是左上坐标，后两个是宽高
    max_matrix = [0, 0, 0, 0]                           # 初始化矩阵
    for x, y, w, h in faces:                            # (x,y)是矩阵左上角坐标，w，h为宽的高
        if w * h >= max_matrix[2] * max_matrix[3]:      # 选出最大的矩阵
            max_matrix = [x, y, w, h]
    cv2.rectangle(img, (max_matrix[0], max_matrix[1]), (max_matrix[0] +
                                                        max_matrix[2], max_matrix[1] + max_matrix[3]), (255, 0, 0), 2)

    return img, max_matrix



def face_train():
    faces = []
    ids = []
    face_recognizer = cv2.face.LBPHFaceRecognizer_create(grid_x=16,
                                                         grid_y=16)  # 提取LBP特征，各小区域建立统计直方图，通过一系列公式判断相似性。grid_x,y为x,y方向长度
    face_img_paths = [os.path.join('dataset', img_name) for img_name in os.listdir('dataset')]  # 所有脸的路径的列表
    for face_img in face_img_paths:
        user_id = os.path.split(face_img)[-1].split('_')[0]
        img = cv2.imread(face_img, cv2.IMREAD_GRAYSCALE)  # 读为灰度图像
        img_numpy = np.array(img, 'uint8')  # 'uint8'为numpy一种数据类型，无符号整数（0 to 255）
        faces.append(img_numpy)  # 向训练集里添加新的图片数据
        ids.append(int(user_id))  # 添加新id
    face_recognizer.train(np.array(faces), np.array(ids))  # 训练新人脸
    face_recognizer.write('./file/train_result.yml')  # 将训练结果写入yml
    print('训练完成!')
    return


def read_train_data():

    face_recognizer = cv2.face.LBPHFaceRecognizer_create(grid_x=16,
                                                         grid_y=16)  # 提取LBP特征，各小区域建立统计直方图，通过一系列公式判断相似性。grid_x,y为x,y方向长度
    face_recognizer.read('./file/train_result.yml')  # 读取训练集

    return face_recognizer


def face_recognize(img, face_recognizer, type):
    face_detector = cv2.CascadeClassifier('./file/haarcascade_frontalface_alt2.xml')  # 人脸的级联分类器，训练根据haar特征
    img = cv2.flip(img, 1)    # 摄像头翻转
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 返回类型是数组
    faces = face_detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(50, 50))
    for x, y, w, h in faces:
        user_id, accuracy = face_recognizer.predict(gray[y:y + h, x:x + w])  # 检测到脸的区域数组与训练的数据对比预测
        if accuracy < 500 and type == 'check_in' and datetime.date.today() not in check_once(user_id):
            name = get_name(user_id)  # 词典中存放着id:name键值对
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)  # 起始坐标，颜色，厚度
            if accuracy <= 300:
                start = '*****'
                check_tts(name, type)
                date = datetime.date.today()
                start_time = datetime.datetime.now()
                check_in(start_time, date, str(user_id))
                print(str(name)+'于'+str(start_time)+'打卡成功！')
            elif accuracy <= 350:
                start = '****'
                check_tts(name, type)
                date = datetime.date.today()
                start_time = datetime.datetime.now()
                check_in(start_time, date, str(user_id))
                print(str(name)+'于'+str(start_time)+'打卡成功！')
            elif accuracy <= 400:
                start = '***'
            elif accuracy <= 450:
                start = '**'
            else:
                start = '*'
            img = cv2ImgAddText(img, name, x + 10, y - 25, (255, 255, 255), 25)  # 显示名字
            # cv2.putText(img, str(name), (x+10, y-10), cv2.FONT_ITALIC, 1, (255, 255, 255), 2)     # 显示名字(中文会乱码)
            cv2.putText(img, start, (x + 10, y + h - 10), cv2.FONT_ITALIC, 1, (255, 255, 0), 1)  # 显示准确度
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        elif accuracy < 500 and type == 'check_out' and datetime.date.today() in check_once(str(user_id)) and check_out_once(str(user_id), datetime.date.today()):
            name = get_name(user_id)       # 词典中存放着id:name键值对
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)  # 起始坐标，颜色，厚度
            if accuracy <= 300:
                start = '*****'
                check_tts(name, type)
                date = datetime.date.today()
                end_time = datetime.datetime.now()
                check_out(end_time, date, str(user_id))
                print(str(name) + '于' + str(end_time) + '签退成功！')
            elif accuracy <= 350:
                start = '****'
                check_tts(name, type)
                date = datetime.date.today()
                end_time = datetime.datetime.now()
                check_out(end_time, date, str(user_id))
                print(str(name) + '于' + str(end_time) + '签退成功！')
            elif accuracy <= 400:
                start = '***'
            elif accuracy <= 450:
                start = '**'
            else:
                start = '*'
            img = cv2ImgAddText(img, name, x + 10, y - 25, (255, 255, 255), 25)  # 显示名字
            # cv2.putText(img, str(name), (x+10, y-10), cv2.FONT_ITALIC, 1, (255, 255, 255), 2)     # 显示名字(中文会乱码)
            cv2.putText(img, start, (x + 10, y + h - 10), cv2.FONT_ITALIC, 1, (255, 255, 0), 1)  # 显示准确度
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    return img


def check_tts(name, type):
    if type == 'check_in':
        time = datetime.datetime.now().strftime('%H %M')
        time = time.split(' ')[0] + '时' + time.split(' ')[1] + '分'
        speaker = win32com.client.Dispatch('SAPI.spVoice')
        speaker.Speak(f'{name}于{time}打卡成功')
    elif type == 'check_out':
        time = datetime.datetime.now().strftime('%H %M')
        time = time.split(' ')[0] + '时' + time.split(' ')[1] + '分'
        speaker = win32com.client.Dispatch('SAPI.spVoice')
        speaker.Speak(f'{name}于{time}签退成功')