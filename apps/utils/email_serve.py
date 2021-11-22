
import smtplib
#发送字符串的邮件
from email.mime.text import MIMEText
#处理多种形态的邮件主体我们需要 MIMEMultipart 类
from email.mime.multipart import MIMEMultipart
#处理图片需要 MIMEImage 类
from email.mime.image import MIMEImage

# 新浪邮箱设置
HOST='smtp.sina.com'
PORT=465
ACCOUNT='用户名@sina.com'
PASSWORD='926f94947f38a12c'
 


def mail(toaddrs,subject,content):
    #设置email信息
    #---------------------------发送字符串的邮件-----------------------------
    #邮件内容设置
    message = MIMEText(content,'plain','utf-8')
    #邮件主题       
    message['Subject'] = subject
    #发送方信息
    message['From'] = ACCOUNT
    #接受方信息     
    message['To'] = toaddrs  
    #---------------------------------------------------------------------
    #登录并发送邮件
    try:
        server = smtplib.SMTP_SSL(HOST,PORT)#163邮箱服务器地址，端口默认为25
        # server=smtplib.SMTP("wm.yufanlogistics.com",25)
        server.login(ACCOUNT,PASSWORD)
        server.sendmail(ACCOUNT, toaddrs, message.as_string())
        server.quit()
        return True
    
    except smtplib.SMTPException as e:
        return False
if __name__=="__main__":
    toaddrs = '510763683@qq.com' #邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
    subject="忘记密码"
    content="请使用密码登录"
    mail(toaddrs,subject,content)