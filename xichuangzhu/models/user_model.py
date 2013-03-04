from xichuangzhu import conn, cursor

class User:

# GET

	# get people by id
	@staticmethod
	def get_people_by_id(user_id):
		query = "SELECT * FROM user WHERE UserID = %d" % user_id
		cursor.execute(query)
		return cursor.fetchone()

	# get people by abbr
	@staticmethod
	def get_people_by_abbr(user_abbr):
		query = "SELECT * FROM user WHERE Abbr = '%s'" % user_abbr
		cursor.execute(query)
		return cursor.fetchone()
	
	# get name by id
	@staticmethod
	def get_name(user_id):
		query = "SELECT Name FROM user WHERE UserID = %d" % user_id
		cursor.execute(query)
		return cursor.fetchone()['Name']

	# get abbr by id
	@staticmethod
	def get_abbr(user_id):
		query = "SELECT Abbr FROM user WHERE UserID = %d" % user_id
		cursor.execute(query)
		return cursor.fetchone()['Abbr']

# UPDATE

	# active user
	@staticmethod
	def active_user(userID):
		query = "UPDATE user SET IsActive = 1 WHERE UserID = %d" % userID
		cursor.execute(query)
		return conn.commit()

	# add email to the user
	@staticmethod
	def add_email(user_id, email):
		query = "UPDATE user SET Email = '%s' WHERE UserID = %d" % (email, user_id)
		cursor.execute(query)
		return conn.commit()

# NEW

	# add a new user
	@staticmethod
	def add_user(userID, name, abbr, avatar, signature, desc, locationID, location):
		query = '''INSERT INTO user (UserID, Name, Abbr, Avatar, Signature, Description, LocationID, Location)\n
			VALUES (%d, '%s', '%s', '%s', '%s', '%s', %d, '%s')''' % (userID, name, abbr, avatar, signature, desc, locationID, location)
		cursor.execute(query)
		return conn.commit()

# CHECK
	
	# check user exist
	@staticmethod
	def check_user_exist(user_id):
		query = "SELECT * FROM user WHERE UserID = %d" % user_id
		#return query
		cursor.execute(query)
		return cursor.rowcount > 0

	# check user active
	@staticmethod
	def check_user_active(user_id):
		query = "SELECT * FROM user WHERE UserID = %d AND IsActive = 1" % user_id
		cursor.execute(query)
		return cursor.rowcount > 0


