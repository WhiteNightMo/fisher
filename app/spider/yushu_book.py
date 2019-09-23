"""
    Created by xukai on 2019/5/30
"""

from flask import current_app
from sqlalchemy import or_

from app.libs.http import HTTP
from app.models.book import Book, db


class YuShuBook:
    """
    爬虫 搜索并存储搜索结果
    """

    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    def __init__(self):
        """
        保存从接口获数据库获取的原数据
        """
        self.total = 0
        self.books = []

    def search_by_isbn(self, isbn):
        """
        根据isbn搜索
        :param isbn: isbn号
        :return:
        """
        # 先检索数据库，再通过API搜索
        result = Book.query.filter_by(isbn=isbn).first()
        if result:
            result = result.__dict__
        else:
            url = self.isbn_url.format(isbn)
            result = HTTP.get(url)
            self.__save(result)
        self.__fill_single(result)

    def search_by_keyword(self, keyword, page=1):
        """
        根据关键字搜索
        :param keyword: 关键字
        :param page: 页码
        :return:
        """
        # 先检索数据库，再通过API搜索
        result = Book.query.filter(or_(Book.title.contains(keyword), Book.author.contains(keyword))).all()
        if result:
            books = []
            for book in result:
                books.append(book.__dict__)
            result.clear()
            result = {'books': books, 'total': len(books)}
        else:
            url = self.keyword_url.format(keyword, current_app.config['PER_PAGE'], self.calculate_start(page))
            result = HTTP.get(url)
            self.__save(result)
        self.__fill_collection(result)

    def __fill_single(self, data):
        if data:
            self.total = 1
            self.books.append(data)

    def __fill_collection(self, data):
        if data:
            self.total = data['total']
            self.books = data['books']

    @staticmethod
    def calculate_start(page):
        return (page - 1) * current_app.config['PER_PAGE']

    @staticmethod
    def __save(data):
        """
        保存到数据库
        :param data:
        :return:
        """
        if 'books' not in data.keys():
            data['books'] = [data]
        if data['books']:
            for item in data['books']:
                # 已存在的不需要插入
                count = Book.query.filter_by(isbn=item['isbn']).count()
                if count == 0:
                    book = Book(title=item['title'], author='、'.join(item['author']), binding=item['binding'],
                                publisher=item['publisher'], price=item['price'], pages=item['pages'],
                                pubdate=item['pubdate'], isbn=item['isbn'], summary=item['summary'],
                                image=item['image'])
                    db.session.add(book)
            db.session.commit()
