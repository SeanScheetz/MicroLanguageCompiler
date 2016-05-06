	.data
prompt_int:	.asciiz	"Enter an int to store in a variable: "
x:	.word	0
y:	.word	0
l:	.word	0

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
li	$t2, 5
add	$t1, $t1, $t2
add	$t0, $t0, $t1
sw		$t0, y

