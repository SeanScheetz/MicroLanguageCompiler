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
			assign(node.children[0], outfile)
		if node.children[0].label == "READ":
			read_ids(node.children[1], outfile) #node.children[1] will always be <id_list> here
		if node.children[0].label == "WRITE":
			write_ids(node.children[1], outfile) #node.children[1] will always be <expr_list> here

#param: file - file being written to
#param: symbol_table - symbol table being written to .data section of mips output file
#Note: we use .word as the data type being an int is 4 bytes and a word is 4 bytes
def convert_symbol_table(outfile, symbol_table):
	for identifier in symbol_table:
		outfile.write(identifier + ":\t.word\t" + str(symbol_table[identifier]) + "\n")

def start(s, outfile):
	outfile.write("\t.data\n") #start of the data section
	convert_symbol_table(outfile, s) #write symbol table to .data section
	outfile.write("prompt_int:\t.asciiz\t\"Enter an int to store in a variable: \"\n") #user instruction
	outfile.write("sum_stack:\t.word\t0:20\n") #write partial sum to this stack during expression recursion - max 20 recursions
	outfile.write("var_stack:\t.word\t0:20\n") #write variables waiting to be added/subtracted to this stack when recurse - e.g. 4 + (3 + 2) would right 4 to this stack
	outfile.write("address_counter:\t.word\t0\n") #keeps track of where the stack address is for the current recursion
	outfile.write("\n")

	outfile.write("\t.text\n")
	outfile.write("main:\n")

def finish(outfile):
	outfile.close()

def read_ids(node, outfile):
	outfile.write("# Reading values for an <id_list>.\n")
	for child in node.children:
		#prompt user for int
		outfile.write("li\t$v0, 4\n") #4 is the syscall to print a str
		outfile.write("la\t$a0, prompt_int\n") #loads starting address of prompt string into $a0 (arg 0)
		outfile.write("syscall\n")

		#read int
		outfile.write("li\t$v0, 5\n") #5 is the syscall to read an int
		outfile.write("syscall\n") #after syscall, $v0 holds the int read in
		outfile.write("sw\t$v0, " + child.val + "\n\n") #store val in $v0 in the memory allocated to the variable

def write_ids(node, outfile):
	outfile.write("# Writing values of an <expr_list>.\n")
	for child in node.children:
		outfile.write("li\t$v0, 1\n") #1 is the syscall to print an int
		store_expression_result(child, outfile) #stores result of the child expression in $t0
		outfile.write("move\t$a0, $t0\n") #move the expression result (int to be printed) that is in $t0 into $a0 (argument 0)
		outfile.write("syscall\n")

def assign(node, outfile):
	ident = node.children[0].val #children[0] will always be <ident>
	outfile.write("# assign value to " + ident + ".\n")
	store_expression_result(node.children[1], outfile) #children[1] will always be <expression>, stored in $t0
	outfile.write("sw\t$t0, " + ident + "\n\n")

#this is infix from your augmented grammar
#$t0 will accumulate the value (hold the result)
#$t1 will hold the number waiting to be added/subtracted
def store_expression_result(node, outfile):
	outfile.write("li\t$t0, 0\n") #$t0 is going to accumulate the value
	add = True #add the first number
	for child in node.children:
		if child.label == "PRIMARY":
			for primary_child in child.children:
				if primary_child.label == "IDENT":
					outfile.write("lw\t$t1, " + primary_child.val + "\n")
					if add:
						outfile.write("add\t$t0, $t0, $t1" + "\n")
					else: #subtract
						outfile.write("sub\t$t0, $t0, $t1" + "\n")
				if primary_child.label == "INTLIT":
					outfile.write("li\t$t1, " + primary_child.val + "\n")
					if add:
						outfile.write("add\t$t0, $t0, $t1" + "\n")
					else: #subtract
						outfile.write("sub\t$t0, $t0, $t1" + "\n")
				if primary_child.label == "EXPRESSION": #problem with current method is $t8 and $t9 will get over written if more than 1 recursive call
					#save values from current expression call in different variable
					outfile.write("move\t$t0, $t8\n") #$t8 now holds the current sum
					outfile.write("move\t$t1, $t9\n") #$t9 now holds the number waiting to be added 2 (e.g. if we are doing 2 + (1 + 3) then $t1 had 2 in it
					#make recursive expression call
					store_expression_result(primary_child, outfile)
					#reset values and add the value gotten from the recursive call to the value total
		if child.label == "PLUS":
			add = True
		if child.label == "MINUS":
			add = False