# Generator - returns nodes while progressing through a depth first search
# of the tree, t


def traverse_tree(t):
	yield t
	for child in t.children:
		yield from traverse_tree(child)

# generates the .data section - full traversal of the tree
def generate_data(node, s, outfile, stringLitDict):
	if node.label == "DECLARATION":
		# Mark the variable as declared
		ident = node.children[1].children[0].val
		if s[ident][1] != 0:
			raise SemanticError("Semantic Error: " + ident + " was declared twice.")
		s[ident][1] = 1
		if node.children[0].children[0].label == "INT" or node.children[0].children[0].label == "BOOL":
			allocate_word(node.children[1], s, outfile)
	if node.label == "STATEMENT":
		if node.children[0].label == "WRITE":
			check_for_stringlits(node.children[1], s, outfile, stringLitDict)
	if node.label == "ASSIGNMENT":
		ident = node.children[0].children[0].val
		try:
			vartype = s[ident][0]
		except:
			raise SemanticError("Semantic Error: Variable used before declaration.")
		if vartype == "STRING":
			allocate_string_ident(node, s, outfile)

#allocates space in .data for an identifier to a string constant
def allocate_string_ident(node, s, outfile):
	vartype = get_expression_type(node.children[1], s, outfile)
	if vartype != "STRING":
		raise SemanticError("Semantic Error: Expected String, received " + vartype)
	string_lit = node.children[1].children[0].children[0].children[0].children[0].children[1].children[0].val
	if node.children[0].label == "IDENT":
		outfile.write(str(node.children[0].val) + ":\t.asciiz\t" + string_lit + "\n")

def check_for_stringlits(node, s, outfile, stringLitDict):
	for child in node.children:
		vartype = get_expression_type(child, s, outfile)
		if vartype == "STRING":
			string_val = child.children[0].children[0].children[0].children[0].children[1].children[0].val
			outfile.write("string" + str(len(stringLitDict)) + ":\t.asciiz\t" + string_val + "\n")
			stringLitDict[string_val] = "string" + str(len(stringLitDict))

# generates the .text section - full traversal of the tree
def generate_text(node, s, outfile, stringLitDict, programCountDict, ifWhileStack):
	if node.label == "END":
		if ifWhileStack[-1] == -1:
			outfile.close()
		elif ifWhileStack[-1] == 0:
			finish_while(outfile, programCountDict, ifWhileStack)
		elif ifWhileStack[-1] == 1:
			finish_if(outfile, programCountDict, ifWhileStack)
		elif ifWhileStack[-1] == 2:
			finish_if_else(outfile, programCountDict, ifWhileStack)
	if node.label == "STATEMENT":
		if node.children[0].label == "ASSIGNMENT": #depends on solve expression
			assign(node.children[0], s, outfile)
		if node.children[0].label == "READ":
			# node.children[1] will always be <id_list> here
			read_ids(node.children[1], s, outfile)
		if node.children[0].label == "WRITE": #depends on solve expression
			# node.children[1] will always be <expr_list> here
			write_ids(node.children[1], s, outfile, stringLitDict)
		if node.children[0].label == "IF":
			if get_expression_type(node.children[1], s, outfile) == "BOOL":
				if len(node.children) > 4:
					ifWhileStack.append(2) #2 is for ifelse statements
					start_if_else(node, s, outfile, programCountDict)
				else:
					ifWhileStack.append(1) #1 is for if statement
					start_if(node, s, outfile, programCountDict)
			else:
				raise SemanticError("Semantic Error: Non-bool expression for if condition.")
		if node.children[0].label == "WHILE":
			if get_expression_type(node.children[1], s, outfile) == "BOOL":
				ifWhileStack.append(0) #0 is for while statement
				start_while(node, s, outfile, programCountDict)
			else:
				raise SemanticError("Semantic Error: Non-bool expression for while loop condition.")

def declaration(node, s, outfile):
	vartype = node.children[0].label.lower()
	ident = node.children[1].val
	s[ident][0] = vartype
	s[ident][1] = 1

def finish_while(outfile, programCountDict, ifWhileStack):
	ifWhileStack.pop()
	outfile.write("\n")
	outfile.write("j\tlabel" + str(programCountDict["count"]) + "\n")
	outfile.write("out" + str(programCountDict["count"]) + ":\n")
	programCountDict["count"] -= 1
	if programCountDict["count"] == programCountDict["check"]:
		programCountDict["count"] = programCountDict["total"]
		programCountDict["check"] = programCountDict["total"]

