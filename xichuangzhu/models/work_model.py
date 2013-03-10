#-*- coding: UTF-8 -*-

from xichuangzhu import conn, cursor

class Work:

# GET

	# get a single work
	@staticmethod
	def get_work(workID):
		query = '''SELECT work.WorkID, work.Title, work.Type, work.TypeName, work.Content, work.Foreword, work.Introduction AS WorkIntroduction, work.Type, work.CollectionID, author.AuthorID, author.Author, author.Abbr AS AuthorAbbr, author.Introduction AS AuthorIntroduction, dynasty.Dynasty, dynasty.Abbr AS DynastyAbbr, collection.Collection, collection.Introduction\n
			FROM work, author, dynasty, collection\n
			WHERE work.workID = %d\n
			AND work.AuthorID = author.AuthorID\n
			AND work.DynastyID = dynasty.DynastyID\n
			AND work.collectionID = collection.CollectionID\n''' % workID
		cursor.execute(query)
		return cursor.fetchone()

	# get works by random
	@staticmethod
	def get_works_by_random(worksNum):
		query = '''SELECT work.WorkID, work.Title, work.Type, work.TypeName, work.Content, author.Author, author.Abbr AS AuthorAbbr\n
			FROM work, author\n
			WHERE work.AuthorID = author.AuthorID\n
			ORDER BY RAND()\n
			LIMIT %d''' % worksNum
		cursor.execute(query)
		return cursor.fetchall()

	# get works by random
	@staticmethod
	def get_work_by_random(work_type):
		query = '''SELECT work.WorkID, work.Title, work.Type, work.TypeName, work.Content, author.Author, author.Abbr AS AuthorAbbr\n
			FROM work, author\n
			WHERE work.AuthorID = author.AuthorID\n
			AND work.Type = '%s'\n
			ORDER BY RAND()\n
			LIMIT 1''' % work_type
		cursor.execute(query)
		return cursor.fetchone()

	# get all works
	@staticmethod
	def get_works(work_type, dynasty_id, page, num):
		query = '''SELECT work.WorkID, work.Title, work.Type, work.TypeName, work.Content, work.AuthorID, author.Author, author.Abbr AS AuthorAbbr\n
			FROM work, author\n
			WHERE work.AuthorID = author.AuthorID\n'''

		if work_type != 'all':
			query += "AND work.Type = '%s'\n" % work_type

		if dynasty_id != 0:
			query += "AND work.DynastyID = %d\n" % dynasty_id

		query += "LIMIT %d, %d" % ((page-1)*num, num)

		#return query

		cursor.execute(query)
		return cursor.fetchall()

	# get all works
	@staticmethod
	def get_works_num(work_type, dynasty_id):
		query = '''SELECT COUNT(*) AS WorksNum\n
			FROM work, author\n
			WHERE work.AuthorID = author.AuthorID\n'''

		if work_type != 'all':
			query += "AND work.Type = '%s'\n" % work_type

		if dynasty_id != 0:
			query += "AND work.DynastyID = %d\n" % dynasty_id

		cursor.execute(query)
		return cursor.fetchone()['WorksNum']

	# get an author's all works
	@staticmethod
	def get_works_by_author(authorID):
		query = "SELECT * FROM work WHERE AuthorID=%d" % authorID
		cursor.execute(query)
		return cursor.fetchall()

	# get an collection's all works
	@staticmethod
	def get_works_by_collection(collectionID):
		query = "SELECT * FROM work WHERE CollectionID = %d" % collectionID
		cursor.execute(query)
		return cursor.fetchall()

	# get all work types
	@staticmethod
	def get_types():
		query = "SELECT * FROM work_type"
		cursor.execute(query)
		return cursor.fetchall()

	# get chinese name of a work type
	@staticmethod
	def get_type_name(work_type):
		query = "SELECT TypeName From work_type WHERE WorkType = '%s'" % work_type
		cursor.execute(query)
		return cursor.fetchone()['TypeName']

# NEW

	# add a work
	@staticmethod
	def add_work(title, content, foreword, introduction, authorID, dynastyID, collectionID, work_type, type_name):
		query = '''INSERT INTO work (Title, Content, Foreword, Introduction, AuthorID, DynastyID, CollectionID, Type, TypeName)\n
			VALUES ('%s', '%s', '%s','%s', %d, %d, %d, '%s', '%s')''' % (title, content, foreword, introduction, authorID, dynastyID, collectionID, work_type, type_name)
		cursor.execute(query)
		conn.commit()
		return cursor.lastrowid

# EDIT

	# edit a Work
	@staticmethod
	def edit_work(title, content, foreword, introduction, authorID, dynastyID, collectionID, work_type, type_name, work_id):
		query = '''UPDATE work SET Title = '%s', Content = '%s', Foreword = '%s', Introduction = '%s', AuthorID = %d, DynastyID = %d, CollectionID = %d, Type = '%s', TypeName = '%s' WHERE WorkID=%d''' % (title, content, foreword, introduction, authorID, dynastyID, collectionID, work_type, type_name, work_id)
		cursor.execute(query)
		return conn.commit()

# DELETE

	# delete a work
	@staticmethod
	def delete_work(workID):
		query = "DELETE FROM work WHERE WorkID = %d" % workID
		cursor.execute(query)
		return conn.commit()