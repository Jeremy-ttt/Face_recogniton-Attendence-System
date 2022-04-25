import smtplib
from email.mime.text import MIMEText
from email.header import Header




def send_email(email, captcha):
    mail_host = "smtp.qq.com"  # 设置服务器
    mail_user = "1438887803@qq.com"  # 用户名
    mail_pass = "cyleylilikbqhgfh"  # 口令

    sender = '1438887803@qq.com'

    receivers = [f'{email}']

    message = MIMEText(f'好兄弟你的验证码是:{captcha},不要丢了=.=', 'plain', 'utf-8')
    message['From'] = Header("考勤密码修改", 'utf-8')
    message['To'] = Header("账户", 'utf-8')
    subject = '验证码'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 587)    # 587 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")