# coding: utf-8
from ._base import db


class Dynasty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    intro = db.Column(db.Text())
    start_year = db.Column(db.Integer)
    end_year = db.Column(db.Integer)

    # 繁体
    name_tr = db.Column(db.String(50))
    intro_tr = db.Column(db.Text())

    def __repr__(self):
        return '<Dynasty %s>' % self.name