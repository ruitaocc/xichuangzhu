#-*- coding: UTF-8 -*-

from flask import g

class Widget:

# GET

	# get all widgets of a target
	@staticmethod
	def get_widgets(target_type, target_id):
		query = "SELECT * FROM widget WHERE Type = '%s' AND TargetID = %d ORDER BY PositionIndex ASC" % (target_type, target_id)
		g.cursor.execute(query)
		return g.cursor.fetchall()

	# get a widget
	@staticmethod
	def get_widget(widget_id):
		query = "SELECT * FROM widget WHERE WidgetID = %d" % widget_id
		g.cursor.execute(query)
		return g.cursor.fetchone()

# NEW

	# add new widget to a target
	@staticmethod
	def add_widget(target_type, target_id, title, content, position_index):
		query = '''INSERT INTO widget (Type, TargetID, Title, Content, PositionIndex)\n
			VALUES ('%s', %d, '%s', '%s', %d)''' % (target_type, target_id, title, content, position_index)
		g.cursor.execute(query)
		g.conn.commit()
		return g.cursor.lastrowid

# EDIT 

	# edit a widget
	@staticmethod
	def edit_widget(widget_id, title, content, position_index):
		query = '''UPDATE widget SET Title = '%s', Content = '%s', PositionIndex = %d\n
			WHERE WidgetID = %d''' % (title, content, position_index, widget_id)
		g.cursor.execute(query)
		return g.conn.commit()

# DELETE

	# delete a widget
	@staticmethod
	def delete_widget(widget_id):
		query = "DELETE FROM widget WHERE WidgetID = %d" % widget_id
		g.cursor.execute()
		return g.conn.commit()