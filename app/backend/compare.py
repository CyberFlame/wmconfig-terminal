import difflib, re

ANSI = {"reset":  "\x1b[0m",    # reset everything
        "bold":   "\x1b[1m",    # bold/bright style
        "dim":    "\x1b[2;3m",  # dim or italic style
        "lined":  "\x1b[4m",    # underline
        "blink":  "\x1b[5m",    # blinking style
        "invert": "\x1b[7m",    # invert foreground/backgroung
        "basic":  "\x1b[22m",   # set normal style
        # COLOR CODES
        "black":  "\x1b[30m",   # black color
        "red":    "\x1b[31m",   # red color
        "green":  "\x1b[32m",   # green color
        "yellow": "\x1b[33m",   # yellow color
        "blue":   "\x1b[34m",   # blue color
        "pink":   "\x1b[35m",   # pink/magenta
        "cyan":   "\x1b[36m",   # cyan color
        "white":  "\x1b[37m",   # white color
        "normal": "\x1b[39m"}   # default color

class Color:
	def colorize(*args):
		colors = 0
		strings = 0
		result = []
		for idx, arg in enumerate(args):
			arg = str(arg)
			split = re.split('([A-Z][a-z]+)', arg[1:])
			split = [e.lower() for e in split if e]

			if not [e for e in split if e not in ANSI] and arg.startswith('%'):
				result.append(''.join([ANSI[c] for c in split]))
				colors += 1
			else:
				if colors >= 1 and idx == len(args)-1:
					arg += ANSI['reset']
				result.append(arg)
				strings += 1

		if len(result) < 2:
			return ''.join(result)
		if not strings:
			return tuple(result)

		return ''.join(result)


	def decolorize(string):
		regex = "\x01?\x1b\\[((?:\\d|;)*)([a-zA-Z])\x02?"
		return re.sub(regex, "", str(string))


class Monitor(Color):
	def __init__(self):
		self.color = Color()


	def diff(self, old, new, display=True):
		if not isinstance(old, list):
			old = self.color.decolorize(str(old)).splitlines()
		if not isinstance(new, list):
			new = self.color.decolorize(str(new)).splitlines()

		line_types = {' ': '%Reset', '-': '%Red', '+': '%Green', '?': '%Pink'}
		if display:
			for line in difflib.Differ().compare(old, new):
				if line.startswith('?'):
					continue
				print(self.color.colorize(line_types[line[0]], line))
		return old != new
