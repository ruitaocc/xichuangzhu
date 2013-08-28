#-*- coding: UTF-8 -*-
import re
import datetime
import markdown2
from xichuangzhu import db
from xichuangzhu.utils import time_diff

class Work(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    foreword = db.Column(db.Text())
    content = db.Column(db.Text())
    intro = db.Column(db.Text())
    create_time = db.Column(db.DateTime)

    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    author = db.relationship('Author', backref=db.backref('works'))

    type_id = db.Column(db.Integer, db.ForeignKey('work_type.id'))
    type = db.relationship('WorkType', backref=db.backref('works'))

    def __repr__(self):
        return '<Work %s>' % self.title

    @property
    def clean_content(self):
        c = re.sub(r'<([^<]+)>', '', self.content)
        c = c.replace('%', '')
        c = c.replace('（一）', "")
        c = c.replace('(一)', "")
        return c

    @property
    def friendly_content(self):
        """
        Add comment -> Split ci -> Generate paragraph
        """
        c = re.sub(r'<([^<^b]+)>', r"<sup title='\1'></sup>", self.content)
        c = c.replace('%', "&nbsp;&nbsp;")
        c = markdown2.markdown(c)
        return c

class WorkType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    en = db.Column(db.String(50))
    cn = db.Column(db.String(50))

    def __repr__(self):
        return '<WorkType %s>' % self.cn

class WorkTag(db.Model):
    tag = db.Column(db.String(50), primary_key=True)

    work_id = db.Column(db.Integer, db.ForeignKey('work.id'), primary_key=True)
    work = db.relationship('Work', backref=db.backref('tags'))

    def __repr__(self):
        return '<WorkTag %s>' % self.tag

class WorkReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    is_publish = db.Column(db.Boolean)
    click_num = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)

    work_id = db.Column(db.Integer, db.ForeignKey('work.id'))
    work = db.relationship('Work', backref=db.backref('reviews', lazy='dynamic'))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('reviews', lazy='dynamic'))

    @property
    def friendly_create_time(self):
        return time_diff(self.create_time)

    @property
    def friendly_content(self):
        return self.content.replace('\n', "<div class='text-gap'></div>")

    def __repr__(self):
        return '<WorkReview %s>' % self.title

class WorkReviewComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    
    review_id = db.Column(db.Integer, db.ForeignKey('work_review.id'), primary_key=True)
    review = db.relationship('WorkReview', backref=db.backref('comments'))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    user = db.relationship('User', backref=db.backref('work_review_comments'))

    @property
    def friendly_create_time(self):
        return time_diff(self.create_time)

    def __repr__(self):
        return '<WorkReviewComment %s>' % self.content