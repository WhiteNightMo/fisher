from flask import flash, redirect, url_for, render_template, request
from flask_login import login_required, current_user
from sqlalchemy import desc, or_

from app.forms.book import DriftForm
from app.libs.email import send_mail
from app.libs.enums import PendingStatus
from app.models.base import db
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.user import User
from app.models.wish import Wish
from app.view_models.book import BookViewModel
from app.view_models.drift import DriftCollection
from . import web


@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):
    # 当前礼物
    current_gift = Gift.query.get_or_404(gid)

    # 不能向自己索要书籍
    if current_gift.is_yourself_gift(current_user.id):
        flash('不能向自己索要书籍')
        return redirect(url_for('web.book_detail', isbn=current_gift.isbn))

    # 是否能够发送鱼漂
    can = current_user.can_send_drift()
    if not can:
        return render_template('not_enough_beans.html', beans=current_user.beans)

    form = DriftForm(request.form)
    if request.method == 'POST' and form.validate():
        # 保存鱼漂信息, 发送邮件提醒
        save_drift(form, current_gift)
        send_mail(current_gift.user.email, '有人想要一本书', 'email/get_gift.html', wisher=current_user, gift=current_gift)
        return redirect(url_for('web.pending'))

        # 赠送者
    gifter = current_gift.user.summary
    return render_template('drift.html', gifter=gifter, user_beans=current_user.beans, form=form)


@web.route('/pending')
@login_required
def pending():
    # 我赠送的或者我索要的书籍列表
    drifts = Drift.query.filter(
        or_(Drift.requester_id == current_user.id, Drift.gifter_id == current_user.id)).order_by(
        desc(Drift.create_time)).all()

    # 将数据封装到数据模型中后, 传递给前端
    views = DriftCollection(drifts, current_user.id)
    return render_template('pending.html', drifts=views.data)


@web.route('/drift/<int:did>/reject')
@login_required
def reject_drift(did):
    """
    拒绝
    :param did:
    :return:
    """

    with db.auto_commit():
        drift = Drift.query.filter(Gift.uid == current_user.id, Drift.id == did).first_or_404()
        drift.pending = PendingStatus.Reject
        # 将鱼豆返还给索要者
        requester = User.query.get_or_404(drift.requester_id)
        requester.beans += 1
    return redirect(url_for('web.pending'))


@web.route('/drift/<int:did>/redraw')
@login_required
def redraw_drift(did):
    """
    撤销
    :param did:
    :return:
    """

    with db.auto_commit():
        drift = Drift.query.filter_by(requester_id=current_user.id, id=did).first_or_404()
        drift.pending = PendingStatus.Redraw
        # 撤销后鱼豆返还
        current_user.beans += 1
    return redirect(url_for('web.pending'))


@web.route('/drift/<int:did>/mailed')
@login_required
def mailed_drift(did):
    with db.auto_commit():
        drift = Drift.query.filter_by(gifter_id=current_user.id, id=did).first_or_404()
        drift.pending = PendingStatus.Success
        # 奖励当前用户一个鱼豆
        current_user.beans += 1
        # 礼物赠送成功
        Gift.query.filter_by(id=drift.grift_id).update({Gift.launched: True})
        # 心愿达成
        Wish.query.filter_by(isbn=drift.isbn, uid=drift.requester_id, launched=False).update({Wish.launched: True})
    return redirect(url_for('web.pending'))


def save_drift(drift_form, current_gift):
    """
    保存鱼漂信息
    :param drift_form:
    :param current_gift:
    :return:
    """

    with db.auto_commit():
        drift = Drift()
        drift_form.populate_obj(drift)

        drift.gift_id = current_gift.id
        drift.requester_id = current_user.id
        drift.requester_nickname = current_user.nickname
        drift.gifter_id = current_gift.user.id
        drift.gifter_nickname = current_gift.user.nickname

        # 书籍信息
        book = BookViewModel(current_gift.book)
        drift.book_title = book.title
        drift.book_author = book.author
        drift.book_img = book.image
        drift.isbn = book.isbn

        # 用户消耗一个鱼豆
        current_user.beans -= 1

        db.session.add(drift)
