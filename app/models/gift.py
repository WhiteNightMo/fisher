"""
    Created by xukai on 2019/6/3
"""
from flask import current_app
from sqlalchemy import Column, Integer, Boolean, String, ForeignKey, desc, func
from sqlalchemy.orm import relationship

from app.models.base import Base, db
from app.spider.yushu_book import YuShuBook


class Gift(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)
    _book = relationship('Book')
    bid = Column(Integer, ForeignKey('book.id'))
    launched = Column(Boolean, default=False)

    def is_yourself_gift(self, uid):
        """
        判断是否是你的礼物
        :param uid:
        :return:
        """

        return True if self.uid == uid else False

    @classmethod
    def get_user_gifts(cls, uid):
        """
        获取用户的所有未赠送出去的礼物
        :param uid:
        :return:
        """

        gifts = Gift.query.filter_by(uid=uid, launched=False).order_by(desc(Gift.create_time)).all()
        return gifts

    @classmethod
    def get_wish_counts(cls, isbn_list):
        """
        根据isbn列表, 获取礼物的心愿数量
        :param isbn_list:
        :return:
        """

        from app.models.wish import Wish
        count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(
            Wish.launched == False,
            Wish.isbn.in_(isbn_list),
            Wish.status == 1).group_by(Wish.isbn).all()
        # 元组=>字典
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list

    @property
    def book(self):
        """
        获取礼物中的书籍
        :return:
        """

        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    @classmethod
    def recent(cls):
        """
        获取最近礼物列表
        :return:
        """

        # 根据时间倒序,isbn去重,取出指定数量的礼物
        recent_gift = Gift.query.filter_by(launched=False).group_by(Gift.isbn).order_by(desc(Gift.create_time)).limit(
            current_app.config['RECENT_BOOK_COUNT']).distinct().all()
        return recent_gift
