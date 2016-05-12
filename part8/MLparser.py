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
    return " - line_num: " + str(token.line_num) + " col: " + str(token.col)


def parser(source_file, token_file):
    """
    :param source_file: A program written in the ML language.
    :param token_file: A file defining the types of tokens in the ML language
    returns True if the code is syntactically correct.
    Throws a ParserError otherwise.
    """

    G = lexer(source_file, token_file)
    try:
        current, t, s = PROGRAM(next(G), G)
        try:
            next(G)  # at this point the source should have no more tokens - if the iterator has more, then it is actually a ParserError
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

    if current.name == "DEF":
        current, child, s1 = FUNCTION_LIST(current, G)
        t.children.append(child)
        s.update(s1)
        if current.name != "BEGIN":
            raise ParserError("Syntax error: BEGIN keyword doesn't follow function declarations." + getTokenLineInfo(current))
        t.children.append(tree("BEGIN"))
        current = next(G)
        current, child, s1 = STATEMENT_LIST(current, G)
        t.children.append(child)
        s.update(s1)
        if current.name == "END":
            t.children.append(tree("END"))
            s.update(s1)
            return current, t, s
        else:
            raise ParserError("Syntax Error: Statement list complete, but no END token to signal end of program" + getTokenLineInfo(current))

    elif current.name == "BEGIN":
        t.children.append(tree("FUNCTION LIST"))
        t.children[0].children.append(tree("LABMDA"))
        t.children.append(tree("BEGIN"))
        current = next(G)
        current, child, s1 = STATEMENT_LIST(current, G)
        t.children.append(child)
        s.update(s1)
        if current.name == "END":
            t.children.append(tree("END"))
            s.update(s1)
            return current, t, s
        else:
            raise ParserError("Syntax Error: Statement list complete, but no END token to signal end of program" + getTokenLineInfo(current))

    else:
        raise ParserError(
            "Syntax Error: Program doesn't begin with BEGIN or function declaration" + getTokenLineInfo(current))

def FUNCTION_LIST(current, G):
    t = tree("FUNCTION LIST")
    s = {}

    while current.name == "DEF":
        current, child, s1 = FUNCTION_DECLARATION(current, G)
        t.children.append(child)
        s.update(s1)
    return current, t, s

def FUNCTION_DECLARATION(current, G):
    t = tree("FUNCTION DECLARATION")
    s = {}
    if current.name != "DEF":
        raise ParserError("Syntax Error: Function declaration does not begin with def keyword" + getTokenLineInfo(current))
    t.children.append(tree("DEF"))
    current = next(G)
    if current.t_class != "TYPE":
        raise ParserError("Syntax Error: Function declaration does not have a return type " + getTokenLineInfo(current))
    current, child, s1, vartype = TYPE(current, G)
    t.children.append(child)
    if current.name != "ID":
        raise ParserError("Syntax Error: Function does not have an identifier " + getTokenLineInfo(current))
    current, child, s1 = IDENT(current, G)
    t.children.append(child)
    if current.name != "LPAREN":
        raise ParserError("Syntax Error: Function is missing opening paren for parm list " + getTokenLineInfo(current))
    current = next(G)
    current, child, s1 = PARAM_LIST(current, G)
    t.children.append(child)
    s.update(s1)
    if current.name != "RPAREN":
        raise ParserError("Syntax Error: Function param list missing closing paren " + getTokenLineInfo(current))
    current = next(G)
    if current.name != "COLON":
        raise ParserError("Syntax Error: Function declaration must be followed by a colon " + getTokenLineInfo(current))
    current = next(G)
    current, child, s1 = STATEMENT_LIST(current, G)
    t.children.append(child)
    s.update(s1)

    return current, t, s

