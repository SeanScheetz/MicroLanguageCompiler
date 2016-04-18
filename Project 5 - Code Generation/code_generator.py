#param: file - file being written to
#param: symbol_table - symbol table being written to .data section of mips output file
#Note: we use .word as the data type being an int is 4 bytes and a word is 4 bytes
def convert_symbol_table(outfile, symbol_table):
	for identifier in symbol_table:
		outfile.write(identifier + ":\t.word\t" + str(symbol_table[identifier]) + "\n")
	outfile.write("\n")

#Generator - returns nodes while progressing through a depth first search of the tree, t
def traverse_tree(t):
	yield t
	for child in t.children:
		yield from traverse_tree(child)

def generate_code(node, outfile):
	if node.label == "BEGIN":
		start(outfile)
	if node.label == "END":
		finish(outfile)
	if node.label == "STATEMENT":
		if node.children[0].label == "ASSIGNMENT":
			assign(node.children[0], outfile)
		if node.children[0].label == "READ":
			read_ids(node.children[1], outfile) #node.children[1] will always be <id_list> here
		if node.children[0].label == "WRITE":
			write_ids(node.children[1], outfile) #node.children[1] will always be <expr_list> here

def start(outfile):
	outfile.write(".text\n")
	outfile.write("main:\n")

def finish(outfile):
	outfile.close()

def read_ids(node, outfile):
	for child in node.children:
		outfile.write("li\t$v0, 5\n") #5 is the syscall to read an int
		outfile.write("syscall\n") #after syscall, $v0 holds the int read in
		outfile.write("sw\t$v0, " + child.val + "\n") #store val in $v0 in the memory allocated to the variable

def write_ids(node, outfile):
	for child in node.children:
		outfile.write("li\t$v0, 1\n") #1 is the syscall to print an int
		store_expression_result(child, outfile) #stores result of the child expression in $t0
		outfile.write("move\t$a0, $t0\n") #move the expression result (int to be printed) that is in $t0 into $a0 (argument 0)
		outfile.write("syscall\n")

def assign(node, outfile):
	ident = node.children[0].val #children[0] will always be <ident>
	store_expression_result(node.children[1], outfile) #children[1] will always be <expression>, stored in $t0
	outfile.write("sw\t$t0, " + ident + "\n")

#stores the result of the expression in $t0 !!!
#this is infix from your augmented grammar
def store_expression_result(node, outfile):
	outfile.write("li\t$t0, 0") #$t1 is going to accumulate the value
	for child in node.children:
		if node.label == "PRIMARY": #if we need to recursively call store_expression_result write off the current values
			for primary_child in child:
				if primary_child.label == "IDENT":
					outfile.write("sw\t$t1, " + primary_child.val)
				if primary_child.label == "INTLIT":
					outfile.write("li\t$t1, " + primary_child.val)
				if primary_child.label == "EXPRESSION": #problem with current method is $t8 and $t9 will get over written if more than 1 recursive call
					#save values from current expression call in different variable
					outfile.write("move\t$t0, $t8") #$t8 now holds the current sum
					outfile.write("move\t$t1, $t9") #$t9 now holds the number waiting to be added 2 (e.g. if we are doing 2 + (1 + 3) then $t1 had 2 in it
					#make recursive expression call
					store_expression_result(primary_child, outfile)
					#reset values and add the value gotten from the recursive call to the value total
		if node.label == "PLUS":
			outfile.write("add\t$t0, $t0, $t1")
		if node.label == "MINUS":
			outfile.write("sub\t$t0, $t0, $t1")