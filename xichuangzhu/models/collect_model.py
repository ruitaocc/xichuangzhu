#-*- coding: UTF-8 -*-
from flask import g

class Collect:

# GET

    # get all works collected by user
    @staticmethod
    def get_works_by_user(user_id, page, num):
        query = '''SELECT work.WorkID, work.Title, work.Content, author.Author, author.Abbr AS AuthorAbbr\n
            FROM collect_work, user, work, author\n
            WHERE collect_work.UserID = %d\n
            AND collect_work.UserID = user.UserID\n
            AND collect_work.WorkID = work.WorkID\n
            AND work.AuthorID = author.AuthorID\n
            ORDER BY collect_work.Time DESC\n
            LIMIT %d, %d''' % (user_id, (page-1)*num, num)
        g.cursor.execute(query)
        return g.cursor.fetchall()

    # get works num collected by user
    @staticmethod
    def get_works_num_by_user(user_id):
        query = "SELECT COUNT(*) AS WorksNum FROM collect_work WHERE UserID = %d" % user_id
        g.cursor.execute(query)
        return g.cursor.fetchone()['WorksNum']

    # get all users who collect the work
    @staticmethod
    def get_users_by_work(work_id, num):
        query = '''SELECT user.UserID, user.Name, user.Signature, user.Abbr, user.Avatar, COUNT(*) AS ReviewNum\n
            FROM collect_work, user, review\n
            WHERE collect_work.WorkID = %d\n
            AND collect_work.UserID = user.UserID\n
            GROUP BY user.UserID
            LIMIT %d''' % (work_id, num)
        g.cursor.execute(query)
        return g.cursor.fetchall()

    # get tags
    @staticmethod
    def get_tags(user_id, work_id):
        query = "SELECT Tags FROM collect_work WHERE UserID = %d AND WorkID = %d" % (user_id, work_id)
        g.cursor.execute(query)
        return g.cursor.fetchone()['Tags']

# CHECK 

    # check if user collected this work
    @staticmethod
    def check(user_id, work_id):
        query = "SELECT * FROM collect_work WHERE UserID = %d AND WorkID = %d" % (user_id, work_id)
        g.cursor.execute(query)
        return g.cursor.rowcount > 0

# NEW
    
    # collect a work
    @staticmethod
    def add(user_id, work_id, tags):
        query = "INSERT INTO collect_work (UserID, WorkID, Tags) VALUES (%d, %d, '%s')" % (user_id, work_id, tags)
        g.cursor.execute(query)
        return g.conn.commit()

# UPDATE

    # edit work tags
    @staticmethod
    def edit(user_id, work_id, tags):
        query = "UPDATE collect_work SET Tags = '%s' WHERE UserID = %d AND WorkID = %d" % (tags, user_id, work_id)
        g.cursor.execute(query)
        return g.conn.commit()

# DELETE

    # discollect a work
    @staticmethod
    def remove(user_id, work_id):
        query = "DELETE FROM collect_work WHERE UserID = %d AND WorkID = %d" % (user_id, work_id)
        g.cursor.execute(query)
        return g.conn.commit()