def PARAM_LIST(current, G):
    t = tree("PARAM LIST")
    s = {}
    if current.name == "RPAREN":
        t.children.append(tree("LAMBDA"))
        return current, t, s

    if current.t_class != "TYPE":
        raise ParserError("Syntax Error: Parameter must have an associated type." + getTokenLineInfo(current))

    current, child, s1, vartype = TYPE(current, G)
    t.children.append(child)
    s.update(s1)
    current, child, s1 = IDENT(current, G, vartype)
    t.children.append(child)
    s.update(s1)

    while current.name == "COMMA":
        current, child, s1, vartype = TYPE(next(G), G)
        t.children.append(child)
        s.update(s1)
        current, child, s1 = IDENT(current, G, vartype)
        t.children.append(child)
        s.update(s1)

    return current, t, s

def STATEMENT_LIST(current, G):
    t = tree("STATEMENT LIST")
    s = {}
    current, child, s1 = STATEMENT(current, G)  # Child is the STATEMENT tree
    t.children.append(child)
    s.update(s1)
    while current.name != "END" and current.name != "DEF" and current.name != "BEGIN":
        # needs to return a semicolon for a valid statement
        current, child, s1 = STATEMENT(current, G)
        t.children.append(child)
        s.update(s1)
    return current, t, s


def STATEMENT(current, G):
    t = tree("STATEMENT")
    s = {}
    if current.name == "ID":
        # make sure ASSIGNMENT is returning next(G)
        current, child, s1 = ASSIGNMENT(current, G)
        t.children.append(child)
        s.update(s1)
        if current.name != "SEMICOLON":
            raise ParserError("Syntax Error: Statement doesn't end with a semicolon" + getTokenLineInfo(current))

        return next(G), t, s  # current should be a ;

    elif current.name == "READ":
        t.children.append(tree("READ"))
        current = next(G)
        if not current.name == "LPAREN":
            raise ParserError(
                "Syntax Error: READ token is not followed by a (" + getTokenLineInfo(current))
        current, child, s1 = ID_LIST(next(G), G)  # should be returning a )
        t.children.append(child)  # child should be the ID_LIST tree
        s.update(s1)
        if not current.name == "RPAREN":
            raise ParserError(
                "Syntax Error: Missing closing ) in READ statement" + getTokenLineInfo(current))
        current = next(G)
        if current.name != "SEMICOLON":
            raise ParserError("Syntax Error: Statement doesn't end with a semicolon" + getTokenLineInfo(current))
        return next(G), t, s  # next(G) should be a <statement>

    elif current.name == "WRITE":
        t.children.append(tree("WRITE"))
        current = next(G)
        if not current.name == "LPAREN":
            raise ParserError(
                "Syntax Error: WRITE token is not followed by a (" + getTokenLineInfo(current))
        current, child, s1 = EXPR_LIST(next(G), G)  # should be returning a )
        t.children.append(child)
        s.update(s1)
        if not current.name == "RPAREN":
            raise ParserError(
                "Syntax Error: Missing closing ) in WRITE statement" + getTokenLineInfo(current))
        current = next(G)
        if current.name != "SEMICOLON":
            raise ParserError("Syntax Error: Statement doesn't end with a semicolon" + getTokenLineInfo(current))

        return next(G), t, s  # next(G) should be a <statement>

    elif current.t_class == "TYPE":
        # DECLARATION returns a next(G)
        current, child, s1 = DECLARATION(current, G)
        t.children.append(child)
        s.update(s1)
        if current.name != "SEMICOLON":
            raise ParserError("Syntax Error: Statement doesn't end with a semicolon" + getTokenLineInfo(current))

        return next(G), t, s  # current should be a ; at this point

    elif current.name == "FUNC":
        t.children.append(tree("FUNC"))
        current = next(G)
        current, child, s1 = IDENT(current, G)
        t.children.append(child)
        s.update(s1)
        if current.name != "LPAREN":
            raise ParserError("Syntax Error: Function call missing opening param to arg list" + getTokenLineInfo(current))
        current = next(G)
        current, child, s1 = ARGLIST(current, G)
        t.children.append(child)
        s.update(s1)
        if current.name != "RPAREN":
            raise ParserError("Syntax Error: Function call missing closing param to arg list" + getTokenLineInfo(current))
        current = next(G)
        if current.name != "SEMICOLON":
            raise ParserError("Syntax Error: Function call doesn't end with a semicolon " + getTokenLineInfo(current))
        return next(G), t, s

    elif current.name == "IF":
        t.children.append(tree("IF"))
        current, child, s1 = EXPRESSION(next(G), G)
        t.children.append(child)
        s.update(s1)
        if not current.name == "THEN":
            raise ParserError("Syntax Error: If must be followed with then")
        t.children.append(tree("THEN"))
        current, child, s1 = PROGRAM(next(G), G)
        t.children.append(child)
        s.update(s1)
        current = next(G)
        if current.name == "ELSE":
            t.children.append(tree("ELSE"))
            current, child, s1 = PROGRAM(next(G), G)
            t.children.append(child)
            s.update(s1)
            return next(G), t, s
        return current, t, s

    elif current.name == "WHILE":
        t.children.append(tree("WHILE"))
        current, child, s1 = EXPRESSION(next(G), G)
        t.children.append(child)
        s.update(s1)
        current, child, s1 = PROGRAM(current, G)
        t.children.append(child)
        s.update(s1)
        return next(G), t, s

    elif current.name == "RETURN":
        t.children.append(tree("RETURN"))
        current, child, s1 = RETURN_STMT(next(G), G)
        t.children.append(child)
        s.update(s1)
        if current.name != "SEMICOLON":
            raise ParserError("Syntax Error: Return statement must end with a semicolon." + getTokenLineInfo(current))
        return next(G), t, s

    else:
        raise ParserError("Syntax Error: Inappproriate token to start a statement" + getTokenLineInfo(current))

