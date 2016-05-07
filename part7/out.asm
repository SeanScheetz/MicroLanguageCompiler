	.data
prompt_int:	.asciiz	"Enter an int to store in a variable: "
n:	.word	0
s:	.word	0
p:	.word	0
i:	.word	0
	.data
prompt_int:	.asciiz	"Enter an int to store in a variable: "
string0:	.asciiz	"\n"
string1:	.asciiz	"\n"

	.text
# assign value to i.
li	$t0, 0
li	$t1, 0
li	$t2, 1
add	$t1, $t1, $t2
add	$t0, $t0, $t1
sw		$t0, i

# assign value to s.
li	$t0, 0
li	$t1, 0
li	$t2, 0
add	$t1, $t1, $t2
add	$t0, $t0, $t1
sw		$t0, s

# assign value to p.
li	$t0, 0
li	$t1, 0
li	$t2, 1
add	$t1, $t1, $t2
add	$t0, $t0, $t1
sw		$t0, p

# Reading values for an <id_list>.
li		$v0, 4
la		$a0, prompt_int
syscall
li		$v0, 5
syscall
sw		$v0, n


	.text
# assign value to s.
li	$t0, 0
li	$t1, 0
lw	$t2, s
add	$t1, $t1, $t2
add	$t0, $t0, $t1
li	$t1, 0
lw	$t2, i
add	$t1, $t1, $t2
add	$t0, $t0, $t1
sw		$t0, s

# assign value to p.
li	$t0, 0
li	$t1, 0
lw	$t2, p
add	$t1, $t1, $t2
lw	$t2, i
mult	$t1, $t2
mflo	$t1
add	$t0, $t0, $t1
sw		$t0, p

# assign value to i.
li	$t0, 0
li	$t1, 0
lw	$t2, i
add	$t1, $t1, $t2
add	$t0, $t0, $t1
li	$t1, 0
li	$t2, 1
add	$t1, $t1, $t2
add	$t0, $t0, $t1
sw		$t0, i

