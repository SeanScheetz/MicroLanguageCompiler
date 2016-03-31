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

# Parse_newick Should raise the following ParserException errors when appropriate:
# * Terminating semi-colon missing.
# * Expected label missing.
# * Missing command or ) where expected.
# (You may add others as you see fit.)
#
# Spacing should not matter: "(a,b)c;", and " ( a  ,  b ) c; " should result in idential
# trees.
def parse_newick(ts):
	"""
	Take a newick string and return the corresponding tree object.
	"""
	token_gen = lexer(ts)
	try:
		return T(next(token_gen), token_gen) == "$"
	except ParserException as pe:
		print(pe.msg)
		return False

def T(current, token_gen):
	current = S(current, token_gen)
	if current == ";":
		return next(token_gen)
	else:
		raise ParserException("Terminating semicolon missing.")

#terminal set: a-zA-Z0-9,)(;
#the only possible terminals for S production is \w+ or (
def S(current, token_gen):
	if re.match("\w+", current):
		return next(token_gen)

	if current == "(":
		current = SPrime(next(token_gen), token_gen)
		if current != ")":
			raise ParserException("Missing matching ')'.")

	return S(next(token_gen), token_gen)

def SPrime(current, token_gen):
	if current == ")":
		return current

	while True:
		current = S(current, token_gen)
		if current != ",":
			break

	return current


