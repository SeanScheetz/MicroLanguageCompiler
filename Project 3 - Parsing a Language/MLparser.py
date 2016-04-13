from lexer import lexer

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
		result = PROGRAM(next(G), G)
		try:
			next(G) #at this point the source should have no more tokens - if the iterator has more, then it is actually a ParserError
			raise ParserError("Tokens exist after END keyword.")
		except StopIteration:
			return True
		return result
	except ParserError as e:
		raise e
	except StopIteration as e:
		raise ParserError("Program ends before END token")

def PROGRAM(current, G):
	if current.name == "BEGIN":
		current = STATEMENT_LIST(next(G), G)
		if current.name == "END":
			return True
		else:
			raise ParserError("Statement list complete, but no END token to signal end of program" + getTokenLineInfo(current))

	else:
		raise ParserError("Program doesn't begin with BEGIN" + getTokenLineInfo(current))

def STATEMENT_LIST(current, G):
	current = STATEMENT(current, G)
	if current.name != "SEMICOLON":
		raise ParserError("Statement doesn't end with a semicolon" + getTokenLineInfo(current))
	current = next(G)
	while current.name != "END":
		current = STATEMENT(current, G) #needs to return a semicolon for a valid statement
		if current.name != "SEMICOLON":
			raise ParserError("Statement doesn't end with a semicolon" + getTokenLineInfo(current))
		current = next(G)
	return current

def STATEMENT(current, G):
	if current.name == "ID":
		current = ASSIGNMENT(current, G) #make sure ASSIGNMENT is returning next(G)
		return current #current should be a ;

	elif current.name == "READ":
		current = next(G)
		if not current.name == "LPAREN":
			raise ParserError("READ token is not followed by a (" + getTokenLineInfo(current))
		current = ID_LIST(next(G), G) #should be returning a )
		if not current.name == "RPAREN":
			raise ParserError("Missing closing ) in READ statement" + getTokenLineInfo(current))
		return next(G)  #next(G) should be a ;

	elif current.name == "WRITE":
		current = next(G)
		if not current.name == "LPAREN":
			raise ParserError("WRITE token is not followed by a (" + getTokenLineInfo(current))
		current = EXPR_LIST(next(G), G) #should be returning a )
		if not current.name == "RPAREN":
			raise ParserError("Missing closing ) in WRITE statement" + getTokenLineInfo(current))
		return next(G)  #next(G) should be a ;

	else:
		raise ParserError("Inappproriate token to start a statement" + getTokenLineInfo(current))

def ASSIGNMENT(current, G):
	current = IDENT(current, G) #should return a :=
	if not current.name == "ASSIGNOP":
		raise ParserError("Assignment operator does not follow identifer in assignment statement" + getTokenLineInfo(current))
	current = EXPRESSION(next(G), G) # should return something that follows expression - we will check for it in whereever this function returns
	return current

def ID_LIST(current, G):
	current = IDENT(current, G)
	while current.name == "COMMA":
		current = next(G)
		current = IDENT(current, G)
	return current # should return a )

def EXPR_LIST(current, G):
	current = EXPRESSION(current, G)
	while current.name == "COMMA":
		current = next(G)
		current = EXPRESSION(current, G)
	return current # should return a ; (if called from ASSIGNMENT) or return ) (if called from STATEMENT)

def IDENT(current, G):
	#probably don't need to check this again since currently the only way to get to this branch is through assignment
	#and the only way to get to assignment is through STATEMENT if it is an ID
	if not current.name == "ID":
		raise ParserError("Invalid identifier" + getTokenLineInfo(current))
	# when we are actually building the tree we will need to parse the ID here/store it in the symbol table here
	return next(G)

def EXPRESSION(current, G):
	current = PRIMARY(current, G) #should return something in { "," , ; , ) , + , - }
	while current.name == "PLUS" or current.name == "MINUS": # loop until what is returned is not an arithop (we are chaining expressions e.g. (1+2)+12-13 etc.
		current = PRIMARY(next(G), G)
	return current #current should be in { "," , ; , ) } - ";" gets checked in STATEMENT_LIST, "," gets checked in EPRS_LIST, and ) gets checked in STATEMENT

def PRIMARY(current, G):
	if current.name == "LPAREN":
		current = EXPRESSION(next(G), G)
		if not current.name == "RPAREN":
			raise ParserError("Expression not followed by matching ')' (in primary function)" + getTokenLineInfo(current))
		return next(G) # should return something in {"," , ; , ) , + , -}

	elif current.name == "ID":
		current = IDENT(current, G) #IDENT processes the ID and returns next token
		return current # should return something in {"," , ; , ) , + , -}

	elif current.name == "INTLIT":
		# process the INTLIT here when building tree before returning the next (G)
		return next(G) # should return something in {"," , ; , ) , + , -}

	else:
		raise ParserError("Inappropriate starting token in primary" + getTokenLineInfo(current))

def ARITH_OP(current, G):
	# process the ARITHOP here when building tree before returning the next (G)
	return next(G) # should return something in  ( , ID , INTLITERAL }