from flask import g

class Node:

# GET

	# get all nodes
	@staticmethod
	def get_nodes(num):
		query = "SELECT * FROM node LIMIT %d" % num
		g.cursor.execute(query)
		return g.cursor.fetchall()

	# get node by abbr
	@staticmethod
	def get_node_by_abbr(node_abbr):
		query = "SELECT * FROM node WHERE Abbr = '%s'" % node_abbr
		g.cursor.execute(query)
		return g.cursor.fetchone()

	# get node by id
	@staticmethod
	def get_node_by_id(node_id):
		query = "SELECT * FROM node WHERE NodeID = %d" % node_id
		g.cursor.execute(query)
		return g.cursor.fetchone()