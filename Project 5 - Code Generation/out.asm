	.data
x:	.word	0
y:	.word	0
z:	.word	0
prompt_int:	.asciiz	"Enter an int to store in a variable: "

	.text
main:
li	$v0, 4
la	$a0, prompt_int
syscall
li	$v0, 5
syscall
sw	$v0, x

li	$v0, 4
la	$a0, prompt_int
syscall
li	$v0, 5
syscall
sw	$v0, y

li	$v0, 4
la	$a0, prompt_int
syscall
li	$v0, 5
syscall
sw	$v0, z

