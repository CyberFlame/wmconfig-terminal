import getpass, re, os, sys
import server.database as db

class ServiceSetup():
	def __init__(self):
		self.data = db.DatabaseSetup()
		self.root_check()
		self.setup_database()
		self.file_handler()
		self.run_service()


	def file_handler(self):
		os.chmod('./files/wmconfig', 0o754)
		os.popen('cp ./files/wmconfig /usr/bin/')
		if not os.path.exists('/usr/share/wmc'):
			os.makedirs('/usr/share/wmc')
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


	def run_service(self):
		pattern = '([Yy][eE][sS])|([Nn][oO])'
		result = None
		while(not result):
			answer = input("do you want to start the service?(yES/No):  ")
			result = re.match(pattern, answer)

		if(re.match('([Yy][eE][sS])', answer)):
			os.popen('systemctl start panoptes.service')

		if(re.match('([Nn][oO])', answer)):
			print("Installation 100% finished")
			sys.exit()


	def setup_database(self):
		self.data.create_tables()
		self.data.conn.close()



ServiceSetup()