def finish_if(outfile, programCountDict, ifWhileStack):
	ifWhileStack.pop()
	outfile.write("\n")
	outfile.write("out" + str(programCountDict["count"]) + ":\n")
	programCountDict["count"] -= 1
	if programCountDict["count"] == programCountDict["check"]:
		programCountDict["count"] = programCountDict["total"]
		programCountDict["check"] = programCountDict["total"]

def finish_if_else(outfile, programCountDict, ifWhileStack):
	ifWhileStack.pop()
	outfile.write("\n")
	outfile.write("out" + str(programCountDict["count"]) + ":\n")
	programCountDict["count"] -= 1
	if programCountDict["count"] == programCountDict["check"]:
		programCountDict["count"] = programCountDict["total"]
		programCountDict["check"] = programCountDict["total"]

def start_if(node, s, outfile, programCountDict):
	programCountDict["count"] += 1
	programCountDict["total"] += 1
	outfile.write("# starting if statement\n")
	solve_bool_expression(node.children[1], s, outfile) #puts result in $t6
	outfile.write("li\t$t0, 1\n")  # for comparing with result in $t6
	outfile.write("bne\t$t0, $t6, out" + str(programCountDict["count"]) + "\n")  # if $t6 did not return true (1)

def start_if_else(node, s, outfile, programCountDict):
	programCountDict["count"] += 1
	programCountDict["total"] += 1
	outfile.write("# starting if else statement\n")
	solve_bool_expression(node.children[1], s, outfile)  # puts result in $t6
	outfile.write("li\t$t0, 1\n")  # for comparing with result in $t6
	outfile.write("bne\t$t0, $t6, out" + str(programCountDict["count"]) + "\n")  # if $t6 did not return true (1)
	outfile.write("j\tout" + str(programCountDict["count"]) + "\n")

def start_while(node, s, outfile, programCountDict): #node is the statement node containing the expression and the sub program
	outfile.write("#Starting while loop\n")
	programCountDict["count"] += 1
	programCountDict["total"] += 1
	outfile.write("label" + str(programCountDict["count"]) + ":\n")
	solve_bool_expression(node.children[1], s, outfile) #puts result in $t6
	outfile.write("li\t$t0, 1\n") #for comparing with result in $t6
	outfile.write("bne\t$t0, $t6, out" + str(programCountDict["count"]) + "\n") #if $t6 did not return true (1)

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


def write_ids(node, s, outfile, stringLitDict):
	outfile.write("# Writing values of an <expr_list>.\n")
	for child in node.children:
		vartype = get_expression_type(child, s, outfile)

		if vartype == "INT":
			outfile.write("# Writing an integer expression\n")
			outfile.write("li\t\t$v0, 1\n")  # 1 is the syscall to print an int
			solve_expression(child, s, outfile)
			# move the expression result (int to be printed) that is in $t0 into
			# $a0 (argument 0)
			outfile.write("move\t$a0, $t0\n")
			outfile.write("syscall\n")
		elif vartype == "BOOL": #eventually make this print true or false instead of 1 or 0
			outfile.write("# Writing a bool expression\n")
			outfile.write("li\t\t$v0, 1\n")  # 1 is the syscall to print an int
			solve_expression(child, s, outfile) #$t6 will hold the result - will be 0 or 1
			outfile.write("move\t$a0, $t6\n")
			outfile.write("syscall\n")
		else: #vartype == "STRING"
			outfile.write("# Writing a string expression\n")
			outfile.write("li\t\t$v0, 4\n")  # 4 is the syscall to print a string
			string_node = child.children[0].children[0].children[0].children[0].children[1].children[0]
			if string_node.label == "IDENT":
				outfile.write("la\t$a0, " + string_node.val + "\n")
				outfile.write("syscall\n")
			else: #string_node.label == "STRINGLIT"
				label = stringLitDict[string_node.val]
				outfile.write("la\t$a0, " + label + "\n")
				outfile.write("syscall\n")

		outfile.write("addi\t$a0, $zero, 0xA\n") #ascii code for LF, if you have any trouble try 0xD for CR.
		outfile.write("addi\t$v0, $zero, 0xB\n") #syscall 11 prints the lower 8 bits of $a0 as an ascii character.
		outfile.write("syscall\n")

