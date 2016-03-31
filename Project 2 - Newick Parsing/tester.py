from tree import *

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
	print("---__len__ tests---")
	print("1. correct: 1 | " + str(len(t1)))
	print("2. correct: 4 | " + str(len(t4)))
	print("3. correct: 8 | " + str(len(t8)))

	# str tests
	print("---__str__ tests---")
	print("4. correct: a; | " + str(t1))
	print("5. correct: (a,b,c)d; | " + str(t4))
	print("6. correct: ((a,b,c)d,(e,f)g)h; | " + str(t8))

	# parse_newick tests - valid
	print("---parse newick tests-valid---")
	t = parse_newick("a;")
	print("1. correct: a; | " + str(t))
	t = parse_newick("(a,b,c)d;")
	print("2. correct: (a,b,c)d; | " + str(t))
	t = parse_newick("((a,b,c)d,(e,f)g)h;")
	print("3. correct: ((a,b,c)d,(e,f)g)h; | " + str(t))
	t = parse_newick("ab;")
	print("4. correct: ab; | " + str(t))
	t = parse_newick("(a,bc9)d;")
	print("5. correct: (a,bc9)d; | " + str(t))

	# # parse_newick tests - exceptions
	print("---parse newick tests-exceptions---")
	t = parse_newick("a")
	print("1. correct: No terminating semicolon | " + t)
	t = parse_newick("(a,b,c)d")
	print("2. correct: No terminating semicolon | " + t)
	t = parse_newick("(a,b,cd;")
	print("3. Missing closing ). | " + t)
	t = parse_newick("(a,b)*;")
	print("4. Unrecognized token. | " + t)
	t = parse_newick("(*,b)c;")
	print("5. Unrecognized token. | " + t)
	t = parse_newick("(a,*)c;")
	print("6. Unrecognized token. | " + t)
	t = parse_newick("(a,b);")
	print("7. No parent after set of children - missing label | " + t)
	t = parse_newick("a,b,c,d;")
	print("8. No terminating semicolon. | " + t) # there should be a terminating semi colon after the a in this case
	t = parse_newick("(a,b)d;a")
	print("9. Symbols after terminating semicolon. | " + t)
