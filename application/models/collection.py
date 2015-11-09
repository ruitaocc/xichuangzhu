# coding: utf-8
from datetime import datetime
from ._base import db


class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.Integer, default=0)
    name = db.Column(db.String(200), unique=True)
    desc = db.Column(db.Text())
    cover = db.Column(db.String(200))
    link = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.now)

    kind_id = db.Column(db.Integer, db.ForeignKey('collection_kind.id'), primary_key=True)
    kind = db.relationship('CollectionKind', backref=db.backref('collections'))

    def __repr__(self):
        return '<Collection %s>' % self.name


class CollectionKind(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.Integer, default=0)
    name = db.Column(db.String(50), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now)


class CollectionWork(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)

    work_id = db.Column(db.Integer, db.ForeignKey('work.id'), primary_key=True)
    work = db.relationship('Work', backref=db.backref('collections'))

    collection_id = db.Column(db.Integer, db.ForeignKey('collection.id'), primary_key=True)
    collection = db.relationship('Collection', backref=db.backref('works'))
