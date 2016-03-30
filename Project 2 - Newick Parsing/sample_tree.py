"""
A set of sample trees.  Provided for help with testing.
Last updated: 1/5/16, 4:20 PM
"""
from tree import *

t1 = tree("a")                 # a;
t2 = tree("b")                 # b;
t3 = tree("c")                 # c;
t4 = tree("d", [t1, t2, t3])   # (a,b,c)d;
t5 = tree("e")                 # e;
t6 = tree("f")                 # f;
t7 = tree("g", [t5, t6])       # (e,f)g;
t8 = tree("h", [t4, t7])       # ((a,b,c)d,(e,f)g)h;