def get_expression_type(node, s, outfile):
	if node.label == "EXPRESSION":
		if len(node.children) > 1:
			for child in node.children:
				if child.label == "TERM1":
					if get_expression_type(child, s, outfile) != "BOOL":
						raise SemanticError("Semantic Error: Non boolean expressions with 'OR's")
			return "BOOL"
		else:
			return get_expression_type(node.children[0], s, outfile) #node.children[0] is a <term1> node

	if node.label == "TERM1":
		if len(node.children) > 1:
			for child in node.children:
				if child.label == "FACT1":
					if get_expression_type(child, s, outfile) != "BOOL":
						raise SemanticError("Semantic Error: Non boolean expressions with 'AND's")
			return "BOOL"
		else:
			return get_expression_type(node.children[0], s, outfile) #node.children[0] is a <fact1> node

	if node.label == "FACT1":
		if node.children[0].label == "NOT":
			if get_expression_type(node.children[1], s, outfile) != "BOOL":
				raise SemanticError("Semantic Error: Tried to not a nonbool expression")
			return "BOOL"
		elif node.children[1].children[0].label == "RELATIONOP":
			if get_expression_type(node.children[1].children[1], s, outfile) != "INT" or get_expression_type(node.children[0], s, outfile) != "INT":
				raise SemanticError("Semantic Error: Used a non int expression with a relation op")
			return "BOOL"
		else:
			return get_expression_type(node.children[0], s, outfile) #node.children[0] is an <expr2> node

	if node.label == "EXP2":
		if len(node.children) > 1:
			for child in node.children:
				if child.label == "TERM2":
					if get_expression_type(child, s, outfile) != "INT":
						raise SemanticError("Semantic Error: Tried to add/sub non int expressions")
			return "INT"
		else:
			return get_expression_type(node.children[0], s, outfile) #node.children[0] is a <term2> node

	if node.label == "TERM2":
		if len(node.children) > 2:
			for child in node.children:
				if child.label == "FACT2":
					if get_expression_type(child, s, outfile) != "INT":
						raise SemanticError("Semantic Error: Tried to mult/div/mod non int expressions")
			return "INT"
		elif node.children[0].children[0].label == "MINUS":
			if get_expression_type(node.children[1].children[0], s, outfile) != "INT":
				raise SemanticError("Semantic Error: Tried to use unary negation with non int expression")
			return "INT"
		else:
			return get_expression_type(node.children[1], s, outfile) #node.chbildren[1] is a <fact2> node

	if node.label == "FACT2":
			if node.children[0].label == "INTLIT":
				return "INT"
			elif node.children[0].label == "BOOLLIT":
				return "BOOL"
			elif node.children[0].label == "STRINGLIT":
				return "STRING"
			elif node.children[0].label == "IDENT":
				return s[node.children[0].val][0]
			else: #node.children[0].label == "EXPRESSION"
				return get_expression_type(node.children[0], s, outfile)

def assign(node, s, outfile):
	ident = node.children[0].val  # children[0] will always be <ident>
	if s[ident][1] == 0:
		raise SemanticError("Semantic Error: Use of variable " + ident + " without declaration.")
	vartype = s[ident][0]

	if vartype != "STRING":
		outfile.write("# assign value to " + ident + ".\n")
		# children[1] will always be <expression>
		solve_expression(node.children[1], s, outfile)
		if vartype == "INT":
			outfile.write("sw\t\t$t0, " + ident + "\n\n")
		else: #vartype == "STRING"
			outfile.write("sw\t\t$t6, " + ident + "\n\n")

def solve_expression(node, s, outfile):
	vartype = get_expression_type(node, s, outfile)
	if vartype == "BOOL":
		solve_bool_expression(node, s, outfile)
	if vartype == "INT":
		solve_int_expression(node, s, outfile)

#result of bool expression with be in $t6
def solve_bool_expression(node, s, outfile):
	outfile.write("li\t$t6, 0\n")
	for child in node.children:
		if child.label == "TERM1":
			solve_term1(child, s, outfile) #stored in $t7
			outfile.write("or\t$t6, $t6, $t7\n")

