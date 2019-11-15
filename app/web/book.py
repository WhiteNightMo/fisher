"""
    Created by xukai on 2019/5/30
"""

from flask import request, render_template, flash
from flask_login import current_user

from app.forms.book import SearchForm
from app.libs.helper import is_isbn_or_key
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook
from app.view_models.book import BookCollection, BookViewModel
from app.view_models.trade import TradeInfo
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
        books.fill(yushu_book, q)
        # 对象需要使用__dict__属性转换成字典才能json化，递归将对象转换成字典再json化
        # return json.dumps(books, default=lambda o: o.__dict__)
    else:
        flash('搜索的关键字不符合要求，请重新输入关键字')
        # return jsonify(form.errors)
    return render_template('search_result.html', books=books)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    has_in_gifts = False
    has_in_wishes = False

    # 取书籍详情数据
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn=isbn)
    book = BookViewModel(yushu_book.first)

    # 登录后判断，当前书籍是否已经在心愿和赠送清单
    if current_user.is_authenticated:
        if Gift.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first():
            has_in_wishes = True

    # 获取书籍的赠送和心愿列表
    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishes_model = TradeInfo(trade_wishes)
    trade_gifts_model = TradeInfo(trade_gifts)

    return render_template('book_detail.html', book=book, wishes=trade_wishes_model, gifts=trade_gifts_model,
                           has_in_gifts=has_in_gifts, has_in_wishes=has_in_wishes)
