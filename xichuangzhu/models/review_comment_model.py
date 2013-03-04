from xichuangzhu import conn, cursor

class Review_comment:

# GET 

	# get comments by review
	@staticmethod
	def get_comments_by_review(review_id):
		query = '''SELECT comment.CommentID, comment.Comment, comment.Time, user.UserID, user.Name, user.Abbr AS UserAbbr, user.Avatar\n
			FROM review_comment AS comment, user\n
			WHERE comment.ReplyerID = user.UserID
			AND comment.ReviewID = %d''' % review_id
		cursor.execute(query)
		return cursor.fetchall()

# NEW

	# add comment to a review
	@staticmethod
	def add_comment(review_id, replyer_id, replyee_id, comment):
		query = '''INSERT INTO review_comment (ReviewID, ReplyerID, ReplyeeID, Comment)\n
			VALUES (%d, %d, %d, '%s')''' % (review_id, replyer_id, replyee_id, comment)
		cursor.execute(query)
		return conn.commit()