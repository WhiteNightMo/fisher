"""
    Created by xukai on 2019/5/31
"""
from flask import Flask
from app.models.base import db
from flask_login import LoginManager
from flask_mail import Mail

login_manage = LoginManager()
mail = Mail()


def create_app():
    """
    创建Flask实例对象
    :return: Flask实例对象
    """
    app = Flask(__name__)

    # 导入配置文件
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')

    # 注册蓝图
    register_blueprint(app)

    # 使用flask-login插件管理登录cookie
    login_manage.init_app(app)
    # 指定登录视图函数，以及未登录的提示
    login_manage.login_view = 'web.login'
    login_manage.login_message = '请先登录或注册'

    # 初始化flask-mail插件
    mail.init_app(app)

    # 实例化数据库对象
    db.init_app(app)
    # 根据模型生成数据表，需要app
    # 1. 直接传递app对象
    # db.create_all(app=app)
    # 2. 使用with语句获取AppContext对象，create_all方法内部自动根据AppContext对象获取app
    with app.app_context():
        db.create_all()

    return app


def register_blueprint(app):
    """
    注册蓝图
    :param app: Flask实例对象
    :return: None
    """
    from app.web import web
    app.register_blueprint(web)
