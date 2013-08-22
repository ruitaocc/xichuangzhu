#-*- coding: UTF-8 -*-
import datetime
from flask import g
from xichuangzhu import db

class WorkImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200))
    filename = db.Column(db.String(200))
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)

    work_id = db.Column(db.Integer, db.ForeignKey('work.id'))
    work = db.relationship('Work', backref=db.backref('images'))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('work_images'))

    def __repr__(self):
        return '<WorkImage %s>' % self.filename
