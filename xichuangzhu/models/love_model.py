from xichuangzhu import conn, cursor

class Love:

# GET

	# get all works loved by user
	@staticmethod
	def get_works_by_user_love(user_id, num):
		query = '''SELECT work.WorkID, work.Title, work.Content, author.Author, author.Abbr AS AuthorAbbr\n
			FROM love, user, work, author\n
			WHERE love.UserID = %d\n
			AND love.UserID = user.UserID\n
			AND love.WorkID = work.WorkID\n
			AND work.AuthorID = author.AuthorID\n
			ORDER BY love.Time DESC LIMIT %d''' % (user_id, num)
		cursor.execute(query)
		return cursor.fetchall()

	# get all users who love a work
	@staticmethod
	def get_users_love_work(work_id, num):
		query = '''SELECT user.UserID, user.Name, user.Signature, user.Abbr, user.Avatar, COUNT(*) AS ReviewNum\n
			FROM love, user, review\n
			WHERE love.WorkID = %d\n
			AND love.UserID = user.UserID\n
			GROUP BY user.UserID
			LIMIT %d''' % (work_id, num)
		cursor.execute(query)
		return cursor.fetchall()

# CHECK 

	# check if user loves work
	@staticmethod
	def check_love(user_id, work_id):
		query = "SELECT * FROM love WHERE UserID = %d AND WorkID = %d" % (user_id, work_id)
		cursor.execute(query)
		return cursor.rowcount > 0

# NEW
	
	# a user love a work
	@staticmethod
	def add_love(user_id, work_id):
		query = "INSERT INTO love (UserID, WorkID) VALUES (%d, %d)" % (user_id, work_id)
		cursor.execute(query)
		return conn.commit()

# DELETE

	# a user dislove a work
	@staticmethod
	def remove_love(user_id, work_id):
		query = "DELETE FROM love WHERE UserID = %d AND WorkID = %d" % (user_id, work_id)
		cursor.execute(query)
		return conn.commit()


