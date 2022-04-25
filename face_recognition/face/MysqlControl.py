import pymysql

db = pymysql.connect(host='127.0.0.1',
                     port=3306,
                     user='root',
                     password='tang6666',
                     database='check_system',
                     charset='utf8',
                     )
cursor = db.cursor()


# def get_mysql():
#
#     ids = 'select studentNum from app_userinfo'
#     name = 'select username from app_userinfo'
#     cursor.execute(ids)
#     print(cursor.fetchall())
#     cursor.execute(name)
#     print(cursor.fetchall())


# 获取这个学号的用户名字
def get_name(user_id):

    name = "select username from app_userinfo where studentNum = %d;" % (user_id)
    cursor.execute(name)
    name = cursor.fetchone()[0]
    return name


# 从数据库中获取这个用户，判断今天是否打过卡
def check_once(user_id):
    try:
        dates = []
        days = "select date from app_attendence where stu_id = %s;" % (user_id)
        cursor.execute(days)
        days = cursor.fetchall()
        for date in days:
            dates.append(date[0])
        return dates
    except:
        print(user_id+'今日未打过卡')
        return False


# 用于判断一天是否签退一次
def check_out_once(user_id, today):
    try:
        end = "select end_time from app_attendence where stu_id = %s and date = '%s';" % (user_id, today)
        cursor.execute(end)
        end = cursor.fetchone()[0]
        if end == None:
            return True
        else:
            print('今日已签退')
            return False
    except:
        print(user_id + '今日未打过卡')
        return False

# def get_end_time(user_id):
#     try:
#         ends = []
#         end = 'select end_time from app_attendence where stu_id = %s;' %(user_id)
#         cursor.execute(end)
#         ends = cursor.fetchall()
#         for i in ends:
#             ends.append(i[0])
#         return ends
#     except:
#         print(user_id+'未打过卡')
#         return False


def add_user(user_id, password, name, phone, email, cid, major_id, user_type_id=2,gender=1):
    add = 'insert into app_userinfo(STUDENTNUM, PASSWORD, USERNAME, GENDER, PHONE, EMAIL, CID_ID, MAJOR_ID,user_type_id) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
    cursor.execute(add, (user_id, password, name, gender, phone, email, cid, major_id, user_type_id))
    db.commit()


def check_in(start_time, date, user_id):
    attendence = 'insert into app_attendence(start_time, date, stu_id, duration, detail, is_leave, leave_count) values(%s,%s,%s,%s,%s,%s,%s);'
    cursor.execute(attendence, (start_time, date, user_id, '0', '0', '0', '0'))
    db.commit()



# 整句一定要用双引号！！！与数据库数据类型格式一定要一致
def check_out(end_time, date, user_id):
    start_time = "select start_time from app_attendence where stu_id = %s and date = '%s';" % (user_id, date)
    cursor.execute(start_time)
    try:
        start_time = cursor.fetchone()[0]
        out = "UPDATE app_attendence SET end_time = '%s' WHERE date = '%s' and stu_id = %s;" % (end_time, date, user_id)
        cursor.execute(out)
        db.commit()
        duration = round((end_time - start_time).seconds / 3600, 1)
        add_duration = "update app_attendence set duration = %f where date = '%s'  and stu_id = %s;" % (duration, date, user_id)
        cursor.execute(add_duration)
        db.commit()
    except Exception as e:
        print(e)
        print('签退失败!')