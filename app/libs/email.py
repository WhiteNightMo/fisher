"""
    Created by xukai on 2019/11/19
"""
from flask import current_app, render_template
from flask_mail import Message

from app import mail


def send_mail(to, subject, template, **kwargs):
    msg = Message(current_app.config['MAIL_SUBJECT_PREFIX'] + ' ' + subject, sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to])
    # 将渲染后的html作为邮件内容发送
    msg.html = render_template(template, **kwargs)
    mail.send(msg)
