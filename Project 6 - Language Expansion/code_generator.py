#Generator - returns nodes while progressing through a depth first search of the tree, t
def traverse_tree(t):
	yield t
	for child in t.children:
		yield from traverse_tree(child)

def generate_code(node, s, outfile):
	if node.label == "BEGIN":
		start(s, outfile)
	if node.label == "END":
		finish(outfile)
	if node.label == "STATEMENT":
		if node.children[0].label == "ASSIGNMENT":
			assign(node.children[0], s, outfile)
		if node.children[0].label == "READ":
			read_ids(node.children[1], s, outfile) #node.children[1] will always be <id_list> here
		if node.children[0].label == "WRITE":
			write_ids(node.children[1], s, outfile) #node.children[1] will always be <expr_list> here
		if node.children[0].label == "DECLARATION":
			declaration(node.children[0], s, outfile)

#param: file - file being written to
#param: symbol_table - symbol table being written to .data section of mips output file
#Note: we use .word as the data type being an int is 4 bytes and a word is 4 bytes
def convert_symbol_table(outfile, symbol_table):
	for identifier in symbol_table:
		outfile.write(identifier + ":\t.word\t" + str(symbol_table[identifier][1]) + "\n")

def start(s, outfile):
	outfile.write("\t.data\n") #start of the data section
	convert_symbol_table(outfile, s) #write symbol table to .data section
	outfile.write("prompt_int:\t.asciiz\t\"Enter an int to store in a variable: \"\n") #user instruction
	outfile.write("\n")

	outfile.write("\t.text\n")
	outfile.write("main:\n")

def finish(outfile):
	outfile.close()

def read_ids(node, s, outfile):
	outfile.write("# Reading values for an <id_list>.\n")
	for child in node.children:
		#prompt user for int
		outfile.write("li\t\t$v0, 4\n") #4 is the syscall to print a str
		outfile.write("la\t\t$a0, prompt_int\n") #loads starting address of prompt string into $a0 (arg 0)
		outfile.write("syscall\n")

		#read int
		outfile.write("li\t\t$v0, 5\n") #5 is the syscall to read an int
		outfile.write("syscall\n") #after syscall, $v0 holds the int read in
		outfile.write("sw\t\t$v0, " + child.val + "\n\n") #store val in $v0 in the memory allocated to the variable
		s[child.val] = 1

def write_ids(node, s, outfile):
	outfile.write("# Writing values of an <expr_list>.\n")
	for child in node.children:
		outfile.write("li\t\t$v0, 1\n") #1 is the syscall to print an int
		store_expression_result(child, s, outfile) #stores result of the child expression in $t0
		outfile.write("move\t$a0, $t0\n") #move the expression result (int to be printed) that is in $t0 into $a0 (argument 0)
		outfile.write("syscall\n")

def declaration(node, s, outfile):
	vartype = node.children[0].label.lower()
	ident = node.children[1].val
	s[ident][0] = vartype
	s[ident][1] = 1

def assign(node, s, outfile):
	ident = node.children[0].val #children[0] will always be <ident>
	if s[ident][1] == 0:
		raise SemanticError("Semantic Error: Use of variable " + ident + " without declaration.")
	vartype = s[ident][0]

	outfile.write("# assign value to " + ident + ".\n")
	store_expression_result(node.children[1], s, outfile) #children[1] will always be <expression>, stored in $t0
	outfile.write("sw\t\t$t0, " + ident + "\n\n")

#this is infix from your augmented grammar
#$t0 will accumulate the value (hold the result)
def store_expression_result(node, s, outfile):
	outfile.write("li\t\t$t0, 0\n") #$t0 is going to accumulate the value
	plus = True #add the first number
	for child in node.children:
		if child.label == "PRIMARY":
			for primary_child in child.children:
				if primary_child.label == "IDENT":
					check_if_var_init(primary_child.val, s) #throws error if ident not initialized
					outfile.write("lw\t\t$t1, " + primary_child.val + "\n")
					if plus:
						outfile.write("add\t\t$t0, $t0, $t1\n")
					else: #minus
						outfile.write("sub\t\t$t0, $t0, $t1\n")
				if primary_child.label == "INTLIT":
					outfile.write("li\t\t$t1, " + primary_child.val + "\n")
					if plus:
						outfile.write("add\t\t$t0, $t0, $t1\n")
					else: #minus
						outfile.write("sub\t\t$t0, $t0, $t1\n")
				# ( 1 + (2 + (3 + 4) ) )
				if primary_child.label == "EXPRESSION":
					#write the current sum and number waiting to be added to the stack pointer $sp
					outfile.write("addi\t$sp, $sp, -4\n") #-4 because we are going to push 1 word onto the stack
					outfile.write("sw\t\t$t0, 0($sp)\n") # store the current sum
					#make recursive expression call
					store_expression_result(primary_child, s, outfile)
					#restore sum from the stack and increment the stack point
					outfile.write("lw\t\t$t2, 0($sp)\n")
					outfile.write("addi\t$sp, $sp, 4\n")
					if plus:
						outfile.write("add\t\t$t0, $t0, $t2\n") #add old sum to the result of the recursion expression
					else: #subtract
						outfile.write("sub\t\t$t0, $t2, $t0\n") #sub recursion result from old sum
		if child.label == "PLUS":
			plus = True
		if child.label == "MINUS":
			plus = False


class SemanticError(Exception):
	def __init__(self, msg):
		self.msg = msg

	def __str__(self):
		return self.msg

#checks if a var has been initialized
#s is the symbol table
def check_if_var_init(ident, s):
	if not s[ident][1] == 1:
		raise SemanticError("Semantic Error: Attempted to use variable " + ident + " without prior initialization.")