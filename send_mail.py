import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 邮箱配置
smtp_server = "smtp.163.com"       # 163 邮箱 SMTP
smtp_port = 465
from_addr = "youremail@email.com"
password = "授权码"            # 不是邮箱密码，是授权码
to_addr = "youremail@email.com"

def send_email(subject, content):
    msg = MIMEText(content, "plain", "utf-8")
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg["Subject"] = Header(subject, "utf-8")

    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())


