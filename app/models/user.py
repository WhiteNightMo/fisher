"""
    Created by xukai on 2019/6/3
"""
from math import floor

from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean, Float
from werkzeug.security import generate_password_hash, check_password_hash

from app import login_manage
from app.libs.enums import PendingStatus
from app.libs.helper import is_isbn_or_key
from app.models.base import Base, db
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook


class User(UserMixin, Base):
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    _password = Column('password', String(128), nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self.password, raw)

    def generate_token(self, expires=600):
        """
        生成重置密码token
        :param expires:
        :return:
        """

        s = Serializer(current_app.config['SECRET_KEY'], expires)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        # 读取token中的用户ID
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False

        # 更新密码
        uid = data.get('id')
        with db.auto_commit():
            user = User.query.get(uid)
            user.password = new_password
        return True

    # 如果不存在id字段，需覆盖UserMixin的get_id函数指定当前模型的唯一标识
    # def get_id(self):
    #     return self.id

    def can_save_to_list(self, isbn):
        """
        是否能添加到赠送或心愿清单
        :param isbn:
        :return:
        """

        if is_isbn_or_key(isbn) != 'isbn':
            return False
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(isbn)
        if not yushu_book.first:
            return False

        # 既不在赠送清单，也不在心愿清单才能添加
        gifting = Gift.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        if not gifting and not wishing:
            return True
        else:
            return False

    def can_send_drift(self):
        """
        是否能发送鱼漂
        :return:
        """

        # 鱼豆是否充足
        if self.beans < 1:
            return False

        # 成功赠送的数量
        success_gifts_count = Gift.query.filter_by(uid=self.id, launched=True).count()
        # 成功接收的数量
        success_receive_count = Drift.query.filter_by(requester_id=self.id, pending=PendingStatus.Success).count()
        # 每索要两本书，必须送出一本书
        return True if floor(success_receive_count / 2) <= floor(success_gifts_count) else False

    @property
    def summary(self):
        """
        用户简略信息
        :return:
        """

        return dict(
            nickname=self.nickname,
            beans=self.beans,
            email=self.email,
            send_receive=str(self.send_counter) + '/' + str(self.receive_counter)
        )


@login_manage.user_loader
def get_user(uid):
    return User.query.get(int(uid))
