"""
Last updated: 2/5/15, 4:20 PM
"""
from tree import *
import unittest
import re

class api_tester(unittest.TestCase):

	def isTree(self, t):
		"""Check that t is a tree, with the correct interla structure.  (Helper function -- not a unit test.)"""
		if type(t) != tree:
			return False
		if not hasattr(t, "label"):
			return False
		if type(t.label) != str:
			return False
		if not hasattr(t, "children"):
			return False
		if type(t.children) != list:
			return False
		return all([type(c) == tree for c in t.children])

	def test01(self):
		"""Test that a tree has the correct internal structure"""
		t = tree("a", [tree("b"), tree("c")])
		self.assertTrue(self.isTree(t))

	def test02(self):
		"""Test __len__ on a three-node tree."""
		t = tree("a", [tree("b"), tree("c")])
		self.assertEqual(len(t), 3)

	def test03(self):
		"""Test __str__ on a single-node tree."""
		t = tree("a")
		s = str(t)
		self.assertEqual(re.sub("\s+", "", s), "a;")  # Remove spaces and test equality

	def test04(self):
		"""Test parse_newick on a single-node tree representation."""
		s = "a;"
		t = parse_newick(s)
		self.assertTrue(self.isTree(t) and t.label == "a" and t.isLeaf())

	def test05(self):
		"""Test that parse_newick throws the right kind of exception
		when the ; is missing."""
		s = "a"
		with self.assertRaises(ParserException):
			t = parse_newick(s)


def run_tests():
	suite = unittest.TestLoader().loadTestsFromTestCase(api_tester)
	testResult = unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
	unittest.main()

