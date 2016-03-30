class tree:
	"""
	Tree class, where a tree is a label
	with zero or more trees as children
	"""

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
		"""
		Return true/false indicating whether
		the tree is a leaf
		"""
		return len(self.children) == 0



class ParserException(Exception):
	"""
	Exception class for parse_newick
	"""
	def __init__(self, msg):
		self.msg = msg

	def __str__(self):
		return self.msg



# Parse_newick Should raise the following ParserException errors when appropriate:
# * Terminating semi-colon missing.
# * Expected label missing.
# * Missing command or ) where expected.
# (You may add others as you see fit.)
#
# Spacing should not matter: "(a,b)c;", and " ( a  ,  b ) c; " should result in idential
# trees.
def parse_newick(s):
	"""
	Take a newick string and return the corresponding tree object.
	"""
	pass # TODO: Replace this line with function body.


