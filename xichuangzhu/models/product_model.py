from flask import g

class Product:

# GET

	# get single product
	@staticmethod
	def get_product(product_id):
		query = "SELECT * FROM product WHERE ProductID = %d" % product_id
		g.cursor.execute(query)
		return g.cursor.fetchone()

	# get a product by random
	@staticmethod
	def get_product_by_random():
		query = "SELECT * FROM product ORDER BY RAND() LIMIT 1"
		g.cursor.execute(query)
		return g.cursor.fetchone()

	# get products by num
	@staticmethod
	def get_products(num):
		query = "SELECT * FROM product LIMIT %d" % num
		g.cursor.execute(query)
		return g.cursor.fetchall()

# NEW

	# add product
	@staticmethod
	def add_product(product, url, image_url, introduction):
		query = '''INSERT INTO product (Product, Url, ImageUrl, Introduction)\n
			VALUES ('%s', '%s', '%s', '%s')''' % (product, url, image_url, introduction)
		g.cursor.execute(query)
		g.conn.commit()
		return g.cursor.lastrowid

# EDIT

	# edit product
	@staticmethod
	def edit_product(product_id, product, url, image_url, introduction):
		query = '''UPDATE product SET Product = '%s', Url = '%s', ImageUrl = '%s', Introduction = '%s' WHERE ProductID = %d''' % (product, url, image_url, introduction, product_id)
		g.cursor.execute(query)
		return g.conn.commit()