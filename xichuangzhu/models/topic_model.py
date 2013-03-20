from xichuangzhu import conn, cursor

class Topic:

# GET

	# get a topic
	@staticmethod
	def get_topic(topic_id):
		query = '''SELECT topic.TopicID, topic.Title, topic.Content, topic.CommentNum, topic.Time, node.Name AS NodeName, node.Abbr AS NodeAbbr, user.Name AS UserName, user.Abbr AS UserAbbr, user.Avatar\n
			FROM topic, user, node\n
			WHERE topic.UserID = user.UserID\n
			AND topic.NodeID = node.NodeID\n
			AND topic.TopicID = %d''' % topic_id
		cursor.execute(query)
		return cursor.fetchone()

	# get topics
	@staticmethod
	def get_topics(num):
		query = '''SELECT topic.TopicID, topic.Title, topic.CommentNum, topic.Time, node.NodeID, node.Name AS NodeName, node.Abbr AS NodeAbbr, user.Name AS UserName, user.Abbr AS UserAbbr, user.Avatar\n
			FROM topic, user, node\n
			WHERE topic.UserID = user.UserID\n
			AND topic.NodeID = node.NodeID\n
			ORDER BY Time DESC LIMIT %d''' % num
		cursor.execute(query)
		return cursor.fetchall()

	# get hot topics
	@staticmethod
	def get_hot_topics(num):
		query = '''SELECT topic.TopicID, topic.Title, user.Abbr AS UserAbbr, user.Avatar\n
			FROM topic, user\n
			WHERE topic.UserID = user.UserID\n
			ORDER BY topic.CommentNum DESC LIMIT %d''' % num
		cursor.execute(query)
		return cursor.fetchall()

	# get topics by node
	@staticmethod
	def get_topics_by_node(node_abbr):
		query = '''SELECT topic.TopicID, topic.Title, topic.CommentNum, topic.Time, node.NodeID, node.Name AS NodeName, node.Abbr AS NodeAbbr, user.Name AS UserName, user.Abbr AS UserAbbr, user.Avatar\n
			FROM topic, user, node\n
			WHERE topic.UserID = user.UserID\n
			AND topic.NodeID = node.NodeID
			AND node.Abbr = '%s'\n
			ORDER BY Time DESC''' % node_abbr
		cursor.execute(query)
		return cursor.fetchall()