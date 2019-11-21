"""
    Created by xukai on 2019/5/31
"""
from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length, NumberRange, DataRequired, Regexp


class SearchForm(Form):
    q = StringField(validators=[DataRequired(), Length(1, 30)])
    page = IntegerField(validators=[NumberRange(1, 99)], default=1)


class DriftForm(Form):
    recipient_name = StringField(validators=[DataRequired(), Length(min=2, max=20, message='收件人姓名长度必须在2到20个字符之间')])
    mobile = StringField(validators=[DataRequired(), Regexp('^1[0-9]{10}$', 0, '请输入正确的手机号')])
    message = StringField()
    address = StringField(validators=[DataRequired(), Length(min=10, max=70, message='地址长度必须在10到70个字符之间')])
