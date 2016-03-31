from tree2 import *

if __name__ == "__main__":
	t1 = tree2("a")                 # a;
	t2 = tree2("b")                 # b;
	t3 = tree2("c")                 # c;
	t4 = tree2("d", [t1, t2, t3])   # (a,b,c)d;
	t5 = tree2("e")                 # e;
	t6 = tree2("f")                 # f;
	t7 = tree2("g", [t5, t6])       # (e,f)g;
	t8 = tree2("h", [t4, t7])       # ((a,b,c)d,(e,f)g)h;

	# len tests
	print(len(t1)) # correct: 1
	print(len(t4)) # correct: 4
	print(len(t8)) # correct: 8

	# str tests
	print(str(t1)) # correct: a;
	print(str(t4)) # correct: (a,b,c)d;
	print(str(t8)) # correct: ((a,b,c)d,(e,f)g)h;

	# parse_newick tests - valid
	# t = parse_newick("a;")
	# print(t) # correct: a;
	t = parse_newick("(a,b,c)d;")
	print(t) # correct: (a,b,c)d;
	# t = parse_newick("((a,b,c)d,(e,f)g)h;")
	# print(t) # correct: ((a,b,c)d,(e,f)g)h;
	# t = parse_newick("ab;")
	# print(t) # correct: ab;
	# t = parse_newick("(a,bc9)d;")
	# print(t) # correct: (a,bc9)d;
	#
	# # parse_newick tests - exceptions
	# t = parse_newick("a")
	# print(t) # correct: Terminating semicolon missing.
	# t = parse_newick("(a,b,c)d")
	# print(t) # correct: Terminating semicolon missing.
	# t = parse_newick("(a,b,cd;")
	# print(t) # correct: Missing closing ')'
	# t = parse_newick("(a,b)*;")
	# print(t) # correct: token not in terminal set
	# t = parse_newick("(*,b)c;")
	# print(t) # correct: token not in terminal set
	# t = parse_newick("(a,*)c;")
	# print(t) # correct: token not in terminal set
	# t = parse_newick("(a,b);")
	# print(t) # correct: missing label
	# t = parse_newick("a,b,c,d;")
	# print(t) # correct: missing label
	# t = parse_newick("(a,b)d;a")
	# print(t) # correct: Symbols after terminating semicolon
