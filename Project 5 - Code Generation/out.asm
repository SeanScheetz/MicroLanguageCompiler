	.data
x:	.word	0
prompt_int:	.asciiz	"Enter an int to store in a variable: "
sum_stack:	.word	0:20
var_stack:	.word	0:20
address_counter:	.word	0

	.text
main:
li	$t0, 0
li	$t1, 20
add	$t0, $t0, $t1
li	$t1, 3
sub	$t0, $t0, $t1
li	$t1, 3
add	$t0, $t0, $t1
li	$t1, 3
add	$t0, $t0, $t1
li	$t1, 3
sub	$t0, $t0, $t1
sw	$t0, x
