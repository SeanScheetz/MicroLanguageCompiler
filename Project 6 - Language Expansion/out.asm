	.data
prompt_int:	.asciiz	"Enter an int to store in a variable: "
x:	.asciiz	"12"
string0:	.asciiz	"hi"
string1:	.asciiz	"mark"
string2:	.asciiz	"sean"

	.text
# Writing values of an <expr_list>.
# Writing a string expression
li		$v0, 4
la	$a0, string0
syscall
addi	$a0, $zero, 0xA
addi	$v0, $zero, 0xB
syscall
# Writing a string expression
li		$v0, 4
la	$a0, string1
syscall
addi	$a0, $zero, 0xA
addi	$v0, $zero, 0xB
syscall
# Writing a string expression
li		$v0, 4
la	$a0, string2
syscall
addi	$a0, $zero, 0xA
addi	$v0, $zero, 0xB
syscall
