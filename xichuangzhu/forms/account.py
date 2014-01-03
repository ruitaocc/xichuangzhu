# coding: utf-8
from flask_wtf import Form
from wtforms import TextField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileField, FileAllowed, FileRequired


class EmailForm(Form):
    """Form for send email"""
    email = TextField('邮箱', [DataRequired(message="邮箱不能为空"), Email(message="无效的邮箱")])
    user_id = HiddenField('用户ID', [DataRequired(message="用户ID不能为空")])