def ARGLIST(current, G):
    t = tree("ARGLIST")
    s = {}

    if (current.name == "NOT" or current.name == "MINUS" or current.name == "ID" or current.name == "INTLIT"
        or current.name == "BOOLLIT" or current.name == "STRINGLIT" or current.name == "LPAREN"):
        current, child, s1 = EXPR_LIST(current, G)
        t.children.append(child)
        s.update(s1)
        return current, t, s

    else:
        t.children.append(tree("LAMBDA"))
        return current, t, s

def RETURN_STMT(current, G):
    t = tree("RETURN STATEMENT")
    s = {}
    current, child, s1 = FACT2(current, G)
    t.children.append(child)
    s.update(s1)
    return current, child, s


def ASSIGNMENT(current, G):
    t = tree("ASSIGNMENT")
    s = {}
    current, child, s1 = IDENT(current, G)
    t.children.append(child)
    s.update(s1)
    if not current.name == "ASSIGNOP":
        raise ParserError(
            "Syntax Error: Assignment operator does not follow identifier in assignment statement" + getTokenLineInfo(current))
    # should return something that follows expression - we will check for it
    # in whereever this function returns
    current, child, s1 = EXPRESSION(next(G), G)
    t.children.append(child)  # child should be EXPRESSION tree
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
    return current, t, s  # should return a )


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
    # should return a ; (if called from ASSIGNMENT) or return ) (if called
    # from STATEMENT)
    return current, t, s


def DECLARATION(current, G):
    # only way to get here it if STATEMENT sees a token with t_class = "TYPE"
    # so don't need to check again here
    t = tree("DECLARATION")
    s = {}
    # TYPE returns next(G) because it processes the type token
    current, child, s1, vartype = TYPE(current, G)
    t.children.append(child)
    s.update(s1)
    # IDENT returns next(G) because it processes the identifier
    current, child, s1 = IDENT(current, G, vartype)
    t.children.append(child)
    s.update(s1)
    return current, t, s


