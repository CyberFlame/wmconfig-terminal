#!/usr/bin/python3
import getpass, re, os, sys, shutil
import server.database as db

def root_check():
	try:
		user = getpass.getuser()
		if( user == 'root' ):
			pass
		else:
			print('Run installation as root\n')
			sys.exit()
	except getpass.GetPassWarning as e:
		print(e)

class Install:
	def __init__(self):
		root_check()
		self.data = db.DatabaseSetup()
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


	def setup_database(self):
		self.data.create_tables()
		self.data.conn.close()

class Uninstall:
	def __init__(self):
		root_check()
		self.remove_files()

	def remove_files(self):
		if os.path.exists('/usr/share/wmc'):
			shutil.rmtree('/usr/share/wmc')

		if os.path.isfile('/usr/bin/wmconfig'):
			os.remove('/usr/bin/wmconfig')


if __name__ == "__main__":
	if len(sys.argv)==2 and sys.argv[1]=='install':
		Install()
		print("Finished installation\n")
	elif len(sys.argv)==2 and sys.argv[1]=='uninstall':
		Uninstall()
		print("Finished removing all wmconfig files\n")
	else:
		print("run setup with 'install' or 'uninstall'\n")
