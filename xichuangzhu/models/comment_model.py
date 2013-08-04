#-*- coding: UTF-8 -*-
from flask import g

class Comment:

# GET 

    # get all comments of a review
    @staticmethod
    def get_comments_by_review(review_id):
        query = '''SELECT c.CommentID, c.Comment, c.Time, user.Name, user.Abbr, user.Avatar\n
            FROM review_comment AS c, user\n
            WHERE c.ReplyerID = user.UserID\n
            AND c.ReviewID = %d\n
            ORDER BY c.Time ASC''' % review_id
        g.cursor.execute(query)
        return g.cursor.fetchall()

    # get all comments of a topic
    @staticmethod
    def get_comments_by_topic(topic_id):
        query = '''SELECT c.CommentID, c.Comment, c.Time, user.Name, user.Abbr, user.Avatar\n
            FROM topic_comment AS c, user\n
            WHERE c.ReplyerID = user.UserID\n
            AND c.TopicID = %d\n
            ORDER BY c.Time ASC''' % topic_id
        g.cursor.execute(query)
        return g.cursor.fetchall()

# NEW

    # add comment to a review
    @staticmethod
    def add_comment_to_review(review_id, replyer_id, comment):
        query = "INSERT INTO review_comment (ReviewID, ReplyerID, Comment) VALUES (%d, '%s', '%s')" % (review_id, replyer_id, comment)
        g.cursor.execute(query)
        g.conn.commit()
        return g.cursor.lastrowid

    # add comment to a topic
    @staticmethod
    def add_comment_to_topic(topic_id, replyer_id, comment):
        query = "INSERT INTO topic_comment (TopicID, ReplyerID, Comment) VALUES (%d, '%s', '%s')" % (topic_id, replyer_id, comment)
        g.cursor.execute(query)
        g.conn.commit()
        return g.cursor.lastrowid