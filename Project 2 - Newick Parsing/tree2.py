import re

class tree2:
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

# Parse_newick Should raise the following ParserException errors when appropriate:
# * Terminating semi-colon missing.
# * Expected label missing.
# * Missing command or ) where expected.
# (You may add others as you see fit.)
#
# Spacing should not matter: "(a,b)c;", and " ( a  ,  b ) c; " should result in idential
# trees.
# terminal set: a-zA-Z0-9,)(;
def parse_newick(ts):
	"""
	Take a newick string and return the corresponding tree object.
	"""
	G = lexer(ts)
	try:
		current, t = T(next(G), G)
		if current != "$":
			print(current)
			raise ParserException("Symbols after teminating semicolon.")
		return t
	except ParserException as pe:
		return pe.msg

def T(current, G):
	if re.match("\w+", current) or current == "(":
		current, t = S(current, G)
		current = next(G)
		if current != ";":
			raise ParserException("No terminating semicolon.")
	else:
		raise ParserException("Invalid first token.")
	return next(G), t

def S(current, G):
	t = tree2("S")

	if re.match("\w+", current):
		label = current
		while True:
			current = next(G)
			if re.match("\w+", current):
				label += current
			else:
				return current, tree2(label)

	if current == '(':
		current, child = SLIST(next(G), G)
		if current != ')':
			raise ParserException("Missing closing ).")

	else:
		print(current)
		raise ParserException("S: Unrecognized token")

	t.children.append(child)
	return next(G), t

def SLIST(current, G):
	t = tree2("SLIST")
	if current == ')':
		return current, t

	while True:
		current, child = S(current, G)
		t.children.append(child)
		if current != ',':
			break
		current = next(G)

	return current, t