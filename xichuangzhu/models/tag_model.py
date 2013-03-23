from xichuangzhu import conn, cursor

class Tag:

# GET

	# get tags of a user
	@staticmethod
	def get_user_tags(user_id, num):
		query = "SELECT Tag FROM user_tag WHERE UserID = %d ORDER BY Num DESC LIMIT %d" % (user_id, num)
		cursor.execute(query)
		return cursor.fetchall()

	# get tags of a work
	@staticmethod
	def get_work_tags(work_id, num):
		query = "SELECT Tag FROM work_tag WHERE WorkID = %d ORDER BY Num DESC LIMIT %d" % (work_id, num)
		cursor.execute(query)
		return cursor.fetchall()