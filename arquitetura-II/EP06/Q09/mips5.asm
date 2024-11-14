.globl main

.data
	x1: .word 15
	x2: .word 25
	x3: .word 13
	x4: .word 17	
	soma: .word -1
.text
main:
	#armazenando a primeira memoria em t0
	ori $t0,$zero,0x1001
	sll $t0,$t0,16
	
	#atribui um registrador para cada dado registrado na memoria
	lw $t1,0($t0)
	lw $t2,4($t0)
	lw $t3,8($t0)
	lw $t4,12($t0)
	
	#realiza a soma
	add $t5,$t1,$t2
	add $t5,$t5,$t3
	add $t5,$t5,$t4
	
	#salva o resultado da soma pra memoria
	sw $t5,16($t0)