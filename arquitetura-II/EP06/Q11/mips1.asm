.globl main

.data
	x: .word 100000
	z: .word 200000
	y: .word 0
	
.text

main:

#carregar memoria
ori $s0,$zero,0x1001
sll $s0,$s0,16 #0x10010000

lw $t0,0($s0) #x
lw $t1,4($s0) #z

sub $t2,$t0,$t1 #x-z
addi $s1,$t2,300000 #x-z+300000
sw $s1, 8($s0)
