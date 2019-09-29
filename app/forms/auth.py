"""
    Created by xukai on 2019/5/31
"""
from wtforms import Form, StringField, PasswordField
from wtforms.validators import Length, DataRequired, Email


class RegisterForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64), Email(message='电子邮箱不符合规范')])
    password = PasswordField(validators=[DataRequired(message='密码不可以为空，请输入你的密码'), Length(6, 32)])
    nickname = StringField(validators=[DataRequired(), Length(2, 10, message='昵称至少需要2个字符，最多10个字符')])
