# Generator - returns nodes while progressing through a depth first search
# of the tree, t
def traverse_tree(t):
	yield t
	for child in t.children:
		yield from traverse_tree(child)

# generates the .data section - full traversal of the tree
def generate_data(node, s, outfile):
	if node.label == "BEGIN":
		start_data(s, outfile)
	if node.label == "DECLARATION":
		# Mark the variable as declared
		ident = node.children[1].children[0].val
		if s[ident][1] != 0:
			raise SemanticError("Semantic Error: " + ident + " was declared twice.")
		s[ident][1] = 1
		if node.children[0].children[0].label == "INT" or node.children[0].children[0].label == "BOOL":
			allocate_word(node.children[1], s, outfile)
	if node.label == "ASSIGNMENT":
		ident = node.children[0].children[0].val
		try:
			vartype = s[ident][0]
		except:
			raise SemanticError("Semantic Error: Variable used before declaration.")
		if vartype == "STRING":
			allocate_string(node, s, outfile)

def allocate_string(node, s, outfile):
	typ, startnode = get_expression_type(node.children[1], s, outfile)
	if typ != "STRING":
		raise SemanticError("Semantic Error: Expected String, received " + typ)
	newnode = node.children[1].children[0].children[0].children[0].children[0].children[1].children[0]
	if newnode.label == "STRINGLIT":
		outfile.write(node.children[0].val + ":\t.asciiz\t" + newnode.val + "\n")
		s[node.children[0].val][2] = newnode.val
	elif node.children[0].label == "IDENT":
		ident = node.children[1].children[0].children[0].children[0].children[0].children[1].children[0].val
		outfile.write(str(node.children[0].val) + ":\t.asciiz\t" + s[ident][1] + "\n")

# generates the .text section - full traversal of the tree
def generate_text(node, s, outfile):
	if node.label == "BEGIN":
		start_text(s, outfile)
	if node.label == "END":
		finish(outfile)
	if node.label == "STATEMENT":
		if node.children[0].label == "ASSIGNMENT": #depends on solve expression
			assign(node.children[0], s, outfile)
		if node.children[0].label == "READ":
			# node.children[1] will always be <id_list> here
			read_ids(node.children[1], s, outfile)
		if node.children[0].label == "WRITE": #depends on solve expression
			# node.children[1] will always be <expr_list> here
			write_ids(node.children[1], s, outfile)


def start_data(s, outfile):
	outfile.write("\t.data\n")  # start of the data section
	# user instruction
	outfile.write("prompt_int:\t.asciiz\t\"Enter an int to store in a variable: \"\n")

def start_text(s, outfile):
	outfile.write("\n")
	outfile.write("\t.text\n")  # start of the data section

def declaration(node, s, outfile):
	vartype = node.children[0].label.lower()
	ident = node.children[1].val
	s[ident][0] = vartype
	s[ident][1] = 1

def finish(outfile):
	outfile.close()

def allocate_word(node, s, outfile):
	ident = node.children[0].val
	outfile.write(ident + ":\t.word\t0\n")

def read_ids(node, s, outfile):
	outfile.write("# Reading values for an <id_list>.\n")
	for child in node.children:
		# prompt user for int
		outfile.write("li\t\t$v0, 4\n")  # 4 is the syscall to print a str
		# loads starting address of prompt string into $a0 (arg 0)
		outfile.write("la\t\t$a0, prompt_int\n")
		outfile.write("syscall\n")

		# read int
		outfile.write("li\t\t$v0, 5\n")  # 5 is the syscall to read an int
		outfile.write("syscall\n")  # after syscall, $v0 holds the int read in
		# store val in $v0 in the memory allocated to the variable
		outfile.write("sw\t\t$v0, " + child.val + "\n\n")
		s[child.val] = 1


def write_ids(node, s, outfile):
	outfile.write("# Writing values of an <expr_list>.\n")
	for child in node.children:
		#need to change the syscall based on the type that is being printed
		outfile.write("li\t\t$v0, 1\n")  # 1 is the syscall to print an int
		solve_expression(child, s, outfile)
		# move the expression result (int to be printed) that is in $t0 into
		# $a0 (argument 0)
		outfile.write("move\t$a0, $t0\n")
		outfile.write("syscall\n")

		outfile.write("addi\t$a0, $zero, 0xA\n") #ascii code for LF, if you have any trouble try 0xD for CR.
		outfile.write("addi\t$v0, $zero, 0xB\n") #syscall 11 prints the lower 8 bits of $a0 as an ascii character.
		outfile.write("syscall\n")



