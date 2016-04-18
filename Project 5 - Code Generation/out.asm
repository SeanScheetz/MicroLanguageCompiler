	.data
x:	.word	0
z:	.word	0
w:	.word	0
y:	.word	0
prompt_int:	.asciiz	"Enter an int to store in a variable: "
sum_stack:	.word	0:20
var_stack:	.word	0:20
address_counter:	.word	0

	.text
main:
# assign value to w.
li	$t0, 0
li	$t1, 1
add	$t0, $t0, $t1
sw	$t0, w

# assign value to x.
li	$t0, 0
li	$t1, 3
add	$t0, $t0, $t1
sw	$t0, x

# assign value to y.
li	$t0, 0
li	$t1, 10
add	$t0, $t0, $t1
sw	$t0, y

# assign value to z.
li	$t0, 0
lw	$t1, x
add	$t0, $t0, $t1
li	$t1, 5
sub	$t0, $t0, $t1
lw	$t1, y
add	$t0, $t0, $t1
lw	$t1, y
add	$t0, $t0, $t1
sw	$t0, z

