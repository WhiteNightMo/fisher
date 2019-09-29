"""
    Created by xukai on 2019/6/3
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, SmallInteger

db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True
    # create_time = Column('create_time', Integer)
    status = Column(SmallInteger, default=1)

    def set_attrs(self, attrs_dict):
        """
        给对象设置属性
        :param attrs_dict:
        :return:
        """
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)