#result is stored in $t7
def solve_term1(node, s, outfile):
	outfile.write("li\t$t7, 1\n")
	for child in node.children:
		if child.label == "FACT1":
			solve_fact1(child, s, outfile) #stored in $t8
			outfile.write("and\t$t7, $t7, $t8\n")

#result $t8
def solve_fact1(node, s, outfile):
	if node.children[0].label == "NOT":
		outfile.write("li\t$t8, -1\n")
		solve_fact2_bool(node.children[1], s, outfile) #result in $t9
		outfile.write("xor\t$t8, $t8, $t9\n")
		outfile.write("andi\t$t8, $t8, 1\n")
	if node.children[0].label == "EXP2":
		if node.children[1].children[0].label != "LAMBDA":
			solve_int_expression(node.children[0], s, outfile) #result of expression is in $t0
			outfile.write("move\t$t5, $t0\n") #storing in $t5 while waiting for other expression
			solve_int_expression(node.children[1].children[1], s, outfile) #stores in $t0
			relop = node.children[1].val

			if relop == "==":
				outfile.write("seq\t$t8, $t5, $t0\n")
			elif relop == "!=":
				outfile.write("sne\t$t8, $t5, $t0\n")
			elif relop == ">=":
				outfile.write("sge\t$t8, $t5, $t0\n")
			elif relop == "<=":
				outfile.write("sle\t$t8, $t5, $t0\n")
			elif relop == ">":
				outfile.write("sgt\t$t8, $t5, $t0\n")
			elif relop == "<":
				outfile.write("slt\t$t8, $t5, $t0\n")
		else:
			solve_fact2_bool(node.children[0].children[0].children[1], s, outfile) #result in $t9
			outfile.write("move\t$t8, $t9\n")

# result is stored in $t9
def solve_fact2_bool(node, s, outfile):
	if node.children[0].label == "IDENT":
		outfile.write("lw\t$t9, " + node.children[0].val + "\n")

	elif node.children[0].label == "BOOLLIT":
		if node.children[0].val == "True":
			outfile.write("li\t$t9, 1\n")
		else: #node.children[0].val == "False"
			outfile.write("li\t$t9, 0\n")

	else: #node.children[0].label == "EXPRESSION"
		# write the current sum and number waiting to be added to the stack pointer $sp
		outfile.write("addi\t$sp, $sp, -4\n")  # -4 because we are going to push 1 word onto the stack
		outfile.write("sw\t\t$t6, 0($sp)\n")  # stores OR results
		outfile.write("addi\t$sp, $sp, -4\n")  # -4 because we are going to push 1 word onto the stack
		outfile.write("sw\t\t$t7, 0($sp)\n")  # stores AND results
		outfile.write("addi\t$sp, $sp, -4\n")  # -4 because we are going to push 1 word onto the stack
		outfile.write("sw\t\t$t8, 0($sp)\n")  # stores NOT results
		# make recursive expression call
		solve_bool_expression(node.children[0], s, outfile) #stores bool result in $t6
		outfile.write("move\t$t9, $t6\n")
		# restore sum from the stack and increment the stack point
		outfile.write("lw\t$t8, 0($sp)\n")  # $t8 now holds the NOT results from before the recursive call
		outfile.write("addi\t$sp, $sp, 4\n")
		outfile.write("lw\t$t7, 0($sp)\n")  # $t7 now holds the AND results from before the recursive call
		outfile.write("addi\t$sp, $sp, 4\n")
		outfile.write("lw\t$t6, 0($sp)\n")  # $t6 now holds the OR before the recursive call
		outfile.write("addi\t$sp, $sp, 4\n")

	# 4 lines up is basically the return of the function. The partial sum of the result is in $t2

#<exp2> -> <term2> { [+|-] <term2> }
#<term2>-> <sign> <fact2> { [*|/|%] <sign> <fact2> }
#<sign> -> - | lambda
#<fact2>-> <ident> | INTLIT | BOOLLIT | STRINGLIT | (<expression>)
#result of solve_int_expression will be solved in $t0
def solve_int_expression(node, s, outfile):
	outfile.write("li\t$t0, 0\n")
	if not node.label == "EXP2": #only does this if the <expression> node is what was passed to this function
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


