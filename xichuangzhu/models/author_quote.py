#-*- coding: UTF-8 -*-
from xichuangzhu import db
from flask import g

class AuthorQuote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote = db.Column(db.Text())

    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    author = db.relationship('Author', backref=db.backref('quotes'))

    work_id = db.Column(db.Integer, db.ForeignKey('work.id'))
    work = db.relationship('Work', backref=db.backref('quotes'))