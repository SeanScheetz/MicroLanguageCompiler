from lexer import lexer
from tree import tree

"""
Parser for the Micro-language.
Grammar:
   <program> -> begin <statement_list> end
   <statement_list> -> <statement>; { <statement; }
   <statement> -> <assign> | read( <id_list> ) | write( <expr_list> )
   <assign> -> <ident> := <expression>
   <id_list> -> <ident> {, <ident>}
   <expr_list> -> <expression> {, <expression>}
   <expression> -> <primary> {<arith_op> <primary>}
   <primary> -> (<expression>) | <ident> | INTLITERAL
   <ident> -> ID
   <arith_op> -> + | -
"""


class ParserError(Exception):
	def __init__(self, msg):
		self.msg = msg

	def __str__(self):
		return self.msg


#######################################
# Parsing code
def getTokenLineInfo(token):
	return  " - line_num: " + str(token.line_num) + " col: " + str(token.col)

def parser(source_file, token_file):
	"""
	source_file: A program written in the ML langauge.
	returns True if the code is syntactically correct.
	Throws a ParserError otherwise.
	"""

	G = lexer(source_file, token_file)
	try:
		tree = PROGRAM(next(G), G)
		try:
			next(G) #at this point the source should have no more tokens - if the iterator has more, then it is actually a ParserError
			raise ParserError("Tokens exist after END keyword.")
		except StopIteration:
			return tree
	except ParserError as e:
		raise e
	except StopIteration:
		raise ParserError("Program ends before END token")

def PROGRAM(current, G):
	t = tree("PROGRAM")
	if current.name == "BEGIN":
		t.children.append(tree("BEGIN"))
		current, child = STATEMENT_LIST(next(G), G) #the returned child is the STATEMENT_LIST tree
		t.children.append(child)
		if current.name == "END":
			t.children.append(tree("END"))
			return t
		else:
			raise ParserError("Statement list complete, but no END token to signal end of program" + getTokenLineInfo(current))

	else:
		raise ParserError("Program doesn't begin with BEGIN" + getTokenLineInfo(current))

def STATEMENT_LIST(current, G):
	t = tree("STATEMENT_LIST")
	current, child = STATEMENT(current, G) # Child is the STATEMENT tree
	t.children.append(child)
	if current.name != "SEMICOLON":
		raise ParserError("Statement doesn't end with a semicolon" + getTokenLineInfo(current))
	current = next(G)
	while current.name != "END":
		current, child = STATEMENT(current, G) #needs to return a semicolon for a valid statement
		t.children.append(child)
		if current.name != "SEMICOLON":
			raise ParserError("Statement doesn't end with a semicolon" + getTokenLineInfo(current))
		current = next(G)
	return current, t

def STATEMENT(current, G):
	t = tree("STATEMENT")
	if current.name == "ID":
		current, child = ASSIGNMENT(current, G) #make sure ASSIGNMENT is returning next(G)
		t.children.append(child)
		return current, t #current should be a ;

	elif current.name == "READ":
		t.children.append(tree("READ"))
		current = next(G)
		if not current.name == "LPAREN":
			raise ParserError("READ token is not followed by a (" + getTokenLineInfo(current))
		current, child = ID_LIST(next(G), G) #should be returning a )
		t.children.append(child) #child should be the ID_LIST tree
		if not current.name == "RPAREN":
			raise ParserError("Missing closing ) in READ statement" + getTokenLineInfo(current))
		return next(G), t  #next(G) should be a ;

	elif current.name == "WRITE":
		t.children.append(tree("WRITE"))
		current = next(G)
		if not current.name == "LPAREN":
			raise ParserError("WRITE token is not followed by a (" + getTokenLineInfo(current))
		current, child = EXPR_LIST(next(G), G) #should be returning a )
		t.children.append(child)
		if not current.name == "RPAREN":
			raise ParserError("Missing closing ) in WRITE statement" + getTokenLineInfo(current))
		return next(G), t  #next(G) should be a ;

	else:
		raise ParserError("Inappproriate token to start a statement" + getTokenLineInfo(current))

def ASSIGNMENT(current, G):
	t = tree("ASSIGNMENT")
	current, child = IDENT(current, G) #should return a :=
	t.children.append(child)
	if not current.name == "ASSIGNOP":
		raise ParserError("Assignment operator does not follow identifer in assignment statement" + getTokenLineInfo(current))
	current, child = EXPRESSION(next(G), G) # should return something that follows expression - we will check for it in whereever this function returns
	t.children.append(child) #child should be EXPRESSION tree
	return current, t

def ID_LIST(current, G):
	t = tree("ID_LIST")
	current, child = IDENT(current, G)
	t.children.append(child)
	while current.name == "COMMA":
		current = next(G)
		current, child = IDENT(current, G)
		t.children.append(child)
	return current, t # should return a )

def EXPR_LIST(current, G):
	t = tree("EXPR_LIST")
	current, child = EXPRESSION(current, G)
	t.children.append(child)
	while current.name == "COMMA":
		current = next(G)
		current, child = EXPRESSION(current, G)
		t.children.append(child)
	return current, t # should return a ; (if called from ASSIGNMENT) or return ) (if called from STATEMENT)

def IDENT(current, G):
	t = tree("IDENT")
	if not current.name == "ID":
		raise ParserError("Invalid identifier" + getTokenLineInfo(current))
	# when we are actually building the tree we will need to parse the ID here/store it in the symbol table here
	t.children.append(tree("ID"))
	return next(G), t

def EXPRESSION(current, G):
	t = tree("EXPRESSION")
	current, child = PRIMARY(current, G) #should return something in { "," , ; , ) , + , - }
	t.children.append(child)
	while current.t_class == "ARITHOP": # loop until what is returned is not an arithop (we are chaining expressions e.g. (1+2)+12-13 etc.
		current, child = ARITH_OP(current, G)
		t.children.append(child)
		current, child = PRIMARY(current, G)
		t.children.append(child)
	return current, t #current should be in { "," , ; , ) } - ";" gets checked in STATEMENT_LIST, "," gets checked in EPRS_LIST, and ) gets checked in STATEMENT

def PRIMARY(current, G):
	t = tree("PRIMARY")
	if current.name == "LPAREN":
		current, child = EXPRESSION(next(G), G)
		t.children.append(child)
		if not current.name == "RPAREN":
			raise ParserError("Expression not followed by matching ')' (in primary function)" + getTokenLineInfo(current))
		return next(G), t # should return something in {"," , ; , ) , + , -}

	elif current.name == "ID":
		current, child = IDENT(current, G) #IDENT processes the ID and returns next token
		t.children.append(child)
		return current, t # should return something in {"," , ; , ) , + , -}

	elif current.name == "INTLIT":
		# process the INTLIT here when building tree before returning the next (G)
		t.children.append(tree("INTLIT"))
		return next(G), t # should return something in {"," , ; , ) , + , -}

	else:
		raise ParserError("Inappropriate starting token in primary" + getTokenLineInfo(current))

#the tree form for this one is different than the others because your tests skipped the ARITH_OP nodes and went
#straight to the "PLUS" "MINUS" options
#to add the ARITH_OP node add t = tree("ARITH_op") at the top and then append children to that tree in the ifs
def ARITH_OP(current, G):
	# process the ARITHOP here when building tree before returning the next (G)
	if current.name == "PLUS":
		return next(G), tree("PLUS")
	if current.name == "MINUS":
		return next(G), tree("MINUS")
	else: #this should never happen because only way to get to this function is if current is an arith op
		raise ParserError("Invalid ARITH_OP" + getTokenLineInfo(current))