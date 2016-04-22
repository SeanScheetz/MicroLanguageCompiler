	.data
x:	.word	0
prompt_int:	.asciiz	"Enter an int to store in a variable: "

	.text
main:
# assign value to x.
li		$t0, 0
sw		$t0, x

