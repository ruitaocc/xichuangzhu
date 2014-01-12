# coding: utf-8
from ._base import db


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    abbr = db.Column(db.String(50), unique=True)
    intro = db.Column(db.Text())
    birth_year = db.Column(db.String(20))
    death_year = db.Column(db.String(20), default=None)

    dynasty_id = db.Column(db.Integer, db.ForeignKey('dynasty.id'))
    dynasty = db.relationship('Dynasty', backref=db.backref('authors', lazy='dynamic'))

    def __repr__(self):
        return '<Author %s>' % self.name

    @property
    def random_quote(self):
        """Get a random quote of the author
        为了防止每次访问此属性时都得到不同的结果，
        在第一次查询后将结果缓存起来，以便后续使用
        """
        if not hasattr(self, '_random_quote'):
            self._random_quote = AuthorQuote.query.filter(AuthorQuote.author_id == self.id).order_by(db.func.rand()).first()
        return self._random_quote


class AuthorQuote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote = db.Column(db.Text())

    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    author = db.relationship('Author', backref=db.backref('quotes'))

    work_id = db.Column(db.Integer, db.ForeignKey('work.id'))
    work = db.relationship('Work', backref=db.backref('quotes'))

    def __repr__(self):
        return '<AuthorQuote %s>' % self.quote