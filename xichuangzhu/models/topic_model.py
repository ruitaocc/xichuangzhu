from flask import g

class Topic:

# GET

	# get a topic
	@staticmethod
	def get_topic(topic_id):
		query = '''SELECT topic.TopicID, topic.Title, topic.Content, topic.CommentNum, topic.Time, topic.ClickNum, node.Name AS NodeName, node.Abbr AS NodeAbbr, node.NodeID, user.Name AS UserName, user.Abbr AS UserAbbr, user.Avatar, user.UserID\n
			FROM topic, user, node\n
			WHERE topic.UserID = user.UserID\n
			AND topic.NodeID = node.NodeID\n
			AND topic.TopicID = %d''' % topic_id
		g.cursor.execute(query)
		return g.cursor.fetchone()

	# get topics
	@staticmethod
	def get_topics(num):
		query = '''SELECT topic.TopicID, topic.Title, topic.CommentNum, topic.Time, node.NodeID, node.Name AS NodeName, node.Abbr AS NodeAbbr, user.Name AS UserName, user.Abbr AS UserAbbr, user.Avatar\n
			FROM topic, user, node\n
			WHERE topic.UserID = user.UserID\n
			AND topic.NodeID = node.NodeID\n
			ORDER BY Time DESC LIMIT %d''' % num
		g.cursor.execute(query)
		return g.cursor.fetchall()

	# get topics by user
	@staticmethod
	def get_topics_by_user(user_id, page, num):
		query = '''SELECT topic.TopicID, topic.Title, topic.CommentNum, topic.Time, node.NodeID, node.Name AS NodeName, node.Abbr AS NodeAbbr, user.Name AS UserName, user.Abbr AS UserAbbr, user.Avatar\n
			FROM topic, user, node\n
			WHERE topic.UserID = user.UserID\n
			AND topic.NodeID = node.NodeID\n
			AND topic.UserID = %d
			ORDER BY Time DESC LIMIT %d, %d''' % (user_id, (page-1)*num, num)
		g.cursor.execute(query)
		return g.cursor.fetchall()

	# get topics num by user
	@staticmethod
	def get_topics_num_by_user(user_id, page, num):
		query = "SELECT COUNT(*) AS TopicsNum FROM topic WHERE topic.UserID = user.UserID" % user_id
		g.cursor.execute(query)
		return g.cursor.fetchone()['TopicsNum']

	# get hot topics
	@staticmethod
	def get_hot_topics(num):
		query = '''SELECT topic.TopicID, topic.Title, user.Abbr AS UserAbbr, user.Avatar\n
			FROM topic, user\n
			WHERE topic.UserID = user.UserID\n
			ORDER BY topic.CommentNum DESC LIMIT %d''' % num
		g.cursor.execute(query)
		return g.cursor.fetchall()

	# get topics by node
	@staticmethod
	def get_topics_by_node(node_abbr):
		query = '''SELECT topic.TopicID, topic.Title, topic.CommentNum, topic.Time, node.NodeID, node.Name AS NodeName, node.Abbr AS NodeAbbr, user.Name AS UserName, user.Abbr AS UserAbbr, user.Avatar\n
			FROM topic, user, node\n
			WHERE topic.UserID = user.UserID\n
			AND topic.NodeID = node.NodeID
			AND node.Abbr = '%s'\n
			ORDER BY Time DESC''' % node_abbr
		g.cursor.execute(query)
		return g.cursor.fetchall()

# NEW

	# add topic
	@staticmethod
	def add(node_id, title, content, user_id):
		query = "INSERT INTO topic (NodeID, Title, Content, UserID) VALUES (%d, '%s', '%s', %d)" % (node_id, title, content, user_id)
		g.cursor.execute(query)
		g.conn.commit()
		return g.cursor.lastrowid

# UPDATE

	# edit topic
	@staticmethod
	def edit(topic_id, node_id, title, content):
		query = "UPDATE topic SET NodeID = %d, Title = '%s', Content = '%s' WHERE TopicID = %d" % (node_id, title, content, topic_id)
		g.cursor.execute(query)
		return g.conn.commit()

	# add click num
	@staticmethod
	def add_click_num(topic_id):
		query = "UPDATE topic SET ClickNum = ClickNum + 1 WHERE TopicID = %d" % topic_id
		g.cursor.execute(query)
		return g.conn.commit()

	# add comment num
	@staticmethod
	def add_comment_num(topic_id):
		query = "UPDATE topic SET CommentNum = CommentNum + 1 WHERE TopicID = %d" % topic_id
		g.cursor.execute(query)
		return g.conn.commit()