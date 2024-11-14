.globl main

.data
	x: .word 5
	z: .word 7
	y: .word 0

.text

main:
	#pega o valor da primeira pos de memoria
	ori $s0,$zero,0x1001
	sll $s0,$s0,16
	
	lw $t1, 0($s0) #x
	lw $t2, 4($s0) #z
	
	sll $t3,$t1,7 #128x
	sub $t3, $t3,1 #127x
	
	sll $t4,$t2,6 #64z
	add $t4,$t4,$t2 #65z
	
	sub $t3,$t3,$t4 # 127x - 65z
	addi $t3,$t3,1 # 127x - 65z + 1
	sw $t3,8($s0)
	