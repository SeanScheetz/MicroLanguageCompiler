	.data
x:	.word	0
prompt_int:	.asciiz	"Enter an int to store in a variable: "

	.text
main:
# assign value to x.
li		$t0, 0
li		$t1, 0
add		$t0, $t0, $t1
sw		$t0, x

# assign value to x.
li		$t0, 0
lw		$t1, x
add		$t0, $t0, $t1
li		$t1, 3
add		$t0, $t0, $t1
sw		$t0, x

