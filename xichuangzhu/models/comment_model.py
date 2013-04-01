from flask import g

class Comment:

# GET 

	# get all comments of a review
	@staticmethod
	def get_comments_by_review(review_id):
		query = '''SELECT comment.CommentID, comment.Comment, comment.Time, user.UserID, user.Name, user.Abbr AS UserAbbr, user.Avatar\n
			FROM review_comment AS comment, user\n
			WHERE comment.ReplyerID = user.UserID
			AND comment.ReviewID = %d''' % review_id
		g.cursor.execute(query)
		return g.cursor.fetchall()

	# get all comments of a topic
	@staticmethod
	def get_comments_by_topic(topic_id):
		query = '''SELECT comment.CommentID, comment.Comment, comment.Time, user.UserID, user.Name, user.Abbr AS UserAbbr, user.Avatar\n
			FROM topic_comment AS comment, user\n
			WHERE comment.ReplyerID = user.UserID
			AND comment.TopicID = %d''' % topic_id
		g.cursor.execute(query)
		return g.cursor.fetchall()

# NEW

	# add comment to a review
	@staticmethod
	def add_comment_to_review(review_id, replyer_id, replyee_id, comment):
		query = '''INSERT INTO review_comment (ReviewID, ReplyerID, ReplyeeID, Comment)\n
			VALUES (%d, %d, %d, '%s')''' % (review_id, replyer_id, replyee_id, comment)
		g.cursor.execute(query)
		return g.conn.commit()

	# add comment to a topic
	@staticmethod
	def add_comment_to_topic(topic_id, replyer_id, replyee_id, comment):
		query = "INSERT INTO topic_comment (TopicID, ReplyerID, ReplyeeID, Comment) VALUES (%d, %d, %d, '%s')" % (topic_id, replyer_id, replyee_id, comment)
		g.cursor.execute(query)
		# comment num + 1
		query = "UPDATE topic SET CommentNum = CommentNum + 1 WHERE TopicID = %d" % topic_id
		g.cursor.execute(query)
		return g.conn.commit()