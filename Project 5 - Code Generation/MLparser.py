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
	:param source_file: A program written in the ML language.
	:param token_file: A file defining the types of tokens in the ML language
	returns True if the code is syntactically correct.
	Throws a ParserError otherwise.
	"""

	G = lexer(source_file, token_file)
	try:
		t, s = PROGRAM(next(G), G)
		try:
			next(G) #at this point the source should have no more tokens - if the iterator has more, then it is actually a ParserError
			raise ParserError("Syntax Error: Tokens exist after END keyword.")
		except StopIteration:
			return t, s
	except ParserError as e:
		raise e
	except StopIteration:
		raise ParserError("Syntax Error: Program ends before END token")

def PROGRAM(current, G):
	t = tree("PROGRAM")
	s = {}
	if current.name == "BEGIN":
		t.children.append(tree("BEGIN"))
		current, child, s1 = STATEMENT_LIST(next(G), G) #the returned child is the STATEMENT_LIST tree
		t.children.append(child)
		s.update(s1)
		if current.name == "END":
			t.children.append(tree("END"))
			return t, s
		else:
			raise ParserError("Syntax Error: Statement list complete, but no END token to signal end of program" + getTokenLineInfo(current))

	else:
		raise ParserError("Syntax Error: Program doesn't begin with BEGIN" + getTokenLineInfo(current))

def STATEMENT_LIST(current, G):
	t = tree("STATEMENT_LIST")
	s = {}
	current, child, s1 = STATEMENT(current, G) # Child is the STATEMENT tree
	t.children.append(child)
	s.update(s1)
	if current.name != "SEMICOLON":
		raise ParserError("Syntax Error: Statement doesn't end with a semicolon" + getTokenLineInfo(current))
	current = next(G)
	while current.name != "END":
		current, child, s1 = STATEMENT(current, G) #needs to return a semicolon for a valid statement
		t.children.append(child)
		s.update(s1)
		if current.name != "SEMICOLON":
			raise ParserError("Syntax Error: Statement doesn't end with a semicolon" + getTokenLineInfo(current))
		current = next(G)
	return current, t, s

def STATEMENT(current, G):
	t = tree("STATEMENT")
	s = {}
	if current.name == "ID":
		current, child, s1 = ASSIGNMENT(current, G) #make sure ASSIGNMENT is returning next(G)
		t.children.append(child)
		s.update(s1)
		return current, t, s #current should be a ;

	elif current.name == "READ":
		t.children.append(tree("READ"))
		current = next(G)
		if not current.name == "LPAREN":
			raise ParserError("Syntax Error: READ token is not followed by a (" + getTokenLineInfo(current))
		current, child, s1 = ID_LIST(next(G), G) #should be returning a )
		t.children.append(child) #child should be the ID_LIST tree
		s.update(s1)
		if not current.name == "RPAREN":
			raise ParserError("Syntax Error: Missing closing ) in READ statement" + getTokenLineInfo(current))
		return next(G), t, s  #next(G) should be a ;

	elif current.name == "WRITE":
		t.children.append(tree("WRITE"))
		current = next(G)
		if not current.name == "LPAREN":
			raise ParserError("Syntax Error: WRITE token is not followed by a (" + getTokenLineInfo(current))
		current, child, s1 = EXPR_LIST(next(G), G) #should be returning a )
		t.children.append(child)
		s.update(s1)
		if not current.name == "RPAREN":
			raise ParserError("Syntax Error: Missing closing ) in WRITE statement" + getTokenLineInfo(current))
		return next(G), t, s  #next(G) should be a ;

	else:
		raise ParserError("Syntax Error: Inappproriate token to start a statement" + getTokenLineInfo(current))

def ASSIGNMENT(current, G):
	t = tree("ASSIGNMENT")
	s = {}
	current, child, s1 = IDENT(current, G) #should return a :=
	t.children.append(child)
	s.update(s1)
	if not current.name == "ASSIGNOP":
		raise ParserError("Syntax Error: Assignment operator does not follow identifier in assignment statement" + getTokenLineInfo(current))
	current, child, s1 = EXPRESSION(next(G), G) # should return something that follows expression - we will check for it in whereever this function returns
	t.children.append(child) #child should be EXPRESSION tree
	s.update(s1)
	return current, t, s

def ID_LIST(current, G):
	t = tree("ID_LIST")
	s = {}
	current, child, s1 = IDENT(current, G)
	t.children.append(child)
	s.update(s1)
	while current.name == "COMMA":
		current = next(G)
		current, child, s1 = IDENT(current, G)
		t.children.append(child)
		s.update(s1)
	return current, t, s # should return a )

def EXPR_LIST(current, G):
	t = tree("EXPR_LIST")
	s = {}
	current, child, s1 = EXPRESSION(current, G)
	t.children.append(child)
	s.update(s1)
	while current.name == "COMMA":
		current = next(G)
		current, child, s1 = EXPRESSION(current, G)
		t.children.append(child)
		s.update(s1)
	return current, t, s # should return a ; (if called from ASSIGNMENT) or return ) (if called from STATEMENT)

def EXPRESSION(current, G):
	t = tree("EXPRESSION")
	s = {}
	current, child, s1 = PRIMARY(current, G) #should return something in { "," , ; , ) , + , - }
	t.children.append(child)
	s.update(s1)
	while current.t_class == "ARITHOP": # loop until what is returned is not an arithop (we are chaining expressions e.g. (1+2)+12-13 etc.
		current, child = ARITH_OP(current, G)
		t.children.append(child)
		current, child, s1 = PRIMARY(current, G)
		t.children.append(child)
		s.update(s1)
	return current, t, s #current should be in { "," , ; , ) } - ";" gets checked in STATEMENT_LIST, "," gets checked in EPRS_LIST, and ) gets checked in STATEMENT

def PRIMARY(current, G):
	t = tree("PRIMARY")
	s = {}
	if current.name == "LPAREN":
		current, child, s1 = EXPRESSION(next(G), G)
		t.children.append(child)
		s.update(s1)
		if not current.name == "RPAREN":
			raise ParserError("Syntax Error: Expression not followed by matching ')' (in primary function)" + getTokenLineInfo(current))
		return next(G), t, s # should return something in {"," , ; , ) , + , -}

	elif current.name == "ID":
		current, child, s1 = IDENT(current, G) #IDENT processes the ID and returns next token
		t.children.append(child)
		s.update(s1)
		return current, t, s # should return something in {"," , ; , ) , + , -}

	elif current.name == "INTLIT":
		t.children.append(tree("INTLIT", val = current.pattern))
		return next(G), t, s # should return something in {"," , ; , ) , + , -}

	else:
		raise ParserError("Syntax Error: Inappropriate starting token in primary" + getTokenLineInfo(current))

def IDENT(current, G):
	t = tree("IDENT")
	s = {current.pattern: 0}
	if not current.name == "ID":
		raise ParserError("Syntax Error: Invalid identifier" + getTokenLineInfo(current))
	t.children.append(tree("ID", val = current.pattern))
	return next(G), t, s

#the tree form for this one is different than the others because your tests skipped the ARITH_OP nodes and went
#straight to the "PLUS" "MINUS" options
#to add the ARITH_OP node add t = tree("ARITH_op") at the top and then append children to that tree in the ifs
#don't need to update symbol table here because it is leaf node and no symbols will be found here
def ARITH_OP(current, G):
	# process the ARITHOP here when building tree before returning the next (G)
	if current.name == "PLUS":
		return next(G), tree("PLUS")
	if current.name == "MINUS":
		return next(G), tree("MINUS")
	else: #this should never happen because only way to get to this function is if current is an arith op
		raise ParserError("Syntax Error: Invalid ARITH_OP" + getTokenLineInfo(current))