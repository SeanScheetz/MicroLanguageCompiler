	.data
prompt_int:	.asciiz	"Enter an int to store in a variable: "
n:	.word	0

	.text
# Writing values of an <expr_list>.
# Writing an integer expression
li		$v0, 1
li	$t0, 0
li	$t1, 0
lw	$t2, n
add	$t1, $t1, $t2
add	$t0, $t0, $t1
move	$a0, $t0
syscall
addi	$a0, $zero, 0xA
addi	$v0, $zero, 0xB
syscall
