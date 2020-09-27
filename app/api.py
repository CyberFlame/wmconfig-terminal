from backend.db_functions import FileFunctions
from backend.compare import Monitor
import sys, os, getpass

class ReplyHandler:
	def handler(reply):
		if reply['msg'][0]:
			if isinstance(reply['msg'][1], bytes):
				return reply['msg'][1].decode('utf-8')
			else:
				print(reply['msg'][1])
		else:
			print(reply['msg'][1])
			sys.exit()

class wmApi(ReplyHandler):
	def __init__(self):
		self.file_func = FileFunctions()
		self.monitor = Monitor()
		self.reply = ReplyHandler()

	def validate_file(self, path):
		if(os.path.isfile(path)):
			continue
		else:
			print('File({}) does not exist'.format(path))
			sys.exit()

	def check_user(self):
		user = getpass.getuser()
		if( user == 'root' ):
			return True
		else:
			return False

	def check(self):
		pass


	def compare(self, path):
		self.validate_file(path)
		old = self.reply.handler(self.file_func.get_content(path))
		new = self.reply.handler(self.file_func.read_file(path))
		self.monitor.diff(old, new)


	def add(self, path):
		self.validate_file(path)
		self.reply.handler(self.file_func.add_file(path))


	def update(self, path):
		self.validate_file(path)
		self.reply.handler(self.file_func.update_file(path))


	def delete(self, path):
		self.validate_file(path)
		db_path = self.reply.handler(self.file_func.get_path(path))

	def display(self, path):
		self.validate_file(path)
		db_data = self.reply.handler(self.file_func.get_content(path))
		print(db_data)

	def replace(self, path):
		pass

