from flask import g

class Author:

# GET

	# get authors by random
	@staticmethod
	def get_authors_by_random(num):
		query = '''SELECT author.AuthorID, author.Author, author.Abbr, dynasty.DynastyID, dynasty.Dynasty, dynasty.Abbr AS DynastyAbbr\n
			FROM author, dynasty\n
			WHERE author.DynastyID = dynasty.DynastyID\n
			ORDER BY RAND()\n
			LIMIT %d''' % num
		g.cursor.execute(query)
		return g.cursor.fetchall()

	# get all authors
	@staticmethod
	def get_authors():
		query = '''SELECT *\n
			FROM author, dynasty\n
			WHERE author.DynastyID = dynasty.DynastyID'''
		g.cursor.execute(query)
		return g.cursor.fetchall()

	# get hot authors
	@staticmethod
	def get_hot_authors(num):
		query = '''SELECT author.AuthorID, author.Author, author.Abbr, dynasty.Dynasty, dynasty.Abbr AS DynastyAbbr\n
			FROM love_work, work, author, dynasty\n
			WHERE love_work.WorkID = work.WorkID\n
			AND work.AuthorID = author.AuthorID\n
			AND author.DynastyID = dynasty.DynastyID\n
			GROUP BY author.AuthorID\n
			ORDER BY love_work.Time DESC\n
			LIMIT %d''' % num
		g.cursor.execute(query)
		return g.cursor.fetchall()

	# get certain dynasty's authors
	@staticmethod
	def get_authors_by_dynasty(dynasty_id, num = 10000):
		query = '''SELECT *\n
			FROM author\n
			WHERE DynastyID = %d
			ORDER BY BirthYear ASC\n
			LIMIT %d''' % (dynasty_id, num)
		g.cursor.execute(query)
		return g.cursor.fetchall()

	# get authors num of certain dynasty's
	@staticmethod
	def get_authors_num_by_dynasty(dynasty_id):
		query = "SELECT COUNT(*) AS authors_num FROM author WHERE DynastyID = '%d'" % dynasty_id
		g.cursor.execute(query)
		return g.cursor.fetchone()['authors_num']

	# get a author by id
	@staticmethod
	def get_author_by_id(authorID):
		query = '''SELECT author.AuthorID, author.Author, author.Abbr, author.Introduction, author.BirthYear, author.DeathYear, dynasty.DynastyID, dynasty.Dynasty, dynasty.Abbr AS DynastyAbbr\n
			FROM author, dynasty\n
			WHERE author.DynastyID = dynasty.DynastyID\n
			AND author.AuthorID = %d''' % authorID
		g.cursor.execute(query)
		return g.cursor.fetchone()

	# get a author by abbr
	@staticmethod
	def get_author_by_abbr(author_abbr):
		query = '''SELECT author.AuthorID, author.Author, author.Abbr, author.Introduction, author.BirthYear, author.DeathYear, dynasty.DynastyID, dynasty.Dynasty, dynasty.Abbr AS DynastyAbbr\n
			FROM author, dynasty\n
			WHERE author.Abbr = '%s'\n
			AND author.DynastyID = dynasty.DynastyID''' % author_abbr
		g.cursor.execute(query)
		return g.cursor.fetchone()

	# get authors by name
	@staticmethod
	def get_authors_by_name(name):
		query = '''SELECT author.AuthorID, author.Author, dynasty.Dynasty\n
			FROM author, dynasty\n
			WHERE Author LIKE '%%%s%%'\n
			AND author.DynastyID = dynasty.DynastyID''' % name
		g.cursor.execute(query)
		return g.cursor.fetchall()

# NEW

	# add a new author and return its AuthorID
	@staticmethod
	def add_author(author, abbr, introduction, birthYear, deathYear, dynastyID):
		query = '''INSERT INTO author (Author, Abbr, Introduction, BirthYear, DeathYear, DynastyID) VALUES ('%s', '%s', '%s', '%s', '%s', %d)''' % (author, abbr, introduction, birthYear, deathYear, dynastyID)
		g.cursor.execute(query)
		g.conn.commit()
		return g.cursor.lastrowid

# EDIT

	# edit an author
	@staticmethod
	def edit_author(author, abbr, introduction, birthYear, deathYear, dynastyID, authorID):
		query = '''UPDATE author\n
			SET Author='%s', Abbr='%s', Introduction='%s', BirthYear='%s', DeathYear='%s', DynastyID=%d WHERE AuthorID = %d''' % (author, abbr, introduction, birthYear, deathYear, dynastyID, authorID)
		g.cursor.execute(query)
		return g.conn.commit()