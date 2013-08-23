#-*- coding: UTF-8 -*-
from flask import g
from xichuangzhu import db
from sqlalchemy import func

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    abbr = db.Column(db.String(50), unique=True)
    intro = db.Column(db.Text())
    birth_year = db.Column(db.String(20))
    death_year = db.Column(db.String(20))

    dynasty_id = db.Column(db.Integer, db.ForeignKey('dynasty.id'))
    dynasty = db.relationship('Dynasty', backref=db.backref('authors', lazy='dynamic'))

    def __repr__(self):
        return '<Author %s>' % self.name

    @property
    def random_quote(self):
        """
        Get a random quote of the author
        """
        return AuthorQuote.query.filter(AuthorQuote.author_id == self.id).order_by(func.rand()).first()

class AuthorQuote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote = db.Column(db.Text())

    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    author = db.relationship('Author', backref=db.backref('quotes'))

    work_id = db.Column(db.Integer, db.ForeignKey('work.id'))
    work = db.relationship('Work', backref=db.backref('quotes'))

    def __repr__(self):
        return '<AuthorQuote %s>' % self.quote