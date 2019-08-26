"""
    Created by xukai on 2019/5/30
"""

from app.libs.http import HTTP
from flask import current_app


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

        url = self.isbn_url.format(isbn)
        result = HTTP.get(url)
        self.__fill_single(result)

    def search_by_keyword(self, keyword, page=1):
        """
        根据关键字搜索
        :param keyword: 关键字
        :param page: 页码
        :return:
        """

        url = self.keyword_url.format(keyword, current_app.config['PER_PAGE'], self.calculate_start(page))
        result = HTTP.get(url)
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
