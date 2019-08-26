"""
    Created by xukai on 2019/5/30
"""
import json

from flask import jsonify, request

from app.forms.book import SearchForm
from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShuBook
from app.view_models.book import BookCollection
from . import web


# @web.route('/book/search/<q>/<page>')
@web.route('/book/search')
def search():
    """
    搜索
    :param q: isbn或者普通关键字
    :param page: 页码
    :return: json
    """
    # ?q=xxx&page=1 格式url获取参数
    # q = request.args['q']
    # page = request.args['page']

    # 使用wtforms验证参数ps
    form = SearchForm(request.args)
    # 存储整理后的搜索结果
    books = BookCollection()

    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        # 判断搜索字段是isbn还是普通关键字
        isbn_or_key = is_isbn_or_key(q)
        # 爬虫 获取搜索结果
        yushu_book = YuShuBook()

        if isbn_or_key == 'isbn':
            yushu_book.search_by_isbn(q)
        else:
            yushu_book.search_by_keyword(q, page)

        # 整理搜索结果
        books.fill(yushu_book)
        # 对象需要使用__dict__属性转换成字典才能json化，递归将对象转换成字典再json化
        return json.dumps(books, default=lambda o: o.__dict__)
    else:
        return jsonify(form.errors)
