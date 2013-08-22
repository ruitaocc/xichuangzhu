#-*- coding: UTF-8 -*-
import re
from flask import g
from xichuangzhu import db

# class WorkType(db.Model):
    

class Work(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    foreword = db.Column(db.Text())
    content = db.Column(db.Text())
    intro = db.Column(db.Text())
    type = db.Column(db.String(10))
    type_name = db.Column(db.String(10))
    create_time = db.Column(db.DateTime)

    @property
    def clean_content(self):
        c = re.sub(r'<([^<]+)>', '', self.content)
        c = c.replace('%', '')
        c = c.replace('（一）', "")
        c = c.replace('(一)', "")
        return c

    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    author = db.relationship('Author', backref=db.backref('works'))

    dynasty_id = db.Column(db.Integer, db.ForeignKey('dynasty.id'))
    dynasty = db.relationship('Dynasty', backref=db.backref('works'))

    def __repr__(self):
        return '<Work %s>' % self.title

# GET

    # get a single work
    @staticmethod
    def get_work(workID):
        query = '''SELECT work.WorkID, work.Title, work.Type, work.TypeName, work.Content, work.Foreword, work.Introduction AS WorkIntroduction, work.Type, author.AuthorID, author.Author, author.Abbr AS AuthorAbbr, author.Introduction AS AuthorIntroduction, dynasty.Dynasty, dynasty.Abbr AS DynastyAbbr\n
            FROM work, author, dynasty\n
            WHERE work.workID = %d\n
            AND work.AuthorID = author.AuthorID\n
            AND work.DynastyID = dynasty.DynastyID\n''' % workID
        g.cursor.execute(query)
        return g.cursor.fetchone()

    # get works by random
    @staticmethod
    def get_works_by_random(worksNum):
        query = '''SELECT work.WorkID, work.Title, work.Type, work.TypeName, work.Content, author.Author, author.Abbr AS AuthorAbbr\n
            FROM work, author\n
            WHERE work.AuthorID = author.AuthorID\n
            ORDER BY RAND()\n
            LIMIT %d''' % worksNum
        g.cursor.execute(query)
        return g.cursor.fetchall()

    # get works by random
    @staticmethod
    def get_work_by_random(work_type):
        query = '''SELECT work.WorkID, work.Title, work.Type, work.TypeName, work.Content, author.Author, author.Abbr AS AuthorAbbr\n
            FROM work, author\n
            WHERE work.AuthorID = author.AuthorID\n
            AND work.Type = '%s'\n
            ORDER BY RAND()\n
            LIMIT 1''' % work_type
        g.cursor.execute(query)
        return g.cursor.fetchone()

    # get works of certain type in certain dynasty
    @staticmethod
    def get_works(work_type, dynasty_abbr, page, num):
        query = '''SELECT work.WorkID, work.Title, work.Type, work.TypeName, work.Content, work.AuthorID, author.Author, author.Abbr AS AuthorAbbr\n
            FROM work, author, dynasty\n
            WHERE work.AuthorID = author.AuthorID
            AND work.DynastyID = dynasty.DynastyID\n'''

        if work_type != 'all':
            query += "AND work.Type = '%s'\n" % work_type
        if dynasty_abbr != 'all':
            query += "AND dynasty.Abbr = '%s'\n" % dynasty_abbr

        query += "LIMIT %d, %d" % ((page-1)*num, num)

        g.cursor.execute(query)
        return g.cursor.fetchall()

    # get works num of certain type in certain dynasty
    @staticmethod
    def get_works_num(work_type, dynasty_abbr):
        query = '''SELECT COUNT(*) AS WorksNum\n
            FROM work, dynasty\n
            WHERE work.DynastyID = dynasty.DynastyID\n'''

        if work_type != 'all':
            query += "AND work.Type = '%s'\n" % work_type
        if dynasty_abbr != 'all':
            query += "AND dynasty.Abbr = '%s'\n" % dynasty_abbr

        g.cursor.execute(query)
        return g.cursor.fetchone()['WorksNum']

    # get works by tag
    @staticmethod
    def get_works_by_tag(tag, page, num):
        query = '''SELECT work.WorkID, work.Title, work.Type, work.TypeName, work.Content, work.AuthorID, author.Author, author.Abbr AS AuthorAbbr\n
            FROM work, author, work_tag\n
            WHERE work.AuthorID = author.AuthorID\n
            AND work_tag.Tag = '%s'\n
            AND work_tag.WorkID = work.WorkID\n
            LIMIT %d, %d''' % (tag, (page-1)*num, num)

        g.cursor.execute(query)
        return g.cursor.fetchall()

    # get works num by tag
    @staticmethod
    def get_works_num_by_tag(tag):
        query = '''SELECT COUNT(*) AS WorksNum\n
            FROM work, work_tag\n
            WHERE work_tag.Tag = '%s'\n
            AND work_tag.WorkID = work.WorkID''' % tag
        g.cursor.execute(query)
        return g.cursor.fetchone()['WorksNum']

    # get an author's all works
    @staticmethod
    def get_works_by_author(authorID):
        query = "SELECT * FROM work WHERE AuthorID=%d" % authorID
        g.cursor.execute(query)
        return g.cursor.fetchall()

    # get an author's other works
    @staticmethod
    def get_other_works_by_author(author_id, work_id, num):
        query = '''SELECT * FROM work\n
            WHERE AuthorID = %d\n
            AND WorkID != %d\n
            ORDER BY RAND()\n
            LIMIT %d''' % (author_id, work_id, num)
        g.cursor.execute(query)
        return g.cursor.fetchall()      

    # get all work types
    @staticmethod
    def get_types():
        query = "SELECT * FROM work_type"
        g.cursor.execute(query)
        return g.cursor.fetchall()

    # get chinese name of a work type
    @staticmethod
    def get_type_name(work_type):
        query = "SELECT TypeName From work_type WHERE WorkType = '%s'" % work_type
        g.cursor.execute(query)
        return g.cursor.fetchone()['TypeName']

    # get a image
    @staticmethod
    def get_image(image_id):
        g.cursor.execute('SELECT work_image.id, work_image.url, work_image.filename, work_image.work_id, work_image.user_id, user.Name as user_name, user.Abbr as user_abbr FROM user, work_image WHERE work_image.id = %d AND user.UserID = work_image.user_id' % image_id)
        return g.cursor.fetchone()

    # get all images
    @staticmethod
    def get_images(page, per_page):
        query = "SELECT id, url FROM work_image ORDER BY create_time DESC LIMIT %d, %d" % ((page-1)*per_page, per_page)
        g.cursor.execute(query)
        return g.cursor.fetchall()

    # get num of all images
    @staticmethod
    def get_images_num():
        query = "SELECT COUNT(*) AS images_num FROM work_image"
        g.cursor.execute(query)
        return g.cursor.fetchone()['images_num']

    # get images by random
    @staticmethod
    def get_images_by_random(num):
        g.cursor.execute('SELECT work_image.url, work_image.id, work_image.work_id FROM user, work_image WHERE user.UserID = work_image.user_id ORDER BY RAND() LIMIT %d' % num) 
        return g.cursor.fetchall()

    # get images of a work
    @staticmethod
    def get_images_by_work(work_id, page, per_page):
        g.cursor.execute('SELECT work_image.url, work_image.id, work_image.work_id  FROM user, work_image WHERE work_image.work_id = %d AND user.UserID = work_image.user_id ORDER BY work_image.create_time DESC LIMIT %d, %d' % (work_id, (page-1)*per_page, per_page))
        return g.cursor.fetchall()

    # get images num of a work
    @staticmethod
    def get_images_num_by_work(work_id):
        g.cursor.execute('SELECT COUNT(*) AS images_num FROM work_image WHERE work_image.work_id = %d' % work_id)
        return g.cursor.fetchone()['images_num']

    # get images by user
    @staticmethod
    def get_images_by_user(user_id, page, per_page):
        g.cursor.execute('SELECT work_image.url, work_image.id, work_image.work_id FROM work_image WHERE work_image.user_id = %d ORDER BY work_image.create_time DESC LIMIT %d, %d' % (user_id, (page-1)*per_page, per_page))
        return g.cursor.fetchall()     

    # get images num by user
    @staticmethod
    def get_images_num_by_user(user_id):
        g.cursor.execute('SELECT COUNT(*) AS work_images_num FROM work_image WHERE work_image.user_id = %d' % user_id)
        return g.cursor.fetchone()['work_images_num']

# NEW

    # add a work
    @staticmethod
    def add_work(title, content, foreword, introduction, authorID, dynastyID, work_type, type_name):
        query = "INSERT INTO work (Title, Content, Foreword, Introduction, AuthorID, DynastyID, Type, TypeName) VALUES ('%s', '%s', '%s','%s', %d, %d, '%s', '%s')" % (title, content, foreword, introduction, authorID, dynastyID, work_type, type_name)
        g.cursor.execute(query)
        g.conn.commit()
        return g.cursor.lastrowid

    @staticmethod
    def add_image(work_id, user_id, image_url, filename):
        query = "INSERT INTO work_image (work_id, user_id, url, filename) VALUES (%d, %d, '%s', '%s')" % (work_id, user_id, image_url, filename)
        g.cursor.execute(query)
        g.conn.commit()
        return g.cursor.lastrowid

# UPDATE

    # Update a work
    @staticmethod
    def edit_work(title, content, foreword, introduction, authorID, dynastyID, work_type, type_name, work_id):
        query = '''UPDATE work SET Title = '%s', Content = '%s', Foreword = '%s', Introduction = '%s', AuthorID = %d, DynastyID = %d, Type = '%s', TypeName = '%s' WHERE WorkID=%d''' % (title, content, foreword, introduction, authorID, dynastyID, work_type, type_name, work_id)
        g.cursor.execute(query)
        return g.conn.commit()

    # Update work image info
    @staticmethod
    def update_image(image_id, url, filename):
        query = "UPDATE work_image SET url = '%s', filename = '%s' WHERE id = %d" % (url, filename, image_id)
        g.cursor.execute(query)
        return g.conn.commit()

# DELETE

    # delete a work
    @staticmethod
    def delete_work(workID):
        query = "DELETE FROM work WHERE WorkID = %d" % workID
        g.cursor.execute(query)
        return g.conn.commit()

    # delete work image
    @staticmethod
    def delete_image(image_id):
        query = "DELETE FROM work_image WHERE id = %d" % image_id
        g.cursor.execute(query)
        return g.conn.commit()