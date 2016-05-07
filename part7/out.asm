	.data
prompt_int:	.asciiz	"Enter an int to store in a variable: "
x:	.word	0
	.data
prompt_int:	.asciiz	"Enter an int to store in a variable: "
string0:	.asciiz	"Yes\n"
	.data
prompt_int:	.asciiz	"Enter an int to store in a variable: "
string1:	.asciiz	"No\n"

	.text
# assign value to x.
li	$t6, 0
li	$t7, 1
li	$t9, 1
move	$t8, $t9
and	$t7, $t7, $t8
or	$t6, $t6, $t7
sw		$t6, x


	.text
# Writing values of an <expr_list>.
# Writing a string expression
li		$v0, 4
la	$a0, string0
syscall
addi	$a0, $zero, 0xA
addi	$v0, $zero, 0xB
syscall
