	.data
x:	.word	0
prompt_int:	.asciiz	"Enter an int to store in a variable: "

	.text
main:
# assign value to x.
li		$t0, 0
sw		$t0, x

# Writing values of an <expr_list>.
li		$v0, 1
li		$t0, 0
move	$a0, $t0
syscall
li		$v0, 1
li		$t0, 0
move	$a0, $t0
syscall
