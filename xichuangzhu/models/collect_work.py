#-*- coding: UTF-8 -*-
from flask import g
from xichuangzhu import db

class CollectWork(db.Model):
    tags = db.Column(db.String(100))
    create_time = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    user = db.relationship('User', backref=db.backref('collect_works'))

    work_id = db.Column(db.Integer, db.ForeignKey('work.id'), primary_key=True)
    work = db.relationship('Work', backref=db.backref('collectors'))

    def __repr__(self):
        return '<%d collect %d>' % (self.user_id, self.work_id)