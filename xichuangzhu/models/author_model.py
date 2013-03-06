from xichuangzhu import conn, cursor

class Author:

# GET

	# get authors by random
	@staticmethod
	def get_authors_by_random(authors_num):
		query = '''SELECT author.AuthorID, author.Author, author.Abbr, author.Quote, dynasty.DynastyID, dynasty.Dynasty, dynasty.Abbr AS DynastyAbbr\n
			FROM author, dynasty\n
			WHERE author.DynastyID = dynasty.DynastyID\n
			ORDER BY RAND()\n
			LIMIT %d''' % authors_num
		cursor.execute(query)
		return cursor.fetchall()

	# get all authors
	@staticmethod
	def get_authors():
		query = '''SELECT *\n
			FROM author, dynasty\n
			WHERE author.DynastyID = dynasty.DynastyID'''
		cursor.execute(query)
		return cursor.fetchall()

	# get certain dynasty's authors
	@staticmethod
	def get_authors_by_dynasty(dynastyID):
		query = '''SELECT *\n
			FROM author\n
			WHERE DynastyID = %d
			ORDER BY BirthYear''' % dynastyID
		cursor.execute(query)
		return cursor.fetchall()

	# get a author by id
	@staticmethod
	def get_author_by_id(authorID):
		query = '''SELECT author.AuthorID, author.Author, author.Abbr, author.Introduction, author.BirthYear, author.DeathYear, author.Quote, dynasty.DynastyID, dynasty.Dynasty, dynasty.Abbr AS DynastyAbbr\n
			FROM author, dynasty\n
			WHERE author.DynastyID = dynasty.DynastyID\n
			AND author.AuthorID = %d''' % authorID
		cursor.execute(query)
		return cursor.fetchone()

	# get a author by abbr
	@staticmethod
	def get_author_by_abbr(author_abbr):
		query = '''SELECT author.AuthorID, author.Author, author.Abbr, author.Introduction, author.BirthYear, author.DeathYear, author.Quote, dynasty.DynastyID, dynasty.Dynasty, dynasty.Abbr AS DynastyAbbr\n
			FROM author, dynasty\n
			WHERE author.Abbr = '%s'\n
			AND author.DynastyID = dynasty.DynastyID''' % author_abbr
		cursor.execute(query)
		return cursor.fetchone()

	# get authors by name
	@staticmethod
	def get_authors_by_name(name):
		query = "SELECT AuthorID, Author FROM author WHERE Author LIKE '%%%s%%'" % name
		cursor.execute(query)
		return cursor.fetchall()

# NEW

	# add a new author and return its AuthorID
	@staticmethod
	def add_author(author, abbr, quote, introduction, birthYear, deathYear, dynastyID):
		query = '''INSERT INTO author (Author, Abbr, Quote, Introduction, BirthYear, DeathYear, DynastyID) VALUES ('%s', '%s', '%s', '%s', %d, %d, %d)''' % (author, abbr, quote, introduction, birthYear, deathYear, dynastyID)
		cursor.execute(query)
		conn.commit()
		return cursor.lastrowid

# EDIT

	# edit an author
	@staticmethod
	def edit_author(author, abbr, quote, introduction, birthYear, deathYear, dynastyID, authorID):
		query = '''UPDATE author\n
			SET Author='%s', Abbr='%s', Quote='%s', Introduction='%s', BirthYear=%d, DeathYear=%d, DynastyID=%d WHERE AuthorID = %d''' % (author, abbr, quote, introduction, birthYear, deathYear, dynastyID, authorID)
		cursor.execute(query)
		return conn.commit()