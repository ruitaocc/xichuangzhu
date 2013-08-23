#-*- coding: UTF-8 -*-
from flask import g
from xichuangzhu import db

class Dynasty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    abbr = db.Column(db.String(50), unique=True)
    intro = db.Column(db.Text())
    start_year = db.Column(db.Integer)
    end_year = db.Column(db.Integer)

    def __repr__(self):
        return '<Dynasty %s>' % self.name

    @property
    def friendly_start_year(self):
        return "%s年" % str(self.start_year).replace('-', '前')

    @property
    def friendly_end_year(self):
        if self.end_year == 2012:
            return "至今"
        else:
            return "%s年" % str(self.end_year).replace('-', '前') 