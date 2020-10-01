#!/usr/bin/python3
import argparse, api

text = '''Backups configuration files and monitors changes in them'''

parser = argparse.ArgumentParser(description=text)
parser.add_argument('-c','--check', action='store_true', help='check system for changes in files')
parser.add_argument('-C','--compare', help='compare file to its backup')
parser.add_argument('-A','--add',  help='add file content to database')
parser.add_argument('-U','--update',  help='update file content in the database')
parser.add_argument('-D','--delete', help='delete file backup')
parser.add_argument('-d', '--display', help='display file content from backup')
parser.add_argument('-V','--version', action='store_true', help='shows version of wmconfig')
parser.add_argument('-r', '--replace', help='replace file in system with saved backup')
args = parser.parse_args()
wmAPI = api.wmApi()

if wmAPI.check_user():
	if args.check:
		wmAPI.check()
	elif args.compare:
		wmAPI.compare(args.compare)
	elif args.add:
		wmAPI.add(args.add)
	elif args.update:
		wmAPI.update(args.update)
	elif args.delete:
		wmAPI.delete(args.delete)
	elif args.display:
		wmAPI.display(args.display)
	elif args.version:
		print("wmconfig version 1.0")
	elif args.replace:
		wmAPI.replace(args.replace)
	else:
		parser.print_help()
else:
	print("Not running as root")