def TYPE(current, G):
    t = tree("TYPE")
    s = {}
    if current.name == "INT":
        t.children.append(tree("INT"))
        return next(G), t, s, "INT"
    elif current.name == "BOOL":
        t.children.append(tree("BOOL"))
        return next(G), t, s, "BOOL"
    elif current.name == "STRING":
        t.children.append(tree("STRING"))
        return next(G), t, s, "STRING"
    elif current.name == "VOID":
        t.children.append(tree("VOID"))
        return next(G), t, s, "VOID"


def EXPRESSION(current, G):
    t = tree("EXPRESSION")
    s = {}
    # term1 should return next(G) I think? in current setup, we are doing
    # error checking at lowest level
    current, child, s1 = TERM1(current, G)
    t.children.append(child)
    s.update(s1)
    while current.name == "OR":
        t.children.append(tree("OR"))
        current = next(G)  # move to token after "or"
        current, child, s1 = TERM1(current, G)
        t.children.append(child)
        s.update(s1)
    return current, t, s  # current should be in {),;}


def TERM1(current, G):
    t = tree("TERM1")
    s = {}
    current, child, s1 = FACT1(current, G)
    t.children.append(child)
    s.update(s1)
    while current.name == "AND":
        t.children.append(tree("AND"))
        current = next(G)  # move to token after "and"
        current, child, s1 = FACT1(current, G)
        t.children.append(child)
        s.update(s1)
    return current, t, s  # current should be in {),;}


def FACT1(current, G):
    t = tree("FACT1")
    s = {}
    if current.name == "NOT":
        t.children.append(tree("NOT"))
        current, child, s1 = FACT2(next(G), G)
        t.children.append(child)
        s.update(s1)
        return current, t, s
    else:  # doing error checking at lowest level because first set for FACT1 is too big
        # EXP2 needs to return a useful current
        current, child, s1 = EXP2(current, G)
        t.children.append(child)
        s.update(s1)
        # relation needs to return a useful current
        current, child, s1 = RELATION(current, G)
        t.children.append(child)  # t.children.update(child) (OLD CODE)
        s.update(s1)
        return current, t, s  # return current, child, s1 (OLD CODE)


def RELATION(current, G):
    t = tree("RELATION")
    s = {}
    if current.t_class == "RELATIONOP":
        t.val = current.pattern
        t.children.append(tree("RELATIONOP", val=current.pattern))
        # assume exp2 returns a useful current
        current, child, s1 = EXP2(next(G), G)
        t.children.append(child)
        s.update(s1)
        return current, t, s
    else:
        t.children.append(tree("LAMBDA"))
        return current, t, s


def EXP2(current, G):
    t = tree("EXP2")
    s = {}
    current, child, s1 = TERM2(current, G)
    t.children.append(child)
    s.update(s1)
    while current.name == "PLUS" or current.name == "MINUS":
        if current.name == "PLUS":
            t.children.append(tree("PLUS"))
        else:  # only other option is "MINUS"
            t.children.append(tree("MINUS"))
        # current returned by TERM2 must be useful
        current, child, s1 = TERM2(next(G), G)
        t.children.append(child)
        s.update(s1)
    return current, t, s


def TERM2(current, G):
    t = tree("TERM2")
    s = {}
    # assumes sign returns useful current
    current, child, s1 = SIGN(current, G)
    t.children.append(child)
    s.update(s1)
    current, child, s1 = FACT2(current, G)
    t.children.append(child)
    s.update(s1)
    while current.name == "TIMES" or current.name == "DIVIDE" or current.name == "MODULO":
        if current.name == "TIMES":
            t.children.append(tree("TIMES"))
        elif current.name == "DIVIDE":
            t.children.append(tree("DIVIDE"))
        else:  # current.name == "MODULO"
            t.children.append(tree("MODULO"))
        current, child, s1 = SIGN(next(G), G)
        t.children.append(child)
        s.update(s1)
        # Assumes FACT2 returns useful current
        current, child, s1 = FACT2(current, G)
        t.children.append(child)
        s.update(s1)
    return current, t, s


