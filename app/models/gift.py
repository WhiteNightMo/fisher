"""
    Created by xukai on 2019/6/3
"""

from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base


class Gift(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    # isbn = Column(String(15), nullable=False)
    book = relationship('Book')
    bid = Column(Integer, ForeignKey('user.id'))
    launched = Column(Boolean, default=False)
