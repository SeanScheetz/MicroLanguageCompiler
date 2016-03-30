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

	# Length Tests
	print(len(t1)) # correct: 1
	print(len(t4)) # correct: 4
	print(len(t8)) # correct: 8

	print(str(t1)) # correct: a;
	print(str(t4)) # correct: (a,b,c)d;
	print(str(t8)) # correct: ((a,b,c)d,(e,f)g)h;