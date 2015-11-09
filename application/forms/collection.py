# coding: utf-8
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired


class CollectionForm(Form):
    name = StringField('名称', validators=[DataRequired('集合名称不能为空')])

