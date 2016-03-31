from tree import *
import re

if __name__ == "__main__":
	t1 = tree("a")                 # a;
	t2 = tree("b")                 # b;
	t3 = tree("c")                 # c;
	t4 = tree("d", [t1, t2, t3])   # (a,b,c)d;
	t5 = tree("e")                 # e;
	t6 = tree("f")                 # f;
	t7 = tree("g", [t5, t6])       # (e,f)g;
	t8 = tree("h", [t4, t7])       # ((a,b,c)d,(e,f)g)h;

	# len tests
	print(len(t1)) # correct: 1
	print(len(t4)) # correct: 4
	print(len(t8)) # correct: 8

	# str tests
	print(str(t1)) # correct: a;
	print(str(t4)) # correct: (a,b,c)d;
	print(str(t8)) # correct: ((a,b,c)d,(e,f)g)h;

	# parse_newick tests - valid
	t = parse_newick("a;")
	print(t) # correct: a;
	t = parse_newick("(a,b,c)d;")
	print(t) # correct: (a,b,c)d;
	t = parse_newick("((a,b,c)d,(e,f)g)h;")
	print(t) # correct: ((a,b,c)d,(e,f)g)h;
	t = parse_newick("ab;")
	print(t) # correct: ab;
	t = parse_newick("(a,bc9)d;")
	print(t) # correct: (a,bc9)d;

	# parse_newick tests - exceptions
	t = parse_newick("a")
	print(t) # correct: Terminating semicolon missing.
	t = parse_newick("(a,b,c)d")
	print(t) # correct: Terminating semicolon missing.
	t = parse_newick("(a,b,cd;")
	print(t) # correct: Missing closing ')'


