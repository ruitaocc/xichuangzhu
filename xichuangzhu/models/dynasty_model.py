#-*- coding: UTF-8 -*-
from flask import g

class Dynasty:

# GET

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