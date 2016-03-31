import re

class tree:
	def __init__(self, label, children = None):
		self.label = label
		self.children = children if children is not None else []

	def __str__(self):
		return self.strHelper() + ";"

	def strHelper(self):
		if not self.children:
			return self.label
		newick_string = "("
		for index, child in enumerate(self.children, 1): #starting at 1 saves an add operation per loop
			if index != len(self.children):
				newick_string += child.strHelper() + ","
			else:
				newick_string += child.strHelper()
		newick_string += ")" + self.label
		return newick_string

	def __repr__(self):
		return "Tree: " + str(self)

	def __len__(self):
		count = 1
		for node in self.children:
			count += len(node)
		return count

	def isLeaf(self):
		return len(self.children) == 0



class ParserException(Exception):
	"""
	Exception class for parse_newick
	"""
	def __init__(self, msg):
		self.msg = msg

	def __str__(self):
		return self.msg

# ts is the token stream - in this case just a string and the lexar is yielding 1 char at a time
def lexer(ts):
	for char in re.sub("\s+", "", ts):
		yield char
	yield "$" # End of Input char - states EOI

# terminal set: a-zA-Z0-9,)(;
def parse_newick(ts):
	G = lexer(ts)
	try:
		current, t = T(next(G), G)
		if current != "$":
			raise ParserException("Symbols after teminating semicolon.")
		return t
	except ParserException as pe:
		raise pe #replace "raise pe" with "return pe.msg" to use my tester.py. I had to throw the error for your unit tests to work

def T(current, G):
	if re.match("\w+", current) or current == "(":
		current, t = S(current, G)
		if current != ";":
			raise ParserException("No terminating semicolon.")
	else:
		raise ParserException("Invalid first token.")
	return next(G), t

def S(current, G):
	if re.match("\w+", current):
		label = current
		while True:
			current = next(G)
			if re.match("\w+", current):
				label += current
			else:
				return current, tree(label)

	if current == '(':
		current, children = SLIST(next(G), G)
		if current != ')':
			raise ParserException("Missing closing ).")
		current = next(G)
		if not re.match("\w+", current): # a parent node must come after a set of children
			raise ParserException("No parent after set of children - missing label")
		current, t = S(current, G)
		for child in children:
			t.children.append(child)

	else:
		raise ParserException("S: Unrecognized token")

	return current, t

def SLIST(current, G):
	if current == ')':
		return current, tree("")

	children = []
	while True:
		current, child = S(current, G)
		children.append(child)
		if current != ',':
			break
		current = next(G)

	return current, children