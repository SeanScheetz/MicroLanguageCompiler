	.data
x:	.word	0
y:	.word	0
prompt_int:	.asciiz	"Enter an int to store in a variable: "

	.text
main:
# assign value to y.
li		$t0, 0
li		$t1, 12
add		$t0, $t0, $t1
sw		$t0, y

# assign value to x.
li		$t0, 0
li		$t1, 1
add		$t0, $t0, $t1
addi	$sp, $sp, -4
sw		$t0, 0($sp)
li		$t0, 0
li		$t1, 2
add		$t0, $t0, $t1
addi	$sp, $sp, -4
sw		$t0, 0($sp)
li		$t0, 0
li		$t1, 3
add		$t0, $t0, $t1
lw		$t1, y
add		$t0, $t0, $t1
lw		$t2, 0($sp)
addi	$sp, $sp, 4
add		$t0, $t0, $t2
lw		$t2, 0($sp)
addi	$sp, $sp, 4
add		$t0, $t0, $t2
sw		$t0, x

# Writing values of an <expr_list>.
li		$v0, 1
li		$t0, 0
lw		$t1, x
add		$t0, $t0, $t1
move	$a0, $t0
syscall
