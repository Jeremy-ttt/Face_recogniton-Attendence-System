import cv2
from tkinter import *
import FaceRecogniton
from PIL import Image, ImageTk
from tkinter import messagebox
from MysqlControl import *
import hashlib


# 初始化
root = Tk()
root.title('人脸识别考勤系统')
root.geometry('1000x600')
root.wm_resizable(False, False)
cap = cv2.VideoCapture(0)
count = 0
detect_go = True
recognize_go = False
check_in = False
check_out = False




def main():
    global b1,b4,b3,button_train
    b1 = Button(root, text='人脸签到', width=15, height=2, command=lambda: recognize('check_in'))
    b4 = Button(root, text='人脸签退', width=15, height=2, command=lambda: recognize('check_out'))
    b3 = Button(root, text='添加人脸', width=15, height=2, command=button_add_face)
    button_train = Button(root, text='训练人脸', width=15, height=2, command=FaceRecogniton.face_train)
    b1.place(x=850, y=150)
    b3.place(x=850, y=300)
    b4.place(x=850, y=200)
    button_train.place(x=850, y=450)


def destroy():
    frame_h.destroy()
    frame_l.destroy()
    frame_m.destroy()
    frame_c.destroy()
    frame_e.destroy()
    frame_phone.destroy()
    frame_pwd.destroy()
    ok_button.destroy()



def tkImage1():
    _, img = cap.read()
    global max_matrix
    img, max_matrix = FaceRecogniton.face_detect(img)
    img = cv2.flip(img, 1)    # 摄像头翻转
    cv_image = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    pil_image = Image.fromarray(cv_image)
    pil_image = pil_image.resize((800, 600), Image.ANTIALIAS)
    tkImage = ImageTk.PhotoImage(image=pil_image)

    return tkImage


def tkImage2(face_recoginizer):
    _, img = cap.read()
    global check_in, check_out
    if check_in == False and check_out == True:
        type = 'check_out'
    elif check_in == True and check_out == False:
        type = 'check_in'
    img = FaceRecogniton.face_recognize(img, face_recoginizer, type)
    cv_image = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    pil_image = Image.fromarray(cv_image)
    pil_image = pil_image.resize((800, 600), Image.ANTIALIAS)
    tkImage = ImageTk.PhotoImage(image=pil_image)

    return tkImage





def save_id(user_id, password, name, phone, email, cid, major_id, gender=1):
    destroy()
    b2.place(x=800, y=300)
    add_user(user_id, password, name, phone, email, cid, major_id)
    print(str(name)+'数据保存成功')



def button_save(id, name):
    global count
    count += 1
    _, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    save_path = './dataset/'+str(id)+'_'+name+'_'+str(count)+'.jpg'
    src = gray[max_matrix[1]:max_matrix[1]+max_matrix[3], max_matrix[0]:max_matrix[0]+max_matrix[2]]
    # cv2.imwrite(save_path, gray[max_matrix[1]:max_matrix[1]+max_matrix[3], max_matrix[0]:max_matrix[0]+max_matrix[2]])
    # 用于解决保存中文路径图片乱码。
    cv2.imencode('.jpg', src)[1].tofile(save_path)


def button_back():
    destroy()
    back_button.destroy()
    b2.destroy()
    main()


def button_cancel():
    global recognize_go
    recognize_go = False
    cancel_button.destroy()
    main()
    detect()
    root.mainloop()
    cap.release()


def sha1(pwd):
    m1 = hashlib.sha1()
    m1.update(pwd.encode('utf8'))
    pwd = m1.hexdigest()
    return pwd


