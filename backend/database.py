import sqlite3, os
from sqlite3 import Error

class DatabaseSetup():
	def __init__(self):
		self.conn = sqlite3.connect(self.create_database())
		self.cursor = self.conn.cursor()


	def create_database(self):
		try:
			file = 'wmconfig.db'
			dir = '/var/lib/wmconfig'
			if not os.path.exists(dir):
				os.makedirs(dir)
			file = dir + '/' + file

			conn = sqlite3.connect(file)
		except Error as e:
			print(e)
		finally:
			if conn:
				conn.close()
		return file


	def create_tables(self):
		def drop_table(name):
			try:
				statement = "DROP TABLE IF EXISTS {};".format(name)
				self.cursor.execute(statement)
				self.conn.commit()
			except Error as e:
				print(e)


		def create_file_table():
			try:
				drop_table('FILES')
				statement = '''CREATE TABLE IF NOT EXISTS FILES (
                        	                PATH TEXT PRIMARY KEY NOT NULL,
						CONTENT BLOB NOT NULL
                                	);
					'''
				self.cursor.execute(statement)
				self.conn.commit()
			except Error as e:
				print(e)

		create_file_table()
