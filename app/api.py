from src.functions import FileFunctions
from src.compare import Monitor
import sys, os, getpass

class ReplyHandler:
	def __init__(self):
		pass

	def handler(self, reply):
		if reply['msg'][0]:
			if isinstance(reply['msg'][1], bytes):
				return reply['msg'][1].decode('utf-8')
			else:
				print("<SUCCESS>-[ {} ]\n".format(reply['msg'][1]))
		else:
			print("<ERROR>-[ {} ]\n".format(reply['msg'][1]))
			sys.exit()

class wmApi(ReplyHandler):
	def __init__(self):
		self.file_func = FileFunctions()
		self.monitor = Monitor()
		self.reply = ReplyHandler()


	def validate_file(self, path):
		n_path = path
		path = os.path.abspath(path)
		if(os.path.isfile(path)):
			return path
		else:
			print('Please provide the correct absolute path of this file({})\n'.format(n_path))
			sys.exit()


	def check_user(self):
		user = getpass.getuser()
		if( user == 'root' ):
			return True
		else:
			return False


	def check(self):
		paths = self.file_func.files_paths()
		if len(paths) >=1 :
			print('         < Cross checking files with backups >')
			length = len(max(paths, key=len))+15
			state = {True:' \x1b[31mWarning', False:'\x1b[32mNo Change'}
			reset = '\x1b[0m'
			for path in paths:
				change = self.compare(path, show=False)
				print(" {}[ {} {}]".format(path.ljust(length," "),  str(state[change]).ljust(14,' '),reset))
		else:
			print("<ERROR>-[ No file has been added to database ]\n")


	def compare(self, path, show=True):
		path = self.validate_file(path)
		old = self.reply.handler(self.file_func.get_content(path))
		new = self.reply.handler(self.file_func.read_file(path))
		if show:
			change = self.monitor.diff(old, new, display=False)
			state = {True:' \x1b[31mWarning', False:'\x1b[32mNo Change'}
			reset = '\x1b[0m'
			print("	<<<<<<<<<<<<<<<<<<<<[ {} {}]>>>>>>>>>>>>>>>>>>>\n".format(state[change], reset))
			self.monitor.diff(old, new)
		else:
			change = self.monitor.diff(old, new, display=show)
			return change

	def add(self, path):
		path = self.validate_file(path)
		self.reply.handler(self.file_func.add_file(path))


	def update(self, path):
		path = self.validate_file(path)
		self.reply.handler(self.file_func.update_file(path))


	def delete(self, path):
		path = self.validate_file(path)
		db_path = self.reply.handler(self.file_func.get_path(path))
		if path == db_path:
			self.reply.handler(self.file_func.delete_file(path))
		else:
			pass

	def display(self, path):
		path = self.validate_file(path)
		db_data = self.reply.handler(self.file_func.get_content(path))
		print("	<<<<<<<<<<<<<<<<<<<<[ Backup Content ]>>>>>>>>>>>>>>>>>>>\n")
		print(db_data)

	def replace(self, path):
		path = self.validate_file(path)
		db_path = self.reply.handler(self.file_func.get_path(path))
		if path == db_path:
			content = self.reply.handler(self.file_func.get_content(db_path))
			self.file_func.write_file(db_path, content)
			print('{} has been replaced with backup'.format(path))
		else:
			print("<ERROR>-[ '{}' does not exist in system/database ]".format(path))

	def print_title(self):
		print(" [ Watch My Config version 1.0 ]\n")
