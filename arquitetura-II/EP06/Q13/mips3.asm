.globl main
.data
	valor1: .word -10
	

.text
main:

ori $s0,$zero,0x1001
sll $s0,$s0,16
lw $t1,0($s0)
sra $t2,$t1,31
#sra $t1,$t1, 31
beq $t2,$zero,positivo
bne $t2,$zero,negativo



positivo:
	sw $t1,0($s0)
negativo:
	sub $t3,$zero,$t1
	sw $t3,0($s0)