def get_expression_type(node, s, outfile):
	startnode = node
	if len(node.children) > 1:
		# EXPRESSION node
		return "BOOL", startnode
	else:
		# TERM1 node
		node = node.children[0]
		if len(node.children) > 1:
			return "BOOL", startnode
		else:
			# FACT1 node
			node = node.children[0]
			if node.children[0].label == "NOT":
				return "BOOL", startnode
			elif node.children[1].children[0].label == "RELATIONOP":
				return "BOOL", startnode
			else:
				# EXP2 node
				node = node.children[0]
				if len(node.children) > 1:
					return "INT", startnode
				else:
					node = node.children[0]
					if len(node.children) > 2:
						return "INT", startnode
					else:
						node = node.children[1]
						if node.children[0].label == "IDENT":
							exprtype = s[node.children[0].val][0]
						elif node.children[0].label == "INTLIT":
							exprtype = "INT"
						elif node.children[0].label == "BOOLLIT":
							exprtype = "BOOL"
						elif node.children[0].label == "STRINGLIT":
							exprtype = "STRING"
						else:
							exprtype = get_expression_type(node, s, outfile)
						return exprtype, startnode


def assign(node, s, outfile):
	ident = node.children[0].val  # children[0] will always be <ident>
	if s[ident][1] == 0:
		raise SemanticError(
			"Semantic Error: Use of variable " + ident + " without declaration.")
	vartype = s[ident][0]

	outfile.write("# assign value to " + ident + ".\n")
	# children[1] will always be <expression>
	solve_expression(node.children[1], s, outfile)
	outfile.write("sw\t\t$t0, " + ident + "\n\n")

def solve_expression(node, s, outfile):
	vartype, startnode = get_expression_type(node, s, outfile)
	if vartype == "BOOL":
		solve_bool_expression(node, s, outfile)
	if vartype == "INT":
		solve_int_expression(node, s, outfile)


def solve_bool_expression(node, s, outfile):

	if node.children[0].label == "TERM1":
		#if we see an or then logically or them
		if len(node.children) > 1:
			return solve_bool_expression(node.children[0],s, outfile) or solve_bool_expression(node.children[2], s, outfile)
		else:
			return solve_bool_expression(node.children[0],s, outfile)
	elif node.children[0].label == "FACT1":
		if len(node.children) > 1:
			return solve_bool_expression(node.children[0],s,outfile) and solve_bool_expression(node.children[2],s,outfile)
		else:
			return solve_bool_expression(node.children[0], s , outfile)
	elif node.children[0].label == "NOT":
		return not solve_bool_expression(node.children[1], s , outfile)
	elif node.children[0].label == "EXPR2":
		if node.children[1].children[0].label == "LAMBDA":
			solve_bool_expression(node.children[0], s, outfile)
		elif node.children[1].children[0].label == "RELATIONOP":
			return parseOperator(solve_int_expression(node.children[0], s, outfile), node.children[1].children[0].val, solve_int_expression(node.children[1].children[1], s, outfile))

	elif node.label == "FACT2":
		if node.children[0].label == "IDENT":
			return s[node.children[0].val][1]
		elif node.children[0].label == "BOOLLIT":
			if node.children[0].val =="True":
				return True
			elif node.children[0].val =="False":
				return False
		elif node.children[0].label == "EXPRESSION":
			return solve_bool_expression(node.children[0], s, outfile)
	else:
		raise SemanticError("Semantic Error: Not valid boolean expression.")
		#dont think will happen with parser but cant hurt to throw it i suppose.

#<exp2> -> <term2> { [+|-] <term2> }
#<term2>-> <sign> <fact2> { [*|/|%] <sign> <fact2> }
#<sign> -> - | lambda
#<fact2>-> <ident> | INTLIT | BOOLLIT | STRINGLIT | (<expression>)
#result of solve_int_expression will be solved in $t0
def solve_int_expression(node, s, outfile):
	outfile.write("li\t$t0, 0\n")
	node = node.children[0].children[0].children[0]
	plus = True  # add the first number
	for child in node.children:
		if child.label == "TERM2":
			if plus:
				int_expression_helper(child, s, outfile) #result of this will be in $t2
				outfile.write("add\t$t0, $t0, $t1\n")
			else:
				int_expression_helper(child, s, outfile) #result of this will be in $t2
				outfile.write("sub\t$t0, $t0, $t1\n")
		if child.label == "PLUS":
			plus = True
		if child.label == "MINUS":
			plus = False

# the node in this case is <term2> - this solves *, /, %
# after this function, the value of <term2> is stored in $t1
def int_expression_helper(node, s, outfile):
	arithop = 0 # 0 = multiplication, 1 = division, 2 = modulo
	isNegative = False
	outfile.write("li\t$t1, 0\n") #$t2 will accumulate the result of the <term2> expression

	for i, child in enumerate(node.children):
		if child.label == "SIGN":
			if not child.children[0].label == "LAMBDA":
				isNegative = True

		#add the first real number to the sum -rest of children need to be mult/divide/modulo
		if i == 1:
			solve_fact2(child.children[0], isNegative, s, outfile) #result is in $t2
			outfile.write("add\t$t1, $t1, $t2\n")
			continue

		if child.label == "TIMES":
			arithop = 0

		if child.label == "DIVIDE":
			arithop = 1

		if child.label == "MODULO":
			arithop = 2

		if child.label == "FACT2":
			valnode = child.children[0]
			solve_fact2(valnode, isNegative, s, outfile) #result is in $t2
			if arithop == 0:
				outfile.write("mult\t$t1, $t2\n")
				outfile.write("mflo\t$t1\n")
			elif arithop == 1:
				outfile.write("div\t$t1, $t2\n")
				outfile.write("mflo\t$t1\n")
			else: #arithop ==2
				outfile.write("div\t$t1, $t2\n")
				outfile.write("mfhi\t$t1\n")

#result of fact2 is stored in $t2
def solve_fact2(node, isNegative, s, outfile):
	if node.label == "IDENT":
		outfile.write("lw\t$t2, " + node.val + "\n")

	if node.label == "INTLIT":
		outfile.write("li\t$t2, " + node.val + "\n")

	if node.label == "EXPRESSION":
		# write the current sum and number waiting to be added to the stack pointer $sp
		outfile.write("addi\t$sp, $sp, -4\n")	# -4 because we are going to push 1 word onto the stack
		outfile.write("sw\t\t$t0, 0($sp)\n")	# store a partial sum
		outfile.write("addi\t$sp, $sp, -4\n")	# -4 because we are going to push 1 word onto the stack
		outfile.write("sw\t\t$t1, 0($sp)\n")	# store a partial quotient/product
		# make recursive expression call
		solve_int_expression(node, s, outfile) #sum of the recursive call is in $t0
		outfile.write("move\t$t2, $t0\n") #moves the result of the recursive int expression into $t2
		# restore sum from the stack and increment the stack point
		outfile.write("lw\t$t1, 0($sp)\n")	#$t1 now holds the partial quotient/product from before the recursive call
		outfile.write("addi\t$sp, $sp, 4\n")
		outfile.write("lw\t$t0, 0($sp)\n")	#$t0 now holds the partial sum before the recursive call
		outfile.write("addi\t$sp, $sp, 4\n")
		#4 lines up is basically the return of the function. The partial sum of the result is in $t2

	if isNegative:
		outfile.write("li\t$t6, 0\n") #this is for subtracting our positive number to get a negative version
		outfile.write("sub\t$t2, $t6, $t2\n") #$t2 now holds the negative of the old $t2
	#else $t2 is already correct

class SemanticError(Exception):

	def __init__(self, msg):
		self.msg = msg

	def __str__(self):
		return self.msg

# checks if a var has been initialized
# s is the symbol table


def check_if_var_init(ident, s):
	if not s[ident][1] == 1:
		raise SemanticError("Semantic Error: Attempted to use variable " +
							ident + " without prior initialization.")

def parseOperator(expr1, opString, expr2):
	if opString == "==":
		return expr1 == expr2
	elif opString == "!=":
		return expr1 != expr2
	elif opString == ">=":
		return expr1 >= expr2
	elif opString == "<=":
		return expr1 <= expr2
	elif opString == "<":
		return expr1 < expr2
	elif opString == ">":
		return expr1 > expr2


###############RETIRED FUNCTIONS################

# param: file - file being written to
# param: symbol_table - symbol table being written to .data section of mips output file
# Note: we use .word as the data type being an int is 4 bytes and a word
# is 4 bytes
def convert_symbol_table(outfile, symbol_table):
	for identifier in symbol_table:
		outfile.write(identifier + ":\t.word\t" +
					  str(symbol_table[identifier][1]) + "\n")
