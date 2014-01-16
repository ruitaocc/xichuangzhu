# coding: utf-8
from flask_wtf import Form
from wtforms import TextField, TextAreaField, SelectField, IntegerField, HiddenField
from wtforms.validators import DataRequired


class WorkForm(Form):
    """Form for add & edit work"""
    title = TextField('标题', [DataRequired('标题不能为空')])
    type_id = SelectField('类别', [DataRequired("类别不能为空")], coerce=int)
    author_id = SelectField('作者', [DataRequired('作者不能为空')], coerce=int)
    foreword = TextAreaField('序')
    intro = TextAreaField('题解')
    content = TextAreaField('内容', [DataRequired('内容不能为空')])


class AuthorForm(Form):
    """Form for add & edit author"""
    name = TextField('姓名', [DataRequired('姓名不能为空')])
    abbr = TextField('拼音', [DataRequired('拼音不能为空')])
    dynasty_id = SelectField('朝代', [DataRequired('朝代不能为空')], coerce=int)
    birth_year = TextField('生年', [DataRequired('生年不能为空')])
    death_year = TextField('卒年')
    intro = TextAreaField('简介', [DataRequired('简介不能为空')])


class AuthorQuoteForm(Form):
    """Form for add & edit author quote"""
    quote = TextField('引语', [DataRequired('引语不能为空')])
    work_id = IntegerField('出处', [DataRequired('出处不能为空')])
    author_id = HiddenField('作者', [DataRequired('作者不能为空')])


class DynastyForm(Form):
    """Form for add & edit dynasty"""
    name = TextField('朝代', [DataRequired('朝代不能为空')])
    abbr = TextField('拼音', [DataRequired('拼音不能为空')])
    intro = TextAreaField('简介', [DataRequired('简介不能为空')])
    start_year = IntegerField('起始年', [DataRequired('起始年不能为空')])
    end_year = IntegerField('结束年', [DataRequired('结束年不能为空')])