def SIGN(current, G):
    t = tree("SIGN")
    s = {}
    if current.t_class == "ARITHOP":
        if current.name == "MINUS":
            t.children.append(tree("MINUS"))
            return next(G), t, s
        else:
            raise ParserError(
                "Syntax Error: Invalid sign for number." + getTokenLineInfo(current))
    else:
        t.children.append(tree("LAMBDA"))
        return current, t, s


def FACT2(current, G):
    t = tree("FACT2")
    s = {}
    if current.name == "LPAREN":
        current, child, s1 = EXPRESSION(next(G), G)
        t.children.append(child)
        s.update(s1)
        if not current.name == "RPAREN":
            raise ParserError(
                "Syntax Error: Expression not followed by matching ')' (in primary function)" + getTokenLineInfo(current))
        # should return something in {"," , ; , ) , + , -}
        return next(G), t, s

    elif current.name == "ID":
        # IDENT processes the ID and returns next token
        current, child, s1 = IDENT(current, G)
        t.val = child.val
        t.children.append(child)
        s.update(s1)
        # should return something in {"," , ; , ) , + , -}
        return current, t, s

    elif current.name == "INTLIT":
        t.val = current.pattern
        t.children.append(tree("INTLIT", val=current.pattern))
        # should return something in {"," , ; , ) , + , -}
        return next(G), t, s

    elif current.name == "BOOLLIT":
        t.val = current.pattern
        t.children.append(tree("BOOLLIT", val=current.pattern))
        return next(G), t, s

    elif current.name == "STRINGLIT":
        t.val = current.pattern
        t.children.append(tree("STRINGLIT", val=current.pattern))
        return next(G), t, s

    else:
        raise ParserError(
            "Syntax Error: Inappropriate starting token in FACT2" + getTokenLineInfo(current))


# REPLACED WITH FACT2
def PRIMARY(current, G):
    t = tree("PRIMARY")
    s = {}
    if current.name == "LPAREN":
        current, child, s1 = EXPRESSION(next(G), G)
        t.children.append(child)
        s.update(s1)
        if not current.name == "RPAREN":
            raise ParserError(
                "Syntax Error: Expression not followed by matching ')' (in primary function)" + getTokenLineInfo(current))
        # should return something in {"," , ; , ) , + , -}
        return next(G), t, s

    elif current.name == "ID":
        # IDENT processes the ID and returns next token
        current, child, s1 = IDENT(current, G)
        t.val = child.val
        t.children.append(child)
        s.update(s1)
        # should return something in {"," , ; , ) , + , -}
        return current, t, s

    elif current.name == "INTLIT":
        t.val = current.pattern
        t.children.append(tree("INTLIT", val=current.pattern))
        # should return something in {"," , ; , ) , + , -}
        return next(G), t, s

    elif current.name == "BOOLLIT":
        t.val = current.pattern
        t.children.append(tree("BOOLLIT", val=current.pattern))
        return next(G), t, s

    elif current.name == "STRINGLIT":
        t.val = current.pattern
        print(t)
        t.children.append(tree("STRINGLIT"), val=current.pattern)
        return next(G), t, s

    else:
        raise ParserError(
            "Syntax Error: Inappropriate starting token in primary" + getTokenLineInfo(current))


def IDENT(current, G, vartype="notype"):
    t = tree("IDENT")
    s = {}
    if not vartype == "notype":
        s = {current.pattern: [vartype, 0, 0]} #vartype, decl flag, init flag
    if not current.name == "ID":
        raise ParserError("Syntax Error: Invalid identifier" +
                          getTokenLineInfo(current))
    t.val = current.pattern
    t.children.append(tree("ID", val=current.pattern))
    return next(G), t, s


