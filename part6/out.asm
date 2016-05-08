	.data
prompt_int:	.asciiz	"Enter an int to store in a variable: "
n:	.word	0
s:	.word	0
p:	.word	0
i:	.word	0
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

#Starting while loop
label1:
li	$t6, 0
li	$t7, 1
li	$t0, 0
li	$t1, 0
lw	$t2, i
add	$t1, $t1, $t2
add	$t0, $t0, $t1
move	$t5, $t0
li	$t0, 0
li	$t1, 0
lw	$t2, n
add	$t1, $t1, $t2
add	$t0, $t0, $t1
slt	$t8, $t5, $t0
and	$t7, $t7, $t8
or	$t6, $t6, $t7
li	$t0, 1
bne	$t0, $t6, out1
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


j	label1
out1:
# Writing values of an <expr_list>.
# Writing an integer expression
li		$v0, 1
li	$t0, 0
li	$t1, 0
lw	$t2, s
add	$t1, $t1, $t2
add	$t0, $t0, $t1
move	$a0, $t0
syscall
addi	$a0, $zero, 0xA
addi	$v0, $zero, 0xB
syscall
# Writing a string expression
li		$v0, 4
la	$a0, string1
syscall
addi	$a0, $zero, 0xA
addi	$v0, $zero, 0xB
syscall
# Writing an integer expression
li		$v0, 1
li	$t0, 0
li	$t1, 0
lw	$t2, p
add	$t1, $t1, $t2
add	$t0, $t0, $t1
move	$a0, $t0
syscall
addi	$a0, $zero, 0xA
addi	$v0, $zero, 0xB
syscall
# Writing a string expression
li		$v0, 4
la	$a0, string1
syscall
addi	$a0, $zero, 0xA
addi	$v0, $zero, 0xB
syscall
