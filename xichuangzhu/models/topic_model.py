#-*- coding: UTF-8 -*-
import datetime
from flask import g
from xichuangzhu import db
from xichuangzhu.utils import time_diff

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

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    click_num = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('topics'))

    @property
    def friendly_create_time(self):
        return time_diff(self.create_time)

    @property
    def friendly_content(self):
        return self.content.replace('\n', "<div class='text-gap'></div>")

# GET

    # get a topic
    @staticmethod
    def get_topic(topic_id):
        query = '''SELECT topic.TopicID, topic.Title, topic.Content, topic.CommentNum, topic.Time, topic.ClickNum, node.Name AS NodeName, node.Abbr AS NodeAbbr, node.NodeID, user.Name AS UserName, user.Abbr AS UserAbbr, user.Avatar, user.UserID\n
            FROM topic, user, node\n
            WHERE topic.UserID = user.UserID\n
            AND topic.NodeID = node.NodeID\n
            AND topic.TopicID = %d''' % topic_id
        g.cursor.execute(query)
        return g.cursor.fetchone()

    # get topics
    @staticmethod
    def get_topics(page, per_page):
        query = '''SELECT topic.TopicID, topic.Title, topic.CommentNum, topic.Time, node.NodeID, node.Name AS NodeName, node.Abbr AS NodeAbbr, user.Name AS UserName, user.Abbr AS UserAbbr, user.Avatar\n
            FROM topic, user, node\n
            WHERE topic.UserID = user.UserID\n
            AND topic.NodeID = node.NodeID\n
            ORDER BY Time DESC LIMIT %d, %d''' % ((page-1)*per_page, per_page)
        g.cursor.execute(query)
        return g.cursor.fetchall()

    # get topics num
    @staticmethod
    def get_topics_num():
        query = "SELECT COUNT(*) AS topics_num FROM topic"
        g.cursor.execute(query)
        return g.cursor.fetchone()['topics_num']

    # get topics by user
    @staticmethod
    def get_topics_by_user(user_id, page, num):
        query = '''SELECT topic.TopicID, topic.Title, topic.CommentNum, topic.Time, node.NodeID, node.Name AS NodeName, node.Abbr AS NodeAbbr, user.Name AS UserName, user.Abbr AS UserAbbr, user.Avatar\n
            FROM topic, user, node\n
            WHERE topic.UserID = user.UserID\n
            AND topic.NodeID = node.NodeID\n
            AND topic.UserID = %d
            ORDER BY Time DESC LIMIT %d, %d''' % (user_id, (page-1)*num, num)
        g.cursor.execute(query)
        return g.cursor.fetchall()

    # get topics num by user
    @staticmethod
    def get_topics_num_by_user(user_id):
        query = "SELECT COUNT(*) AS TopicsNum FROM topic WHERE topic.UserID = %d" % user_id
        g.cursor.execute(query)
        return g.cursor.fetchone()['TopicsNum']

    # get hot topics
    @staticmethod
    def get_hot_topics(num):
        query = '''SELECT topic.TopicID, topic.Title, user.Abbr AS UserAbbr, user.Avatar\n
            FROM topic, user\n
            WHERE topic.UserID = user.UserID\n
            ORDER BY topic.CommentNum DESC LIMIT %d''' % num
        g.cursor.execute(query)
        return g.cursor.fetchall()

    # get topics by node
    @staticmethod
    def get_topics_by_node(node_abbr):
        query = '''SELECT topic.TopicID, topic.Title, topic.CommentNum, topic.Time, node.NodeID, node.Name AS NodeName, node.Abbr AS NodeAbbr, user.Name AS UserName, user.Abbr AS UserAbbr, user.Avatar\n
            FROM topic, user, node\n
            WHERE topic.UserID = user.UserID\n
            AND topic.NodeID = node.NodeID
            AND node.Abbr = '%s'\n
            ORDER BY Time DESC''' % node_abbr
        g.cursor.execute(query)
        return g.cursor.fetchall()

# NEW

    # add topic
    @staticmethod
    def add(node_id, title, content, user_id):
        query = "INSERT INTO topic (NodeID, Title, Content, UserID) VALUES (%d, '%s', '%s', %d)" % (node_id, title, content, user_id)
        g.cursor.execute(query)
        g.conn.commit()
        return g.cursor.lastrowid

# UPDATE

    # edit topic
    @staticmethod
    def edit(topic_id, node_id, title, content):
        query = "UPDATE topic SET NodeID = %d, Title = '%s', Content = '%s' WHERE TopicID = %d" % (node_id, title, content, topic_id)
        g.cursor.execute(query)
        return g.conn.commit()

    # add click num
    @staticmethod
    def add_click_num(topic_id):
        query = "UPDATE topic SET ClickNum = ClickNum + 1 WHERE TopicID = %d" % topic_id
        g.cursor.execute(query)
        return g.conn.commit()

    # add comment num
    @staticmethod
    def add_comment_num(topic_id):
        query = "UPDATE topic SET CommentNum = CommentNum + 1 WHERE TopicID = %d" % topic_id
        g.cursor.execute(query)
        return g.conn.commit()