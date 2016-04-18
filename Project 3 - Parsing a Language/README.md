This project begins the implementation of an actual micro languages using projects 1 and 2.

The lexar from project 1 to create a token stream which is in turn used to parse an input program written
in my micro language. The result is a simple true false indicating whether or not the program is valid
according to the language definition.

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