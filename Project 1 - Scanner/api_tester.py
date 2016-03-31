"""
api_tester: Checks that your lexer class conforms to the API for my testing.
This *only* checks the API match -- it does not check for correctness.
You could still pass all tests on this and get a 0 for the assignment.
"""
# Last update: 1/30, 1:20 AM
import re
import lexer
import unittest

def create_file(str_list, file):
	with open(file, "w") as fp:
		fp.write("\n".join(str_list) + "\n")


class LexerTesting(unittest.TestCase):
	"""Four tests to make sure your submission maches the API."""

	def test01_basic(self):
		"""Test to make sure this works on a simple, one line file, using the tokens.txt token file."""
		L = ["begin"]
		file = "test.txt"
		token_file = "tokens.txt"
		create_file(L, file)
		G = lexer.lexer(file, token_file)
		self.assertTrue(next(G) == lexer.Token("RESERVED", "BEGIN", "begin", "begin", 1, 0))

	def test02_StopIteration(self):
		"""Makes sure next(G) throws a StopIteration excpetion if done.  (This should happen automatically
		if you used yield."""
		L = ["begin"]
		file = "test.txt"
		token_file = "tokens.txt"
		create_file(L, file)
		G = lexer.lexer(file, token_file)
		next(G)
		with self.assertRaises(StopIteration):
			next(G)

	def test03_LexerError(self):
		"""Makes sure next(G) throws a LexerError exception if it hits a bad token."""
		L = ["ab%cd"]
		file = "test.txt"
		token_file = "tokens.txt"
		create_file(L, file)
		G = lexer.lexer(file, token_file)
		next(G)
		with self.assertRaises(lexer.LexerError):
			next(G)

	def test04_LexerError2(self):
		"""Makes sure next(G) throws an error message containing the strings "line x"
		and "column y", where x and y are the line and column numbers of the first character
		of the bad token.  (Line numbers counted from 1; column numbers counted from 0.)"""
		L = ["ab%cd"]
		file = "test.txt"
		token_file = "tokens.txt"
		create_file(L, file)
		G = lexer.lexer(file, token_file)
		next(G)
		try:
			l = next(G)
		except lexer.LexerError as e:
			r1 = re.search("line \d+", str(e))
			r2 = re.search("col(umn)?\s+\d+", str(e))
			self.assertTrue(r1 != None and r2 != None)
		else:
			self.assertTrue(False)   # No exception was thrown.

def run_tests():
	suite = unittest.TestLoader().loadTestsFromTestCase(LexerTesting)
	testResult = unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
	run_tests()