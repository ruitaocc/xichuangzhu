# coding: utf-8
from flask_wtf import Form
from wtforms import TextField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileField, FileAllowed, FileRequired