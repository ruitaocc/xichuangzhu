# coding: utf-8
from flask_wtf import Form
from wtforms import TextField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email


class WorkForm(Form):
    """Form for add and edit work"""
    title = TextField('标题', [DataRequired('标题不能为空')])
    type_id = SelectField('类别', [DataRequired("类别不能为空")], coerce=int)
    author_id = SelectField('作者', [DataRequired('作者不能为空')], coerce=int)
    foreword = TextAreaField('序')
    intro = TextAreaField('题解')
    content = TextAreaField('内容', [DataRequired('内容不能为空')])


class AuthorForm(Form):
    name = TextField('姓名', [DataRequired('姓名不能为空')])
    abbr = TextField('拼音缩写', [DataRequired('拼音缩写不能为空')])
    dynasty_id = SelectField('朝代', [DataRequired('朝代不能为空')], coerce=int)
    birth_year = TextField('生年', [DataRequired('生年不能为空')])
    death_year = TextField('卒年')
    intro = TextAreaField('简介', [DataRequired('简介不能为空')])