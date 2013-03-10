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

	# get hot authors
	@staticmethod
	def get_hot_authors(num):
		query = '''SELECT author.Author, author.Abbr, author.Quote, dynasty.Dynasty, dynasty.Abbr AS DynastyAbbr, count(*) AS LoveNum\n
			FROM love, work, author, dynasty\n
			WHERE love.WorkID = work.WorkID\n
			AND work.AuthorID = author.AuthorID\n
			AND author.DynastyID = dynasty.DynastyID\n
			GROUP BY author.AuthorID\n
			ORDER BY LoveNum DESC\n
			LIMIT %d''' % num
		cursor.execute(query)
		return cursor.fetchall()

	# get certain dynasty's authors
	@staticmethod
	def get_authors_by_dynasty(dynasty_id, num = 10000):
		query = '''SELECT *\n
			FROM author\n
			WHERE DynastyID = %d
			ORDER BY BirthYear ASC\n
			LIMIT %d''' % (dynasty_id, num)
		cursor.execute(query)
		return cursor.fetchall()

	# get authors num of certain dynasty's
	@staticmethod
	def get_authors_num_by_dynasty(dynasty_id):
		query = "SELECT COUNT(*) AS authors_num FROM author WHERE DynastyID = '%d'" % dynasty_id
		cursor.execute(query)
		return cursor.fetchone()['authors_num']

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
		query = '''INSERT INTO author (Author, Abbr, Quote, Introduction, BirthYear, DeathYear, DynastyID) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', %d)''' % (author, abbr, quote, introduction, birthYear, deathYear, dynastyID)
		cursor.execute(query)
		conn.commit()
		return cursor.lastrowid

# EDIT

	# edit an author
	@staticmethod
	def edit_author(author, abbr, quote, introduction, birthYear, deathYear, dynastyID, authorID):
		query = '''UPDATE author\n
			SET Author='%s', Abbr='%s', Quote='%s', Introduction='%s', BirthYear='%s', DeathYear='%s', DynastyID=%d WHERE AuthorID = %d''' % (author, abbr, quote, introduction, birthYear, deathYear, dynastyID, authorID)
		cursor.execute(query)
		return conn.commit()