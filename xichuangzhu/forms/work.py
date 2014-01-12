# coding: utf-8
from flask_wtf import Form
from wtforms import TextField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileField, FileAllowed, FileRequired


class WorkReviewForm(Form):
    """Form for add and edit work review"""
    title = TextField('标题', [DataRequired(message="标题不能为空")])
    content = TextAreaField('内容', [DataRequired(message="内容不能为空")])


class WorkReviewCommentForm(Form):
    """Form for add comment to work review"""
    content = TextAreaField('回复', [DataRequired(message="回复不能为空")])


class WorkImageForm(Form):
    """Form for add and edit work image"""
    image = FileField('作品', [FileRequired('作品图片不能为空')])