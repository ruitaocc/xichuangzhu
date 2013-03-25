from xichuangzhu import conn, cursor

class Quote:

# GET

	# get quotes by author
	@staticmethod
	def get_quotes_by_author(author_id):
		query = "SELECT * FROM author_quote WHERE AuthorID = %d" % author_id
		cursor.execute(query)
		return cursor.fetchall()

	# get quotes num by author
	@staticmethod
	def get_quotes_num_by_author(author_id):
		query = "SELECT COUNT(*) AS QuotesNum FROM author_quote WHERE AuthorID = %d" % author_id
		cursor.execute(query)
		return cursor.fetchone()['QuotesNum']

	# get quotes by id
	@staticmethod
	def get_quote_by_id(quote_id):
		query = "SELECT * FROM author_quote WHERE QuoteID = %d" % quote_id
		cursor.execute(query)
		return cursor.fetchone()

	# get quote by random
	@staticmethod
	def get_quote_by_random(author_id):
		query = "SELECT * FROM author_quote WHERE AuthorID = %d ORDER BY RAND() LIMIT 1" % author_id
		cursor.execute(query)
		return cursor.fetchone()

# UPDATE

	# edit quote
	@staticmethod
	def edit(quote_id, author_id, quote, work_id, work_title):
		query = "UPDATE author_quote SET AuthorID = %d, Quote = '%s', WorkID = %d, WorkTitle = '%s' WHERE QuoteID = %d" % (author_id, quote, work_id, work_title, quote_id)
		cursor.execute(query)
		return conn.commit()

# NEW

	# add quote
	@staticmethod
	def add(author_id, quote, work_id, work_title):
		query = "INSERT INTO author_quote (AuthorID, Quote, WorkID, WorkTitle) VALUES (%d, '%s', %d, '%s')" % (author_id, quote, work_id, work_title)
		cursor.execute(query)
		return conn.commit()

# DELETE

	# delete quote
	@staticmethod
	def delete(quote_id):
		query = "DELETE FROM author_quote WHERE QuoteID = %d" % quote_id
		cursor.execute(query)
		return conn.commit()