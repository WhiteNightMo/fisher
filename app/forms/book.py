"""
    Created by xukai on 2019/5/31
"""
from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length, NumberRange, DataRequired


class SearchForm(Form):
    q = StringField(validators=[DataRequired(), Length(1, 30)])
    page = IntegerField(validators=[NumberRange(1, 99)], default=1)
