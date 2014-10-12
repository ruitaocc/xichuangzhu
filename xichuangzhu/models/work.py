# coding: utf-8
import datetime
from flask import current_app
from ._base import db


class Work(db.Model):
    """作品"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    foreword = db.Column(db.Text())
    content = db.Column(db.Text())
    intro = db.Column(db.Text())
    layout = db.Column(db.String(10))
    highlight = db.Column(db.Boolean, default=False)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now)
    highlight_at = db.Column(db.Boolean)

    mobile_title = db.Column(db.String(50))
    mobile_content = db.Column(db.Text())

    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    author = db.relationship('Author', backref=db.backref('works', lazy='dynamic'))

    type_id = db.Column(db.Integer, db.ForeignKey('work_type.id'))
    type = db.relationship('WorkType', backref=db.backref('works', lazy='dynamic'))

    def __repr__(self):
        return '<Work %s>' % self.title


class WorkType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    en = db.Column(db.String(50))
    cn = db.Column(db.String(50))

    def __repr__(self):
        return '<WorkType %s>' % self.cn


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    desc = db.Column(db.String(200))
    icon = db.Column(db.String(200))


class WorkTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    work_id = db.Column(db.Integer, db.ForeignKey('work.id'), primary_key=True)
    work = db.relationship('Work', backref=db.backref('tags'))

    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), primary_key=True)
    tag = db.relationship('Tag', backref=db.backref('works'))

    def __repr__(self):
        return '<WorkTag %s>' % self.tag


class WorkImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200))
    is_original = db.Column(db.Boolean, default=False)
    from_url = db.Column(db.String(250))
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)

    work_id = db.Column(db.Integer, db.ForeignKey('work.id'))
    work = db.relationship('Work', backref=db.backref('images', lazy='dynamic'))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('work_images', lazy='dynamic',
                                                      order_by="desc(WorkImage.create_time)"))

    @property
    def url(self):
        return current_app.config['OSS_URL'] + self.filename

    def __repr__(self):
        return '<WorkImage %s>' % self.filename


class WorkReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    is_publish = db.Column(db.Boolean)
    click_num = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)

    work_id = db.Column(db.Integer, db.ForeignKey('work.id'))
    work = db.relationship('Work', backref=db.backref('reviews', lazy='dynamic',
                                                      order_by="desc(WorkReview.create_time)"))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('work_reviews', lazy='dynamic',
                                                      order_by="desc(WorkReview.create_time)"))

    def __repr__(self):
        return '<WorkReview %s>' % self.title


class WorkReviewComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)

    review_id = db.Column(db.Integer, db.ForeignKey('work_review.id'), primary_key=True)
    review = db.relationship('WorkReview',
                             backref=db.backref('comments', lazy='dynamic',
                                                order_by="desc(WorkReviewComment.create_time)"))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    user = db.relationship('User',
                           backref=db.backref('work_review_comments', lazy='dynamic',
                                              order_by="desc(WorkReviewComment.create_time)"))

    def __repr__(self):
        return '<WorkReviewComment %s>' % self.content