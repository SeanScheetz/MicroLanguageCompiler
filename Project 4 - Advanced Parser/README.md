Project 3 checked if the source code was in the language. This project extends that functionality by building
and abstract syntrax tree and symbol table from the source.

The resulting tree is serialized using newick strings (e.g. (BEGIN,((read,((id)IDENT,(id)IDENT,(id)IDENT)ID_LIST)STATEMENT)STATEMENT_LIST,END)PROGRAM;)

## Grammar

<program>	->	begin <statement list> end

<statement list>	->	<statement>; { <statement>; }

<statement>	->	<assignment> | read( <id list> ) | write( <expr list> )

<assignment>	->	<ident> := <expression>

<id list>	->	<ident> {, <ident>}

<expr list>	->	<expression> {, <expression> }

<expression>	->	<primary> {<arith op> <primary> }

<primary>	->	( <epxerssion> ) | <ident> | INTLITERAL

<ident>	->	ID  (that is, an ID token)

<arith op>	->	+ | -