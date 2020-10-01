#!/usr/bin/python3
import getpass, re, os, sys
import server.database as db

class ServiceSetup():
	def __init__(self):
		self.data = db.DatabaseSetup()
		self.pattern = '([Yy][eE][sS])|([Nn][oO])'
		self.yes = '([Yy][eE][sS])'
		self.no = '([Nn][oO])'
		self.root_check()
		self.setup_database()
		self.file_handler()


	def file_handler(self):
		wm_path = './files/wmconfig'
		if(os.path.isfile(wm_path) and os.path.exists('/usr/bin/')):
			os.chmod(wm_path, 0o755)
			os.popen('cp ./files/wmconfig /usr/bin/')

		if not os.path.exists('/usr/share/wmc'):
			os.makedirs('/usr/share/wmc')

		if os.path.exists('./app'):
			os.popen('cp -r ./app/* /usr/share/wmc/')

		if(os.path.isfile('cp ./files/wmconfig.service') and os.path.exists('/etc/systemd/system/')):
			os.popen('cp ./files/wmconfig.service /etc/systemd/system/')


	def root_check(self):
		try:
			user = getpass.getuser()
			if( user == 'root' ):
				pass
			else:
				print('Run installation as root')
				sys.exit()
		except getpass.GetPassWarning as e:
			print(e)


	def setup_database(self):
		self.data.create_tables()
		self.data.conn.close()



ServiceSetup()
