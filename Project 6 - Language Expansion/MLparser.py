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

	elif current.t_class == "TYPE":
		current, child, s1 = DECLARATION(current, G) # DECLARATION returns a next(G)
		t.children.append(child)
		s.update(s1)
		return current, t, s # #current should be a ; at this point

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

def DECLARATION(current, G):
	#only way to get here it if STATEMENT sees a token with t_class = "TYPE" so don't need to check again here
	t = tree("DECLARATION")
	s = {}
	current, child, s1 = TYPE(current, G) #TYPE returns next(G) because it processes the type token
	t.children.append(child)
	s.update(s1)
	current, child, s1 = IDENT(current, G) #IDENT returns next(G) because it processes the identifier
	t.children.append(child)
	s.update(s1)
	return current, t, s

def TYPE(current, G):
	t = tree("TYPE")
	s = {}
	if current.name == "STRING":
		t.children.append(tree("STRING"))
	elif current.name == "INT":
		t.children.append(tree("INT"))
	elif current.name == "BOOL":
		t.children.append(tree("BOOL"))
	return next(G), t, s

def EXPRESSION(current, G):
	t = tree("EXPRESSION")
	s = {}
	current, child, s1 = TERM1(current, G) #term1 should return next(G) I think? in current setup, we are doing error checking at lowest level
	t.children.append(child)
	s.update(s1)
	while current.name == "OR":
		t.children.append("OR")
		current = next(G) #move to token after "or"
		current, child, s1 = TERM1(current, G)
		t.children.append(child)
		s.update(s1)
	return current, t, s # current should be in {),;}

def TERM1(current, G):
	t = tree("TERM1")
	s = {}
	current, child, s1 = FACT1(current, G)
	t.children.append(child)
	s.update(s1)
	while current.name == "AND":
		t.children.append("AND")
		current = next(G) #move to token after "and"
		current, child, s1 = FACT1(current, G)
		t.children.append(child)
		s.update(s1)
	return current, t, s # current should be in {),;}

def FACT1(current, G):
	t = tree("FACT1")
	s = {}
	if current.name == "NOT":
		current, child, s1 = PRIMARY(next(G), G)
		t.children.append(child)
		s.update(s1)
		return current, t, s
	else: #doing error checking at lowest level because first set for FACT1 is too big
		current, child, s1 = EXP2(next(G), G) #EXP2 needs to return a useful current
		t.children.append(child)
		s.update(s1)
		current, child, s1 = RELATION(current, G) #relation needs to return a useful current
		t.children.update(child) #Is this supposed to be append??
		s.update(s1)
		return current, child, s1  #should this not return s instead of s1? 
		
def RELATION(current, G):
	t = tree("RELATION")
	s = {}
	if current.name == "RELATIONOP":
		t.val = current.pattern
		t.children.append(tree("RELATIONOP", val = current.pattern)
		current, child, s1 = EXP2(next(G), G)
		t.children.append(child)
		s.update(s1)
		return current, child, s
	else:
		return next(G), child, s
		
def EXP2(current, G):
	t = tree("EXP2")
	s = {}
	current, child, s1 = TERM2(current, G)
	t.children.append(child)
	s.update(s1)
	while current.name == "ARITHOP"
		t.children.append(tree("ARITHOP", val = current.pattern)
		current, child, s1 = TERM2(next(G), G)
		t.children.append(child)
		s.update(s1)
	return current, child, s1
		
	
		
		

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
		t.val = child.val
		t.children.append(child)
		s.update(s1)
		return current, t, s # should return something in {"," , ; , ) , + , -}

	elif current.name == "INTLIT":
		t.val = current.pattern
		t.children.append(tree("INTLIT", val = current.pattern))
		return next(G), t, s # should return something in {"," , ; , ) , + , -}

	elif current.name == "BOOLLIT":
		t.val = current.pattern
		t.children.append(tree("BOOLLIT", val = current.pattern))
		return next(G), t, s

	elif current.name == "STRINGLIT":
		t.val = current.pattern
		t.children.append(tree("STRINGLIT"), val = current.pattern)
		return next(G), t, s

	else:
		raise ParserError("Syntax Error: Inappropriate starting token in primary" + getTokenLineInfo(current))

def IDENT(current, G):
	t = tree("IDENT")
	s = {current.pattern: 0}
	if not current.name == "ID":
		raise ParserError("Syntax Error: Invalid identifier" + getTokenLineInfo(current))
	t.val = current.pattern
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