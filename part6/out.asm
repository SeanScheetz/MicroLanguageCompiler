	.data
prompt_int:	.asciiz	"Enter an int to store in a variable: "
x:	.word	0
y:	.word	0
z:	.word	0

	.text
# assign value to x.
li	$t0, 0
li	$t1, 0
li	$t2, 1
add	$t1, $t1, $t2
add	$t0, $t0, $t1
sw		$t0, x

# assign value to y.
li	$t0, 0
li	$t1, 0
li	$t2, 2
add	$t1, $t1, $t2
add	$t0, $t0, $t1
sw		$t0, y

# assign value to z.
li	$t0, 0
li	$t1, 0
li	$t2, 3
add	$t1, $t1, $t2
add	$t0, $t0, $t1
sw		$t0, z

# Writing values of an <expr_list>.
# Writing an integer expression
li		$v0, 1
li	$t0, 0
li	$t1, 0
addi	$sp, $sp, -4
sw		$t0, 0($sp)
addi	$sp, $sp, -4
sw		$t1, 0($sp)
li	$t0, 0
li	$t1, 0
lw	$t2, x
add	$t1, $t1, $t2
add	$t0, $t0, $t1
li	$t1, 0
lw	$t2, y
add	$t1, $t1, $t2
add	$t0, $t0, $t1
move	$t2, $t0
lw	$t1, 0($sp)
addi	$sp, $sp, 4
lw	$t0, 0($sp)
addi	$sp, $sp, 4
add	$t1, $t1, $t2
lw	$t2, z
mult	$t1, $t2
mflo	$t1
add	$t0, $t0, $t1
move	$a0, $t0
syscall
addi	$a0, $zero, 0xA
addi	$v0, $zero, 0xB
syscall
