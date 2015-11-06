# coding: utf-8
import datetime
from ._base import db


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    intro = db.Column(db.Text())
    baidu_wiki = db.Column(db.String(300))
    birth_year = db.Column(db.String(20))
    death_year = db.Column(db.String(20))
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now)

    dynasty_id = db.Column(db.Integer, db.ForeignKey('dynasty.id'))
    dynasty = db.relationship('Dynasty', backref=db.backref('authors', lazy='dynamic',
                                                            order_by="asc(Author.birth_year)"))

    def __repr__(self):
        return '<Author %s>' % self.name

    @property
    def random_quote(self):
        """Get a random quote of the author"""
        return self.quotes.order_by(db.func.random()).first()


class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote = db.Column(db.Text())
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now)

    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    author = db.relationship('Author', backref=db.backref('quotes', lazy='dynamic'))

    work_id = db.Column(db.Integer, db.ForeignKey('work.id'))
    work = db.relationship('Work', backref=db.backref('quotes', lazy='dynamic'))

    def __repr__(self):
        return '<Quote %s>' % self.quote