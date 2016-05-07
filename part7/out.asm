	.data
prompt_int:	.asciiz	"Enter an int to store in a variable: "
i:	.word	0
n:	.word	0

	.text
# assign value to i.
li	$t0, 0
li	$t1, 0
li	$t2, 0
add	$t1, $t1, $t2
add	$t0, $t0, $t1
sw		$t0, i

# assign value to n.
li	$t0, 0
li	$t1, 0
li	$t2, 3
add	$t1, $t1, $t2
add	$t0, $t0, $t1
sw		$t0, n

