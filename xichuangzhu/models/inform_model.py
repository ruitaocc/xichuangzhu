from flask import g

class Inform:

# GET

	# get all informs
	@staticmethod
	def get_informs(user_id):
		query = '''SELECT inform.Title, inform.Content, inform.Time, user.Avatar, user.Abbr
			FROM inform, user\n
			WHERE inform.ReplyerID = user.UserID\n
			AND inform.UserID = %d''' % user_id
		g.cursor.execute(query)
		return g.cursor.fetchall()

# NEW

	# add a inform
	@staticmethod
	def add(replyer_id, user_id, title, content):
		query = "INSERT INTO inform (ReplyerID, UserID, Title, Content) VALUES (%d, %d, '%s', '%s')" % (replyer_id, user_id, title, content)
		g.cursor.execute(query)
		return g.conn.commit()