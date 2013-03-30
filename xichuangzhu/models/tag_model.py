from flask import g

class Tag:

# GET

	# get tags of a user
	@staticmethod
	def get_user_tags(user_id, num):
		query = "SELECT Tag FROM user_tag WHERE UserID = %d ORDER BY Num DESC LIMIT %d" % (user_id, num)
		g.cursor.execute(query)
		return g.cursor.fetchall()

	# get tags of a work
	@staticmethod
	def get_work_tags(work_id, num):
		query = "SELECT Tag FROM work_tag WHERE WorkID = %d ORDER BY Num DESC LIMIT %d" % (work_id, num)
		g.cursor.execute(query)
		return g.cursor.fetchall()

# NEW
	
	# add tag in user tags
	@staticmethod
	def add_user_tag(user_id, tag):
	 	g.cursor.execute("SELECT * FROM user_tag WHERE UserID=%d AND Tag = '%s'" % (user_id, tag))

		if g.cursor.rowcount == 0:
			query = "INSERT INTO user_tag (UserID, Tag) VALUES (%d, '%s')" % (user_id, tag)
			g.cursor.execute(query)
			g.conn.commit()
		else:
			query = "UPDATE user_tag SET Num = Num + 1 WHERE UserID = %d AND Tag = '%s'" % (user_id, tag)
			g.cursor.execute(query)
			g.conn.commit()
	
	# add tag in work tags
	@staticmethod
	def add_work_tag(work_id, tag):
	 	g.cursor.execute("SELECT * FROM work_tag WHERE WorkID=%d AND Tag = '%s'" % (work_id, tag))

		if g.cursor.rowcount == 0:
			query = "INSERT INTO work_tag (WorkID, Tag) VALUES (%d, '%s')" % (work_id, tag)
			g.cursor.execute(query)
			g.conn.commit()
		else:
			query = "UPDATE work_tag SET Num = Num + 1 WHERE WorkID = %d AND Tag = '%s'" % (work_id, tag)
			g.cursor.execute(query)
			g.conn.commit()
