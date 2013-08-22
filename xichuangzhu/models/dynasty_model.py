#-*- coding: UTF-8 -*-
from flask import g
from xichuangzhu import db

class Dynasty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    abbr = db.Column(db.String(50), unique=True)
    intro = db.Column(db.Text())
    start_year = db.Column(db.Integer)
    end_year = db.Column(db.Integer)

    def __repr__(self):
        return '<Dynasty %s>' % self.name

    @property
    def friendly_start_year(self):
        return "%s年" % str(self.start_year).replace('-', '前')

    @property
    def friendly_end_year(self):
        if self.end_year == 2012:
            return "至今"
        else:
            return "%s年" % str(self.end_year).replace('-', '前') 

    # get all dynasties
    @staticmethod
    def get_dynasties():
        query = "SELECT * FROM dynasty ORDER BY StartYear ASC";
        g.cursor.execute(query)
        return g.cursor.fetchall()

    # get a dyansty by id
    @staticmethod
    def get_dynasty(dynastyID):
        query = "SELECT * FROM dynasty WHERE DynastyID = %d" % dynastyID
        g.cursor.execute(query)
        return g.cursor.fetchone()

    # get a dynasty by abbr
    @staticmethod
    def get_dynasty_by_abbr(dynasty_abbr):
        query = "SELECT * FROM dynasty WHERE Abbr = '%s'" % dynasty_abbr
        g.cursor.execute(query)
        return g.cursor.fetchone()

    # get dynastyID by author
    @staticmethod
    def get_dynastyID_by_author(authorID):
        query = "SELECT DynastyID FROM author WHERE AuthorID = %d" % authorID
        g.cursor.execute(query)
        return g.cursor.fetchone()['DynastyID']

# NEW

    # add a new dynasty
    @staticmethod
    def add_dynasty(dynasty, abbr, intro, startYear, endYear):
        query = '''INSERT INTO dynasty (Dynasty, Abbr, Introduction, StartYear, EndYear) VALUES
            ('%s', '%s', '%s', %d, %d)''' % (dynasty, abbr, intro, startYear, endYear)
        g.cursor.execute(query)
        g.conn.commit()
        return g.cursor.lastrowid

# EDIT

    # edit a dynasty
    @staticmethod
    def edit_dynasty(dynasty, abbr, intro, history, startYear, endYear, dynastyID):
        query = '''UPDATE dynasty SET Dynasty='%s', Abbr='%s', Introduction='%s', History='%s', StartYear=%d, EndYear=%d\n
            WHERE DynastyID = %d''' % (dynasty, abbr, intro, history, startYear, endYear, dynastyID)
        g.cursor.execute(query)
        return g.conn.commit()