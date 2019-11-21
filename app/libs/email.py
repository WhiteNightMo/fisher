"""
    Created by xukai on 2019/11/19
"""
from threading import Thread

from flask import current_app, render_template
from flask_mail import Message

from app import mail


def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            pass


def send_mail(to, subject, template, **kwargs):
    msg = Message(current_app.config['MAIL_SUBJECT_PREFIX'] + ' ' + subject, sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to])
    # 将渲染后的html作为邮件内容发送
    msg.html = render_template(template, **kwargs)
    # 开辟新线程发送邮件(current_app是主线程的代理对象，开辟新线程后内部为空)
    # 获取当前主线程的Flask核心对象，直接当作参数传递
    app = current_app._get_current_object()
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
