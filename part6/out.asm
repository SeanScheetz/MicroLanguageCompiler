	.data
prompt_int:	.asciiz	"Enter an int to store in a variable: "
x:	.word	0

	.text
# assign value to x.
li	$t0, 0
li	$t1, 0
li	$t2, 12
add	$t1, $t1, $t2
add	$t0, $t0, $t1
sw		$t0, x

# Writing values of an <expr_list>.
# Writing an integer expression
li		$v0, 1
li	$t0, 0
li	$t1, 0
lw	$t2, x
add	$t1, $t1, $t2
add	$t0, $t0, $t1
move	$a0, $t0
syscall
addi	$a0, $zero, 0xA
addi	$v0, $zero, 0xB
syscall
