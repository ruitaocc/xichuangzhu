#-*- coding: UTF-8 -*-
from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, HiddenField, validators
from flask_wtf.file import FileField, FileAllowed, FileRequired

# Review form
class ReviewForm(Form):
    title = TextField('标题', [
        validators.Required(message="标题不能为空")
    ])
    
    content = TextAreaField('内容', [
        validators.Required(message="内容不能为空")
    ])

# Topic form
class TopicForm(Form):
    node_id = HiddenField('节点', [])
    
    title = TextField('标题', [
        validators.Required(message="标题不能为空")
    ])

    content = TextAreaField('内容', [
        validators.Required(message="内容不能为空")
    ])

# Comment form
class CommentForm(Form):
    comment = TextAreaField('回复', [
        validators.Required(message="回复不能为空")
    ])

# Email form
class EmailForm(Form):
    email = TextField('邮箱', [
        validators.Email(message="无效的邮箱"),
        validators.Required(message="邮箱不能为空")
    ])

    user_id = HiddenField('用户ID', [
        validators.Required(message="用户ID不能为空")
    ])

# Work image form
class WorkImageForm(Form):
    image = FileField('作品', [
        FileRequired('作品不能为空'),
        # FileAllowed(['jpg', 'jpeg', 'png', 'bmp', 'gif'], '仅限png/jpg/jpeg/bmp/gif格式的图片')
    ])