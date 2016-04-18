Project 3 checked if the source code was in the language. This project extends that functionality by building
and abstract syntrax tree and symbol table from the source.

The resulting tree is serialized using newick strings (e.g. (BEGIN,((read,((id)IDENT,(id)IDENT,(id)IDENT)ID_LIST)STATEMENT)STATEMENT_LIST,END)PROGRAM;)

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

ARITH_OP	->	+ | -## Grammar
