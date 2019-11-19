"""
    Created by xukai on 2019/5/31
"""

from flask import Blueprint, render_template

# 蓝图
web = Blueprint('web', __name__)


# 使用app_errorhandler装饰器监听404异常
@web.app_errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


from app.web import auth, main, book, drift, gift, wish
