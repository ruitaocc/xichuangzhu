# coding: utf-8
import datetime
from ._base import db
from ..roles import NewUserRole


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    role = db.Column(db.Integer, default=NewUserRole)
    abbr = db.Column(db.String(50))
    email = db.Column(db.String(50))
    avatar = db.Column(db.String(200))
    signature = db.Column(db.Text)
    check_inform_time = db.Column(db.DateTime, default=datetime.datetime.now)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return '<User %s>' % self.name