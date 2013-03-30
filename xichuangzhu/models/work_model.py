#-*- coding: UTF-8 -*-

from flask import g

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
		g.cursor.execute(query)
		return g.cursor.fetchone()

	# get works by random
	@staticmethod
	def get_works_by_random(worksNum):
		query = '''SELECT work.WorkID, work.Title, work.Type, work.TypeName, work.Content, author.Author, author.Abbr AS AuthorAbbr\n
			FROM work, author\n
			WHERE work.AuthorID = author.AuthorID\n
			ORDER BY RAND()\n
			LIMIT %d''' % worksNum
		g.cursor.execute(query)
		return g.cursor.fetchall()

	# get works by random
	@staticmethod
	def get_work_by_random(work_type):
		query = '''SELECT work.WorkID, work.Title, work.Type, work.TypeName, work.Content, author.Author, author.Abbr AS AuthorAbbr\n
			FROM work, author\n
			WHERE work.AuthorID = author.AuthorID\n
			AND work.Type = '%s'\n
			ORDER BY RAND()\n
			LIMIT 1''' % work_type
		g.cursor.execute(query)
		return g.cursor.fetchone()

	# get works of certain type in certain dynasty
	@staticmethod
	def get_works(work_type, dynasty_abbr, page, num):
		query = '''SELECT work.WorkID, work.Title, work.Type, work.TypeName, work.Content, work.AuthorID, author.Author, author.Abbr AS AuthorAbbr\n
			FROM work, author, dynasty\n
			WHERE work.AuthorID = author.AuthorID
			AND work.DynastyID = dynasty.DynastyID\n'''

		if work_type != 'all':
			query += "AND work.Type = '%s'\n" % work_type
		if dynasty_abbr != 'all':
			query += "AND dynasty.Abbr = '%s'\n" % dynasty_abbr

		query += "LIMIT %d, %d" % ((page-1)*num, num)

		g.cursor.execute(query)
		return g.cursor.fetchall()

	# get works num of certain type in certain dynasty
	@staticmethod
	def get_works_num(work_type, dynasty_abbr):
		query = '''SELECT COUNT(*) AS WorksNum\n
			FROM work, dynasty\n
			WHERE work.DynastyID = dynasty.DynastyID\n'''

		if work_type != 'all':
			query += "AND work.Type = '%s'\n" % work_type
		if dynasty_abbr != 'all':
			query += "AND dynasty.Abbr = '%s'\n" % dynasty_abbr

		g.cursor.execute(query)
		return g.cursor.fetchone()['WorksNum']

	# get works by tag
	@staticmethod
	def get_works_by_tag(tag, page, num):
		query = '''SELECT work.WorkID, work.Title, work.Type, work.TypeName, work.Content, work.AuthorID, author.Author, author.Abbr AS AuthorAbbr\n
			FROM work, author, work_tag\n
			WHERE work.AuthorID = author.AuthorID\n
			AND work_tag.Tag = '%s'\n
			AND work_tag.WorkID = work.WorkID\n
			LIMIT %d, %d''' % (tag, (page-1)*num, num)

		g.cursor.execute(query)
		return g.cursor.fetchall()

	# get works num by tag
	@staticmethod
	def get_works_num_by_tag(tag):
		query = '''SELECT COUNT(*) AS WorksNum\n
			FROM work, work_tag\n
			WHERE work_tag.Tag = '%s'\n
			AND work_tag.WorkID = work.WorkID''' % tag
		g.cursor.execute(query)
		return g.cursor.fetchone()['WorksNum']

	# get an author's all works
	@staticmethod
	def get_works_by_author(authorID):
		query = "SELECT * FROM work WHERE AuthorID=%d" % authorID
		g.cursor.execute(query)
		return g.cursor.fetchall()

	# get an author's other works
	@staticmethod
	def get_other_works_by_author(author_id, work_id, num):
		query = '''SELECT * FROM work\n
			WHERE AuthorID = %d\n
			AND WorkID != %d\n
			ORDER BY RAND()\n
			LIMIT %d''' % (author_id, work_id, num)
		g.cursor.execute(query)
		return g.cursor.fetchall()		

	# get an collection's all works
	@staticmethod
	def get_works_by_collection(collectionID):
		query = "SELECT * FROM work WHERE CollectionID = %d" % collectionID
		g.cursor.execute(query)
		return g.cursor.fetchall()

	# get all work types
	@staticmethod
	def get_types():
		query = "SELECT * FROM work_type"
		g.cursor.execute(query)
		return g.cursor.fetchall()

	# get chinese name of a work type
	@staticmethod
	def get_type_name(work_type):
		query = "SELECT TypeName From work_type WHERE WorkType = '%s'" % work_type
		g.cursor.execute(query)
		return g.cursor.fetchone()['TypeName']

# NEW

	# add a work
	@staticmethod
	def add_work(title, content, foreword, introduction, authorID, dynastyID, collectionID, work_type, type_name):
		query = '''INSERT INTO work (Title, Content, Foreword, Introduction, AuthorID, DynastyID, CollectionID, Type, TypeName)\n
			VALUES ('%s', '%s', '%s','%s', %d, %d, %d, '%s', '%s')''' % (title, content, foreword, introduction, authorID, dynastyID, collectionID, work_type, type_name)
		g.cursor.execute(query)
		g.conn.commit()
		return g.cursor.lastrowid

# EDIT

	# edit a Work
	@staticmethod
	def edit_work(title, content, foreword, introduction, authorID, dynastyID, collectionID, work_type, type_name, work_id):
		query = '''UPDATE work SET Title = '%s', Content = '%s', Foreword = '%s', Introduction = '%s', AuthorID = %d, DynastyID = %d, CollectionID = %d, Type = '%s', TypeName = '%s' WHERE WorkID=%d''' % (title, content, foreword, introduction, authorID, dynastyID, collectionID, work_type, type_name, work_id)
		g.cursor.execute(query)
		return g.conn.commit()

# DELETE

	# delete a work
	@staticmethod
	def delete_work(workID):
		query = "DELETE FROM work WHERE WorkID = %d" % workID
		g.cursor.execute(query)
		return g.conn.commit()