def button_add_face():
    global b1,b4,b3,button_train
    b1.destroy()
    b4.destroy()
    b3.destroy()
    button_train.destroy()
    id = StringVar()
    name = StringVar()
    pwd = StringVar()
    phone = StringVar()
    email = StringVar()
    class_id = StringVar()
    major_id = StringVar()
    global frame_h, frame_l,frame_m,frame_c,frame_e,frame_phone,frame_pwd,back_button,ok_button,b2
    frame_h = Frame(root)
    frame_l = Frame(root)
    frame_m = Frame(root)
    frame_c = Frame(root)
    frame_e = Frame(root)
    frame_phone = Frame(root)
    frame_pwd = Frame(root)
    name_label = Label(frame_h, text="姓名：")
    id_label = Label(frame_l, text="学号：")
    major_label = Label(frame_m, text='专业：')
    class_label = Label(frame_c, text='班级：')
    phone_label = Label(frame_phone, text='手机：')
    email_label = Label(frame_e, text='邮箱：')
    pwd_label = Label(frame_pwd, text='密码：')
    name_entry = Entry(frame_h, textvariable=name)
    id_entry = Entry(frame_l, textvariable=id)
    major_entry = Entry(frame_m, textvariable=major_id)
    class_entry = Entry(frame_c, textvariable=class_id)
    phone_entry = Entry(frame_phone, textvariable=phone)
    email_entry = Entry(frame_e, textvariable=email)
    pwd_entry = Entry(frame_pwd, textvariable=pwd)
    b2 = Button(root, text='添加此人脸', width=15, height=2,
                command=lambda: button_save(id.get(), name.get()))
    ok_button = Button(root, text="确认", width=25,
                       command=lambda: save_id(id.get(), sha1(pwd.get()), name.get(), str(phone.get()), email.get(),
                                               '1', '1'))
    back_button = Button(root, text='返回', width=25, command=button_back)
    name_label.pack(side='left', fill="both", padx=5, pady=5)
    name_entry.pack(side="right", fill="both", padx=5, pady=5)
    id_label.pack(side="left", fill="both", padx=5, pady=5)
    id_entry.pack(side="right", fill="both", padx=5, pady=5)
    major_label.pack(side='left', fill="both", padx=5, pady=5)
    major_entry.pack(side='right', fill="both", padx=5, pady=5)
    class_label.pack(side='left', fill="both", padx=5, pady=5)
    class_entry.pack(side='right', fill="both", padx=5, pady=5)
    email_label.pack(side='left', fill="both", padx=5, pady=5)
    email_entry.pack(side='right', fill="both", padx=5, pady=5)
    phone_label.pack(side='left', fill="both", padx=5, pady=5)
    phone_entry.pack(side='right', fill="both", padx=5, pady=5)
    pwd_label.pack(side='left', fill="both", padx=5, pady=5)
    pwd_entry.pack(side='right', fill="both", padx=5, pady=5)
    ok_button.pack(side="bottom", fill="y", ipadx=5, pady=5)
    frame_h.pack()
    frame_l.pack()
    frame_c.pack()
    frame_m.pack()
    frame_e.pack()
    frame_phone.pack()
    frame_pwd.pack()
    frame_h.place(x=800, y=0)
    frame_l.place(x=800, y=30)
    frame_m.place(x=800, y=60)
    frame_c.place(x=800, y=90)
    frame_e.place(x=800, y=120)
    frame_phone.place(x=800, y=150)
    frame_pwd.place(x=800, y=180)
    ok_button.place(x=800, y=220)
    back_button.place(x=800, y=250)
    b2.place(x=800, y=400)





def detect():
    canvas = Canvas(root, bg='white', width=800, height=600)
    canvas.place(x=0, y=0)
    while detect_go:
        img = tkImage1()
        canvas.create_image(0, 0, anchor='nw', image=img)
        root.update()
        # root.after(100)   # 延迟
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


# 用于人脸签到和人脸签退
def recognize(type):
    if type == 'check_in':
        button_check_in()
    elif type == 'check_out':
        button_check_out()
    global recognize_go
    recognize_go = True
    canvas = Canvas(root, bg='white', width=800, height=600)
    canvas.place(x=0, y=0)
    global b1,b4,b3
    b1.destroy()
    b4.destroy()
    b3.destroy()
    button_train.destroy()
    global cancel_button
    cancel_button = Button(root, text='取消识别', width=25, command=button_cancel)
    cancel_button.place(x=800, y=250)
    face_recognizer = FaceRecogniton.read_train_data()
    while recognize_go:
        img = tkImage2(face_recognizer)
        canvas.create_image(0, 0, anchor='nw', image=img)
        root.update()
        # root.after(100)             # 加延迟
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


# 点击❌关闭窗口时同时关闭人脸检测和人脸识别，防止报错
def on_closing():
    global detect_go
    detect_go = False
    global recognize_go
    recognize_go = False
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
    else:
        detect_go = True
        recognize_go = True


# 用于确认是签到还是签退
def button_check_in():
    global check_in, check_out
    check_in = True
    check_out = False


# 用于确认是签到还是签退
def button_check_out():
    global check_in, check_out
    check_in = False
    check_out = True



root.protocol("WM_DELETE_WINDOW", on_closing)




if __name__ == '__main__':
    main()
    detect()
    root.mainloop()
    cap.release()