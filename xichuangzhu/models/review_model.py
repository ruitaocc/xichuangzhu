#-*- coding: UTF-8 -*-
import datetime
from flask import g
from xichuangzhu import db
from xichuangzhu.utils import time_diff

class WorkReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    is_publish = db.Column(db.Boolean)
    click_num = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)

    work_id = db.Column(db.Integer, db.ForeignKey('work.id'))
    work = db.relationship('Work', backref=db.backref('reviews'))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('reviews'))

    @property
    def friendly_create_time(self):
        return time_diff(self.create_time)

    @property
    def friendly_content(self):
        return self.content.replace('\n', "<div class='text-gap'></div>")

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

class Review:

# GET

    # get a review
    @staticmethod
    def get_review(review_id):
        query = '''SELECT review.ReviewID, review.Title, review.IsPublish, review.Content, review.Time, review.ClickNum, review.IsPublish, user.UserID, user.Abbr AS UserAbbr, user.Name, user.Avatar, work.WorkID, work.Title AS WorkTitle, work.Content AS WorkContent, author.Author\n
            FROM review, user, work, author\n
            WHERE review.ReviewID = %d\n
            AND review.UserID = user.UserID\n
            AND review.WorkID = work.WorkID\n
            AND work.AuthorID = author.AuthorID''' % review_id
        g.cursor.execute(query)
        return g.cursor.fetchone()

    # get reviews by random
    @staticmethod
    def get_reviews_by_random(reviews_num):
        query = '''SELECT review.ReviewID, review.Title, review.Content, review.Time, user.UserID, user.Abbr AS UserAbbr, user.Name, user.Avatar, work.WorkID, work.Title AS WorkTitle, work.Content AS WorkContent, author.Author\n
            FROM review, user, work, author\n
            WHERE review.UserID = user.UserID\n
            AND review.WorkID = work.WorkID\n
            AND work.AuthorID = author.AuthorID\n
            AND review.IsPublish = 1\n
            LIMIT %d''' % reviews_num
        g.cursor.execute(query)
        return g.cursor.fetchall()

    # get hot reviews
    @staticmethod
    def get_reviews(page, num):
        query = '''SELECT review.ReviewID, review.Title, review.Content, review.Time, user.UserID, user.Abbr AS UserAbbr, user.Name, user.Avatar, work.WorkID, work.Title AS WorkTitle, work.Content AS WorkContent, author.Author\n
            FROM review, user, work, author\n
            WHERE review.UserID = user.UserID\n
            AND review.WorkID = work.WorkID\n
            AND work.AuthorID = author.AuthorID\n
            AND review.IsPublish = 1\n
            LIMIT %d, %d''' % ((page-1)*num, num)
        g.cursor.execute(query)
        return g.cursor.fetchall()

    # get hot reviews total num
    @staticmethod
    def get_reviews_num():
        query = "SELECT COUNT(*) AS ReviewsNum FROM review WHERE review.IsPublish = 1"
        g.cursor.execute(query)
        return g.cursor.fetchone()['ReviewsNum']

    # get reviews of a work
    @staticmethod
    def get_reviews_by_work(work_id, page, per_page):
        query = '''SELECT review.ReviewID, review.Title, review.Content, review.Time, user.UserID, user.Abbr AS UserAbbr, user.Name, user.Avatar, work.WorkID, work.Title AS WorkTitle, work.Content AS WorkContent, author.Author\n
            FROM review, user, work, author\n
            WHERE review.WorkID = %d\n
            AND review.UserID = user.UserID\n
            AND review.WorkID = work.WorkID\n
            AND work.AuthorID = author.AuthorID\n
            AND review.IsPublish = 1\n
            LIMIT %d, %d''' % (work_id, (page-1)*per_page, per_page)
        g.cursor.execute(query)
        return g.cursor.fetchall()

    # get reviews num of a work
    @staticmethod
    def get_reviews_num_by_work(work_id):
        query = "SELECT COUNT(*) AS reviews_num FROM review WHERE review.WorkID = %d" % work_id
        g.cursor.execute(query)
        return g.cursor.fetchone()['reviews_num']

    # get reviews from a user
    @staticmethod
    def get_reviews_by_user(user_id, page, num, is_me):
        query = '''SELECT review.ReviewID, review.Title, review.Content, review.Time, review.IsPublish, user.UserID, user.Abbr AS UserAbbr, user.Name, user.Avatar, work.WorkID, work.Title AS WorkTitle, work.Content AS WorkContent, author.Author\n
            FROM review, user, work, author\n
            WHERE review.UserID = %d\n
            AND review.UserID = user.UserID\n
            AND review.WorkID = work.WorkID\n
            AND work.AuthorID = author.AuthorID\n''' % user_id

        if not is_me:
            query += "AND review.IsPublish = 1\n"

        query += "ORDER BY review.Time LIMIT %d, %d" % ((page-1)*num, num)

        g.cursor.execute(query)
        return g.cursor.fetchall()

    # get reviews num from a user
    @staticmethod
    def get_reviews_num_by_user(user_id, is_me):
        query = '''SELECT COUNT(*) AS ReviewsNum\n
            FROM review\n
            WHERE review.UserID = %d\n''' % user_id

        if not is_me:
            query += "AND review.IsPublish = 1"

        g.cursor.execute(query)
        return g.cursor.fetchone()['ReviewsNum']

    # get hot reviewers
    @staticmethod
    def get_hot_reviewers(num):
        query = '''SELECT review.UserID, user.Avatar, user.Name, user.Abbr, user.Signature, COUNT(*) AS ReviewNum\n
            FROM review, user\n
            WHERE review.UserID = user.UserID
            AND review.IsPublish = 1\n
            GROUP BY review.UserID\n
            ORDER BY ReviewNum DESC\n
            LIMIT %d''' % num
        g.cursor.execute(query)
        return g.cursor.fetchall()
# NEW

    # add a review to a work
    @staticmethod
    def add_review(work_id, user_id, title, content, is_publish):
        query = "INSERT INTO review (WorkID, UserID, Title, Content, IsPublish) VALUES (%d, %d, '%s', '%s', %d)" % (work_id, user_id, title, content, is_publish)
        g.cursor.execute(query)
        g.conn.commit()
        return g.cursor.lastrowid

# UPDATE

    # edit a review
    @staticmethod
    def edit_review(review_id, title, content, is_publish):
        query = "UPDATE review SET Title = '%s', Content = '%s', IsPublish = %d WHERE ReviewID = %d" % (title, content, is_publish, review_id)
        g.cursor.execute(query)
        return g.conn.commit()

    # add click num
    @staticmethod
    def add_click_num(review_id):
        query = "UPDATE review SET ClickNum = ClickNum + 1 WHERE ReviewID = %d" % review_id
        g.cursor.execute(query)
        return g.conn.commit()

    # add comment num
    @staticmethod
    def add_comment_num(review_id):
        query = "UPDATE review SET CommentNum = CommentNum + 1 WHERE ReviewID = %d" % review_id
        g.cursor.execute(query)
        return g.conn.commit()

# DELETE
    
    # delete a review
    @staticmethod
    def delete(review_id):
        g.cursor.execute("DELETE FROM review WHERE ReviewID = %d" % review_id)
        return g.conn.commit()