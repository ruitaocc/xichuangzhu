# coding: utf-8
from flask_wtf import Form
from wtforms import TextField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Email


class SignupForm(Form):
    """Form for send email"""
    user_id = HiddenField('用户ID', [DataRequired(message="用户ID不能为空")])
    name = TextField('名号', [])
    abbr = TextField('我的域名', [])
    # signature = TextAreaField('个性签名')
    email = TextField('邮箱', [DataRequired(message="邮箱不能为空"), Email(message="无效的邮箱")],
                      description='你常用的邮箱')
