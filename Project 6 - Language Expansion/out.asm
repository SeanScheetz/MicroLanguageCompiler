	.data
z:	.word	0
x:	.word	0
y:	.word	0
prompt_int:	.asciiz	"Enter an int to store in a variable: "

	.text
main:
# assign value to x.
li		$t0, 0
li		$t1, 7
add		$t0, $t0, $t1
sw		$t0, x

# assign value to y.
li		$t0, 0
li		$t1, 8
add		$t0, $t0, $t1
sw		$t0, y

# assign value to z.
li		$t0, 0
lw		$t1, x
add		$t0, $t0, $t1
sw		$t0, z

# Writing values of an <expr_list>.
li		$v0, 1
li		$t0, 0
lw		$t1, x
add		$t0, $t0, $t1
move	$a0, $t0
syscall
li		$v0, 1
li		$t0, 0
lw		$t1, y
add		$t0, $t0, $t1
move	$a0, $t0
syscall
