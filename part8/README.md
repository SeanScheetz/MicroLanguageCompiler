This project adds a code generator and compiler module to the project. In order to accomplish this the parser
needed to be modified to store the intliteral and identifier data in the nodes.

## Current Tasks
2. Write the code to print a string lit (it is in the write_list function)
4. Potentially refactor part 2 into solve_string_expression


## Compiler.py
compiler.py sets up argparse which allows the compiler to be run from the command line using the following command:

python compiler.py -t tokens.txt source.txt out.asm


## Code_generator.py
* traverses the abstract syntax tree and generates the relevant mips code.
* checks if variables are initialized before use (semantic error checking)

## Augmented Grammar

PROGRAM	-> #start	begin STATEMENT_LIST end #finish

STATEMENT_LIST	->	STATEMENT; { STATEMENT; #read_ids}

STATEMENT	->	ASSIGNMENT | read( ID_LIST ) | write( EXPR_LIST #write_ids)

ASSIGNMENT|	->	IDENT := EXPRESSION #assign

ID_LIST	->	IDENT {, IDENT}

EXPR_LIST	->	EXPRESSION {, EXPRESSION }

EXPRESSION	->	PRIMARY {ARITH_OP PRIMARY } #solve_expression

PRIMARY	->	( EXPRESSION ) | IDENT | intliteral (intlit is a terminal)

IDENT	->	id  (id is a terminal) #process

ARITH_OP	->	+ | -

**#process is actually done in the parser