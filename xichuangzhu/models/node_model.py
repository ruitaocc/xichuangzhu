from xichuangzhu import conn, cursor

class Node:

# GET

	# get all nodes
	@staticmethod
	def get_nodes():
		query = "SELECT * FROM node"
		cursor.execute(query)
		return cursor.fetchall()

	# get node by abbr
	@staticmethod
	def get_node_by_abbr(node_abbr):
		query = "SELECT * FROM node WHERE Abbr = '%s'" % node_abbr
		cursor.execute(query)
		return cursor.fetchone()