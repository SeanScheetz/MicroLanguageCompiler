import re
import sys

class LexerError(Exception):
	"""
	Exception to be thrown when the lexer encounters a bad token.
	"""
	def __init__(self, msg):
		self.msg = msg

	def __str__(self):
		return str(self.msg)

class Token:
	"""
	A class for storing token information.
	The variable instances for a token object are:
	* t_class: The token class.
	* name: The name of the token.
	* pattern: The specific pattern of the token
	* line: The line containing the token
	* line_num: The line number (numbered from 1)
	* col: The column number (numbered from 0)
	"""

	def __init__(self, t_class, name, pattern, line, line_num, col):
		"""
		Constructor
		"""
		self.t_class = t_class
		self.name = name
		self.pattern = pattern
		self.line = line
		self.line_num = int(line_num)
		self.col = int(col)

	def __str__(self):
		"""
		Defines behavior of the str function on the Token class.
		Prints as a tupple all information except self.line.
		"""
		return str((self.t_class, self.name, self.pattern, self.line_num, self.col))

	def __repr__(self):
		"""
		Defines the behaviour of the repr() function
		on the Token class.
		"""
		return "Token: " + str(self)

	def __eq__(self, other):
		"""
		Defines behaviour of the == operator on the Token class
		"""
		return self.t_class == other.t_class and self.name == other.name and \
			   self.pattern == other.pattern and self.line == other.line and \
			   self.line_num == other.line_num and self.col == other.col


def lexer(source_file, token_file):
	"""
	Input:
	* source_file: file containing the content to be tokenized
	* token_file: token file (see assignment specifications for format)
	Output:
	* A generator that will iteratively return token objects corresponding to the tokens
	  of source_file, throwing a LexerError if it hits a bad token.
	"""
	classes, names, regexs = [], [], []

	definitions = open(token_file, "r")
	for definition in definitions:
		def_arr = definition.split()
		classes.append(def_arr[0])
		names.append(def_arr[1])
		regexs.append(def_arr[2])

	src = open(source_file, "r")
	for linenum, line in enumerate(src, 1): #1 is start index for the enumeration
		startline = line.rstrip() #the full starting line, right whitespace stripped
		line = startline.lstrip() #will be changed as tokens in a line are found
		colnum = len(startline) - len(line)
		while line:
			for index, regex in enumerate(regexs):
				match = re.match(regex, line)
				if match:
					if match.group(1) == "#":
						line = "" #hacky way to move to the next line (ends the while loop, empty string is false)
						break
					token = Token(classes[index], names[index], match.group(1), startline, linenum, colnum)
					yield token
					startline = line[match.end(1):] #used to see how much whitspace is stripped off
					line = startline.lstrip()
					colnum += (match.end(1) - match.start(1)) + (len(startline) - len(line)) #length of match + whitespace before next token
					break




