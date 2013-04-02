from flask import g

class Comment:

# GET 

	# get all comments of a review
	@staticmethod
	def get_comments_by_review(review_id):
		query = '''SELECT c.CommentID, c.Comment, c.Replyer, c.ReplyerAbbr, c.Replyee, c.ReplyeeAbbr, c.Time, user.Avatar as ReplyerAvatar\n
			FROM review_comment AS c, user\n
			WHERE c.ReplyerAbbr = user.Abbr
			AND c.ReviewID = %d''' % review_id
		g.cursor.execute(query)
		return g.cursor.fetchall()

	# get all comments of a topic
	@staticmethod
	def get_comments_by_topic(topic_id):
		query = '''SELECT c.CommentID, c.Comment, c.Replyer, c.ReplyerAbbr, c.Replyee, c.ReplyeeAbbr, c.Time, user.Avatar as ReplyerAvatar\n
			FROM topic_comment AS c, user\n
			WHERE c.ReplyerAbbr = user.Abbr
			AND c.TopicID = %d
			ORDER BY c.Time DESC''' % topic_id
		g.cursor.execute(query)
		return g.cursor.fetchall()

# NEW

	# add comment to a review
	@staticmethod
	def add_comment_to_review(review_id, replyer, replyer_abbr, replyee, replyee_abbr, comment):
		query = "INSERT INTO review_comment (ReviewID, Replyer, ReplyerAbbr, Replyee, ReplyeeAbbr, Comment) VALUES (%d, '%s', '%s', '%s', '%s', '%s')" % (review_id, replyer, replyer_abbr, replyee, replyee_abbr, comment)
		g.cursor.execute(query)
		return g.conn.commit()

	# add comment to a topic
	@staticmethod
	def add_comment_to_topic(topic_id, replyer, replyer_abbr, replyee, replyee_abbr, comment):
		query = "INSERT INTO topic_comment (TopicID, Replyer, ReplyerAbbr, Replyee, ReplyeeAbbr, Comment) VALUES (%d, '%s', '%s', '%s', '%s', '%s')" % (topic_id, replyer, replyer_abbr, replyee, replyee_abbr, comment)
		g.cursor.execute(query)
		return g.conn.commit()