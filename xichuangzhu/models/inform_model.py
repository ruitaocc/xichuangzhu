from flask import g

class Inform:

# GET

	# get all informs
	@staticmethod
	def get_informs(num):
		pass

# NEW

	# add a inform
	@staticmethod
	def add(replyer_id, user_id, title, content):
		query = "INSERT INTO inform (ReplyerID, UserID, Title, Content) VALUES (%d, %d, '%s', '%s')" % (replyer_id, user_id, title, content)
		g.cursor.execute(query)
		return g.conn.commit()