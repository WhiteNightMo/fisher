"""
    Created by xukai on 2019/5/31
"""

from flask import Blueprint

# 蓝图
web = Blueprint('web', __name__)

from app.web import auth, book, drift, gift, main, wish
