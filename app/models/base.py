"""
    Created by xukai on 2019/6/3
"""
from contextlib import contextmanager
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import Column, SmallInteger, Integer


class SQLAlchemy(_SQLAlchemy):
    """
    继承flask_sqlalchemy的SQLAlchemy
    """

    @contextmanager
    def auto_commit(self):
        """
        使用内容管理器和yield实现try-except封装，以及事务自动commit和rollback
        :return:
        """
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


class Query(BaseQuery):
    """
    继承flask_sqlalchemy的BaseQuery，它又继承sqlalchemy的Query
    """

    def filter_by(self, **kwargs):
        """
        重写filter_by函数，给查询参数中添加status=1
        :param kwargs:
        :return:
        """

        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super(Query, self).filter_by(**kwargs)


# 实例化db对象
db = SQLAlchemy(query_class=Query)


class Base(db.Model):
    __abstract__ = True
    create_time = Column('create_time', Integer)
    status = Column(SmallInteger, default=1)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    def set_attrs(self, attrs_dict):
        """
        给对象设置属性
        :param attrs_dict:
        :return:
        """
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    @property
    def create_datetime(self):
        """
        将int类型的create_time转换为时间类型
        :return:
        """

        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None
