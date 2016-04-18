This project adds a code generator and compiler module to the project. In order to accomplish this the parser
needed to be modified to store the intliteral and identifier data in the nodes.


## Compiler.py
compiler.py sets up argparse which allows the compiler to be run from the command line using the following command:

python compiler.py -t tokens.txt source.txt out.asm

Defaults

## Code_generator.py
* traverses the abstract syntax tree and generates the relevant mips code.
* checks if variables are initialized before use (semantic error checking)

## Augmented Grammar

<program>	->	#start begin <statement list> end #finish

<statement list>	->	<statement>; { <statement>; }

<statement>	 ->	<assignment> | read( <id list> #read_ids ) | write( <expr list> #write_ids )

<assignment>	->	<ident> := <expression> #assign

<id list>	->	<ident> {, <ident>}

<expr list>	->	<expression> {, <expression> }

<expression>	->	<primary> {<arith op> <primary> #infix }

<primary>	->	( <expression> ) | <ident> | INTLITERAL

<ident>	->	ID #process

<arith op>	->	+ | -

**#process is handled in the parser