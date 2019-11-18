from flask import current_app, flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from app.models.base import db
from app.models.book import Book
from app.models.gift import Gift
from app.view_models.trade import MyTrades
from . import web


@web.route('/my/gifts')
@login_required
def my_gifts():
    uid = current_user.id
    # 获取当前用户未赠送的礼物列表
    gifts_of_mine = Gift.get_user_gifts(uid)
    # 获取isbn列表
    isbn_list = [gift.isbn for gift in gifts_of_mine]
    # 获取这些isbn的心愿数量
    wish_count_list = Gift.get_wish_counts(isbn_list)
    # 封装视图模型
    view_model = MyTrades(gifts_of_mine, wish_count_list)
    return render_template('my_gifts.html', gifts=view_model.trades)


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            gift = Gift()
            gift.uid = current_user.id
            gift.isbn = isbn
            # 获取book id
            book = Book.query.filter_by(isbn=isbn).first()
            gift.bid = book.id
            # 用户赠书增加鱼豆
            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
            db.session.add(gift)
    else:
        flash('这本书已添加至你的赠送清单或已存在于你的心愿清单，请不要重复添加')
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/gifts/<gid>/redraw')
@login_required
def redraw_from_gifts(gid):
    pass
