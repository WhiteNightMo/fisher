"""
    Created by xukai on 2019/6/3
"""

from sqlalchemy import Column, Integer, String, Text

from app.models.base import Base


class Book(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    author = Column(String(80), default='未名')
    binding = Column(String(20))  # 精装|平装
    publisher = Column(String(50))  # 出版社
    price = Column(String(20))  # 单价
    pages = Column(String(10))  # 页数
    pubdate = Column(String(20))  # 出版时间
    isbn = Column(String(15), nullable=False, unique=True)
    summary = Column(Text())  # 简介
    image = Column(String(50))  # 封面
