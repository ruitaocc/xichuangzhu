#-*- coding: UTF-8 -*-
import datetime
from xichuangzhu import db
from xichuangzhu.utils import time_diff

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    click_num = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('topics', lazy='dynamic'))

    def __repr__(self):
        return '<Topic %s>' % self.title

    @property
    def friendly_create_time(self):
        return time_diff(self.create_time)

    @property
    def friendly_content(self):
        return self.content.replace('\n', "<div class='text-gap'></div>")

class TopicComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), primary_key=True)
    topic = db.relationship('Topic', backref=db.backref('comments'))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    user = db.relationship('User', backref=db.backref('topic_comments'))

    @property
    def friendly_create_time(self):
        return time_diff(self.create_time)

    def __repr__(self):
        return '<TopicComment %s>' % self.content