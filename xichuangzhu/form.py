#-*- coding: UTF-8 -*-

from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, HiddenField, validators

# Review form
class ReviewForm(Form):
	title = TextField('标题', [
		validators.Length(max=20, message="标题最多20个字哦"),
		validators.Required(message="标题不能为空")])
	
	content = TextAreaField('内容', [
		validators.Length(min=30, message="内容最少30个字哦"),
		validators.Required(message="内容不能为空")])

# Topic form
class TopicForm(Form):
	# node_id = HiddenField('节点', [
	# 	validators.Required(message="节点不能为空")])
	node_id = HiddenField('节点', [])
	
	title = TextField('标题', [
		validators.Length(max=30, message="标题最多30个字哦"),
		validators.Required(message="标题不能为空")])

	content = TextAreaField('内容', [
		validators.Required(message="内容不能为空")])

# Comment form
class CommentForm(Form):
	comment = TextAreaField('回复', [
		validators.Required(message="回复不能为空")])

# Email form
class EmailForm(Form):
	email = TextField('邮箱', [
		validators.Email(message="无效的邮箱"),
		validators.Required(message="邮箱不能为空")])

	user_id = HiddenField('用户ID', [
		validators.Required(message="用户ID不能为空")])