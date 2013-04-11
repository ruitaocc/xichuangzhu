#-*- coding: UTF-8 -*-

from flask import g

class Love_work:

# GET

	# get all works loved by user
	@staticmethod
	def get_works_by_user(user_id, page, num):
		query = '''SELECT work.WorkID, work.Title, work.Content, author.Author, author.Abbr AS AuthorAbbr\n
			FROM love_work, user, work, author\n
			WHERE love_work.UserID = %d\n
			AND love_work.UserID = user.UserID\n
			AND love_work.WorkID = work.WorkID\n
			AND work.AuthorID = author.AuthorID\n
			ORDER BY love_work.Time DESC\n
			LIMIT %d, %d''' % (user_id, (page-1)*num, num)
		g.cursor.execute(query)
		return g.cursor.fetchall()

	# get works num loved by user
	@staticmethod
	def get_works_num_by_user(user_id):
		query = "SELECT COUNT(*) AS WorksNum FROM love_work WHERE UserID = %d" % user_id
		g.cursor.execute(query)
		return g.cursor.fetchone()['WorksNum']

	# get all users who love a work
	@staticmethod
	def get_users_by_work(work_id, num):
		query = '''SELECT user.UserID, user.Name, user.Signature, user.Abbr, user.Avatar, COUNT(*) AS ReviewNum\n
			FROM love_work, user, review\n
			WHERE love_work.WorkID = %d\n
			AND love_work.UserID = user.UserID\n
			GROUP BY user.UserID
			LIMIT %d''' % (work_id, num)
		g.cursor.execute(query)
		return g.cursor.fetchall()

	# get tags
	@staticmethod
	def get_tags(user_id, work_id):
		query = "SELECT Tags FROM love_work WHERE UserID = %d AND WorkID = %d" % (user_id, work_id)
		g.cursor.execute(query)
		return g.cursor.fetchone()['Tags']

# CHECK 

	# check if user loves work
	@staticmethod
	def check_love(user_id, work_id):
		query = "SELECT * FROM love_work WHERE UserID = %d AND WorkID = %d" % (user_id, work_id)
		g.cursor.execute(query)
		return g.cursor.rowcount > 0

# NEW
	
	# a user love a work
	@staticmethod
	def add(user_id, work_id, tags):
		query = "INSERT INTO love_work (UserID, WorkID, Tags) VALUES (%d, %d, '%s')" % (user_id, work_id, tags)
		g.cursor.execute(query)
		return g.conn.commit()

# UPDATE

	# edit work tags
	@staticmethod
	def edit(user_id, work_id, tags):
		query = "UPDATE love_work SET Tags = '%s' WHERE UserID = %d AND WorkID = %d" % (tags, user_id, work_id)
		g.cursor.execute(query)
		return g.conn.commit()

# DELETE

	# a user dislove a work
	@staticmethod
	def remove(user_id, work_id):
		query = "DELETE FROM love_work WHERE UserID = %d AND WorkID = %d" % (user_id, work_id)
		g.cursor.execute(query)
		return g.conn.commit()