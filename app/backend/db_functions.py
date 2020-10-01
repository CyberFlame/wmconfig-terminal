import sqlite3, os, hashlib

schema = {'files':['path','content']}

def insert(table, fields):
	attributes = ''
	value = ''
	statement = 'INSERT INTO {} ({}) VALUES({})'

	for i in range(len(fields)):
		attributes += str(fields[i]).upper()
		value += '?'
		if(i != len(fields)-1):
			attributes += ', '
			value += ', '
	return statement.format(table, attributes, value)


def update(table, fields, where):
	attributes = ''
	w_value = str(where).upper() + ' = ?'
	statement = 'UPDATE {} SET {}WHERE {}'
	for i in range(len(fields)):
		attributes += str(fields[i]).upper() +  ' = ? '
		if(i != len(fields)-1):
			attributes += ','
	return statement.format(table, attributes, w_value)


def delete(table, where):
	statement = 'DELETE FROM {} WHERE {}'
	w_value = str(where).upper() + '= ?'
	return statement.format(table, w_value)


def select(table, fields, where):
	attributes = ''
	w_value = str(where).upper() + ' = ?'
	statement = 'SELECT {} FROM {} WHERE {}'
	for i in range(len(fields)):
		attributes += str(fields[i]).upper()
		if(i != len(fields)-1):
			attributes += ', '
	return statement.format(attributes, table, w_value)



class FileFunctions:
	def __init__(self):
		self.conn = None
		self.cursor = None


	def add_file(self, path):
		content = self.read_file(path)['msg'][1]
		try:
			self.create_connection()
			self.cursor.execute(insert('files', schema['files']),(path, content))
			self.conn.commit()
			self.close_connection()
			return {'msg':[True, '{} has been added'.format(path)]}
		except sqlite3.Error as e:
			return {'msg':[False, '{} already exists in database'.format(path)]}

	def update_file(self, path):
		content = self.read_file(path)
		try:
			self.create_connection()
			self.cursor.execute(update('files', schema['files'], 'path'),(path, content, path))
			self.conn.commit()
			self.close_connection()
			return {'msg':[True, '{} has been updated'.format(path)]}
		except sqlite3.Error as e:
			return {'msg':[False, 'Database Error: '.format(e.args)]}


	def delete_file(self, path):
		try:
			self.create_connection()
			self.cursor.execute(delete('files', 'path'), (path,))
			self.conn.commit()
			self.close_connection()
			return {'msg':[True, '{} has been deleted'.format(path)]}
		except sqlite3.Error as e:
			return {'msg':[False, 'Database Error: {}'.format(e.args)]}


	def get_content(self, path):
		try:
			self.create_connection()
			self.cursor.execute(select('files', schema['files'], 'path'), (path, ))
			record = self.cursor.fetchall()
			file_data = record[0][1]
			self.close_connection()
			return {'msg':[True,file_data]}
		except sqlite3.Error as e:
			return {'msg':[False, 'Database Error: {}'.format(e.args)]}

	def get_path(self, path):
		try:
			self.create_connection()
			self.cursor.execute(select('files',schema['files'], 'path'),(path,))
			record = self.cursor.fetchall()
			if len(record) >= 1:
				file_path = record[0][0]
				return {'msg':[True,file_path.encode('utf-8')]}
			else:
				return {'msg':[False, '{} does not exist in database'.format(path)]}
			self.close_connection()
		except sqlite3.Error as e:
			return {'msg':[False, 'Database Error: {}'.format(e.args)]}

	def read_file(self, path):
		file_data = None
		with open(path,'rb') as file:
			file_data = file.read()

		return {'msg':[True,file_data]}

	def write_file(self, path, content):
		config = open(path,'w')
		config.write(content)
		config.close()

	def create_connection(self):
		path = '/var/lib/wmconfig/wmconfig.db'
		if(os.path.isfile(path)):
			self.conn = sqlite3.connect(path)
			self.cursor = self.conn.cursor()
		else:
			print('Database file not found')

	def close_connection(self):
		self.conn.close()


	def files_paths(self):
		paths = []
		try:
			self.create_connection()
			self.cursor.execute('SELECT PATH FROM FILES')
			record = self.cursor.fetchall()
			for i in record:
				paths.append(i[0])

			self.close_connection()
			return paths
		except sqlite3.Error as e:
			pass
