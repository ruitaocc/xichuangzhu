#-*- coding: UTF-8 -*-

from flask import g

class Inform:

# GET

	# get all informs
	@staticmethod
	def get_informs(user_id, page, num):
		query = '''SELECT inform.Title, inform.Content, inform.Time, user.Avatar, user.Abbr
			FROM inform, user\n
			WHERE inform.ReplyerID = user.UserID\n
			AND inform.UserID = %d\n
			ORDER BY inform.Time DESC\n
			LIMIT %d, %d''' % (user_id, (page-1)*num, num)
		g.cursor.execute(query)
		return g.cursor.fetchall()

	# get informs num
	@staticmethod
	def get_informs_num(user_id):
		query = '''SELECT COUNT(*) AS InformsNum FROM inform WHERE inform.UserID = %d''' % user_id
		g.cursor.execute(query)
		return g.cursor.fetchone()['InformsNum']

	# get new informs num
	@staticmethod
	def get_new_informs_num(user_id):
		query = '''SELECT COUNT(*) AS InformsNum
			FROM inform, user\n
			WHERE inform.UserID = user.UserID\n
			AND inform.UserID = %d\n
			AND inform.Time >= user.CheckInformTime''' % user_id
		g.cursor.execute(query)
		return g.cursor.fetchone()['InformsNum']

# NEW

	# add a inform
	@staticmethod
	def add(replyer_id, user_id, title, content):
		query = "INSERT INTO inform (ReplyerID, UserID, Title, Content) VALUES (%d, %d, '%s', '%s')" % (replyer_id, user_id, title, content)
		g.cursor.execute(query)
		return g.conn.commit()

# UPDATE

	# update user's check inform time
	@staticmethod
	def update_check_inform_time(user_id):
		query = "UPDATE user SET CheckInformTime = NOW() WHERE UserID = %d" % user_id
		g.cursor.execute(query)
		return g.conn.commit()