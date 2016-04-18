This project begins the implementation of an actual micro languages using projects 1 and 2.

The lexar from project 1 to create a token stream which is in turn used to parse an input program written
in my micro language. The result is a simple true false indicating whether or not the program is valid
according to the language definition.

## Grammar

PROGRAM	->	begin STATEMENT_LIST end

STATEMENT_LIST	->	STATEMENT; { STATEMENT; }

STATEMENT	->	ASSIGNMENT| read( ID_LIST ) | write( EXPR_LIST )

ASSIGNMENT|	->	IDENT := EXPRESSION

ID_LIST	->	IDENT {, IDENT}

EXPR_LIST	->	EXPRESSION {, EXPRESSION }

EXPRESSION	->	PRIMARY {ARITH_OP PRIMARY }

PRIMARY	->	( EXPRESSION ) | IDENT | intliteral (intlit is a terminal)

IDENT	->	id  (id is a terminal)

ARITH_OP	->	+ | -