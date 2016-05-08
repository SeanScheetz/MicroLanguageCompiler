	.data
prompt_int:	.asciiz	"Enter an int to store in a variable: "
i:	.word	0
n:	.word	0
z:	.word	0
string0:	.asciiz	"first test"

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

# assign value to z.
li	$t0, 0
li	$t1, 0
li	$t2, 5
add	$t1, $t1, $t2
add	$t0, $t0, $t1
sw		$t0, z

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
# starting if statement
li	$t6, 0
li	$t7, 1
li	$t9, 1
move	$t8, $t9
and	$t7, $t7, $t8
or	$t6, $t6, $t7
li	$t0, 1
bne	$t0, $t6, out2
# starting if statement
li	$t6, 0
li	$t7, 1
li	$t9, 1
move	$t8, $t9
and	$t7, $t7, $t8
or	$t6, $t6, $t7
li	$t0, 1
bne	$t0, $t6, out3
# Writing values of an <expr_list>.
# Writing a string expression
li		$v0, 4
la	$a0, string0
syscall
addi	$a0, $zero, 0xA
addi	$v0, $zero, 0xB
syscall

out3:

out2:
# Writing values of an <expr_list>.
# Writing an integer expression
li		$v0, 1
li	$t0, 0
li	$t1, 0
lw	$t2, i
add	$t1, $t1, $t2
add	$t0, $t0, $t1
move	$a0, $t0
syscall
addi	$a0, $zero, 0xA
addi	$v0, $zero, 0xB
syscall
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
#Starting while loop
label4:
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
lw	$t2, z
add	$t1, $t1, $t2
add	$t0, $t0, $t1
slt	$t8, $t5, $t0
and	$t7, $t7, $t8
or	$t6, $t6, $t7
li	$t0, 1
bne	$t0, $t6, out4
# Writing values of an <expr_list>.
# Writing an integer expression
li		$v0, 1
li	$t0, 0
li	$t1, 0
lw	$t2, i
add	$t1, $t1, $t2
add	$t0, $t0, $t1
move	$a0, $t0
syscall
addi	$a0, $zero, 0xA
addi	$v0, $zero, 0xB
syscall
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


j	label4
out4:
